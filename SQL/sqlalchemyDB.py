
__all__ = ('create_connection_postgresql', 'create_temp_connection')

from functools import lru_cache

import sqlalchemy.exc
from sqlalchemy.engine import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker

from . import models
from . import generators


def create_connection_postgresql(user, password, host, port, path_db):
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{path_db}"
    CreateRecords(url, amount_of_students=2*10**4)
    return SQL(url)


def create_temp_connection():
    url = "sqlite:///:memory:"
    session_data = CreateRecords(url, amount_of_students=1*10**2).session
    sql = SQL(url)
    sql.session = session_data
    return sql


def cache_result(func):
    result = None
    memory = None

    def wrapper(self, *args, **kwargs):
        nonlocal result, memory
        if result is None:
            memory = self._updates
            result = func(self, *args, **kwargs)
            return result

        elif memory == self._updates:
            return result
        else:
            memory = self._updates
            result = func(self, *args, *kwargs)
            return result
    return wrapper


class SQLTools:

    def __init__(self, url):
        self.url = url

        if not database_exists(url):
            create_database(url)
            models.Base.metadata.create_all(bind=create_engine(url))

        self.engine = create_engine(url, echo=False, future=True)
        if url == "sqlite:///:memory:":
            models.Base.metadata.create_all(bind=self.engine)

        self.session = sessionmaker(bind=self.engine)()
        self._updates = 0

    def _drop_database(self):
        self.session.commit()
        self.session.close()
        drop_database(self.url)

    @lru_cache
    def get_course(self, course: str) -> models.Course or ValueError:
        """get instance course from the database"""
        course_db = self.session.query(models.Course).where(models.Course.course_name == course).first()
        if course_db:
            return course_db
        else:
            raise ValueError(f"course {course} doesn't exist")

    @lru_cache
    def get_id_group(self, group: str) -> int or ValueError:
        """get id of group from the database by name"""
        group_db = self.session.query(models.Group).where(models.Group.name == group).first()
        if group_db:
            return int(group_db.id)
        else:
            raise ValueError(f"group {group} doesn't exist")

    @lru_cache
    def get_name_group(self, _id: int) -> str or ValueError:
        """getting name group name by id"""
        group_db = self.session.query(models.Group).where(models.Group.id == _id).first()
        if group_db:
            return str(group_db.name)
        else:
            raise ValueError(f"group with {_id} id doesn't exist")

    @cache_result
    def get_students(self) -> list:
        """getting all student in database and split to various parts for make pages and caching by updates"""
        students = self.session.query(models.Student).all()
        count_in_the_page = 30
        return [students[num:num + count_in_the_page] for num in range(0, len(students), int(count_in_the_page))]

    @cache_result
    def get_groups(self) -> list:
        """getting all groups in database"""
        return self.session.query(models.Group).all()

    @cache_result
    def get_courses(self) -> list:
        """getting all courses in database"""
        return self.session.query(models.Course).all()

    def create_new_student(self, name: str, surname: str, group: str, courses: list) -> models.Student:
        """create instance of student by module"""
        person = models.Student(name=name,
                                surname=surname,
                                group=self.get_id_group(group))
        person.courses += [self.get_course(course) for course in set(courses)]
        return person

    def get_dict_students_from_list(self, list_students) -> dict:
        """transform list of instance to dict"""
        students = {student.id: {'name': str(student.name),
                                 'surname': str(student.surname),
                                 'group': str(self.get_name_group(student.group)),
                                 'courses': list(map(str, student.courses))
                                 } for student in list_students}
        return students


class SQL(SQLTools):
    """class SQL: is for postgresql"""
    def __init__(self, url):
        super().__init__(url)

    def insert_student(self, name: str, surname: str, group: str, courses: list) -> models.Student:
        """insert student into database"""
        student = self.create_new_student(name, surname, group, courses)
        self.session.add(student)
        self.session.commit()
        self._updates += 1
        return student

    def delete_student(self, _id: int) -> models.Student:
        """delete student from database by id"""
        student = self.select_student(_id)
        self.session.delete(student)
        self.session.commit()
        self._updates += 1
        return student

    def update_student(self, _id=None, name=None, surname=None, group=None, courses=[]) -> models.Student:
        """update student in database by id"""
        student = self.select_student(_id)

        student.name = name if name else student.name
        student.surname = surname if surname else student.surname
        student.group = self.get_id_group(group) if group else student.group
        student.courses = [self.get_course(course) for course in set(courses)] if courses else student.courses

        self.session.add(student)
        self.session.commit()
        self._updates += 1
        return student

    def select_student(self, _id: int) -> models.Student or ValueError:
        """select student from database by id"""
        student = self.session.query(models.Student).where(models.Student.id == abs(int(_id))).first()
        if student:
            return student
        else:
            raise ValueError(f"student with id: {_id} doesn't exist")

    def add_student_to_courses(self, _id: int, courses: list) -> models.Student:
        """add student to course in database by id"""
        student = self.select_student(_id)

        student_courses = [course.course_name for course in student.courses]
        courses = [self.get_course(course) for course in set(courses) if course not in student_courses]
        student.courses += courses

        self.session.add(student)
        self.session.commit()
        self._updates += 1
        return student

    def remove_student_from_course(self, _id: int, course: str):
        """remove student from course in database by id"""
        student = self.select_student(_id)
        course_instance = self.get_course(course)
        for index, course in enumerate(student.courses):
            if course_instance == course:
                del student.courses[index]
                break
        self.session.add(student)
        self.session.commit()
        self._updates += 1
        return student

    def get_students_by_course(self, course: str) -> list:
        """get all students in one course"""
        course = self.get_course(course)
        students = [self.select_student(_id) for _id, _ in
                    self.session.query(models.student_course).filter_by(course_id=course.id).all()]
        return students

    def find_less_group(self) -> dict:
        """find group with less student and return {group_name: count}"""
        groups = {group.name: self.session.query(models.Student).filter_by(group=group.id).count()
                  for group in self.get_groups()}
        key = min(groups, key=groups.get)
        return {key: groups[key]}


class CreateRecords(SQLTools):
    """Class use for writing new randomly records"""

    def __init__(self, url, amount_of_students=1*10**3):
        super().__init__(url)

        self.generate_person = generators.GeneratePerson()

        try:
            self.add_courses()
            self.add_groups()
        except sqlalchemy.exc.IntegrityError:  # if courses and groups is exists
            pass
        else:
            self.add_students(amount=amount_of_students)

    def add_courses(self):
        courses = generators.courses
        list_courses = [models.Course(course_name=course, description=description) for course, description in courses]
        self.session.add_all(list_courses)
        self.session.commit()

    def add_groups(self):
        groups = self.generate_person.groups
        list_groups = [models.Group(name=group) for group in groups]
        self.session.add_all(list_groups)
        self.session.commit()

    def add_students(self, amount):
        students = [self.create_new_student(**self.generate_person()) for _ in range(amount)]
        self.session.add_all(students)
        self.session.commit()


if __name__ == '__main__':  # pragma: no cover
    database = create_temp_connection()
