
__all__ = ['SQL', 'CreateRecords']

import os
from functools import lru_cache

from sqlalchemy.engine import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

from . import models
from . import generators
# import models
# import generators


class SQLTools:

    def __init__(self, user, password, host, port, path_db):

        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{path_db}"

        if not database_exists(url):
            create_database(url)
            models.Base.metadata.create_all(bind=create_engine(url))

        self.engine = create_engine(url, echo=False, future=True)
        self.session = sessionmaker(bind=self.engine)()

    @lru_cache
    def get_course(self, course):
        """get instance course from the database"""
        course_db = self.session.query(models.Course).where(models.Course.course_name == course).first()
        if course_db:
            return course_db
        else:
            raise ValueError(f"course {course} doesn't exist")

    @lru_cache
    def get_id_group(self, group):
        """get id of group from the database"""
        group_db = self.session.query(models.Group).where(models.Group.name == group).first()
        if group_db:
            return group_db.id
        else:
            raise ValueError(f"group {group} doesn't exist")

    @lru_cache
    def get_name_group(self, _id):
        group_db = self.session.query(models.Group).where(models.Group.id == _id).first()
        if group_db:
            return group_db.name
        else:
            raise ValueError(f"group with {_id} id doesn't exist")

    def create_new_student(self, name, surname, group, courses):
        person = models.Student(name=name,
                                surname=surname,
                                group=self.get_id_group(group))
        person.courses += [self.get_course(course) for course in set(courses)]
        return person

    def get_groups(self):
        return self.session.query(models.Group).all()

    def get_courses(self):
        return self.session.query(models.Course).all()

    def get_students(self, count_in_the_page=3):
        students = self.session.query(models.Student).all()
        return [students[num:num + count_in_the_page] for num in range(0, len(students), count_in_the_page)]

    def get_dict_students_from_list(self, list_students):
        students = {student.id: {'name': str(student.name),
                                 'surname': str(student.surname),
                                 'group': str(self.get_name_group(student.group)),
                                 'courses': list(map(str, student.courses))
                                 } for student in list_students}
        return students


class SQL(SQLTools):

    def __init__(self, user, password, host, port, path_db):
        super().__init__(user, password, host, port, path_db)

    def insert_student(self, name, surname, group, courses):
        student = self.create_new_student(name, surname, group, courses)
        self.session.add(student)
        self.session.commit()
        return student

    def delete_student(self, _id: int):
        student = self.select_student(_id)
        self.session.delete(student)
        self.session.commit()
        return student

    def update_student(self, _id=None, name=None, surname=None, group=None, courses=[]):
        student = self.select_student(_id)

        student.name = name if name else student.name
        student.surname = surname if surname else student.surname
        student.group = self.get_id_group(group) if group else student.group
        student.courses = [self.get_course(course) for course in set(courses)] if courses else student.courses

        self.session.add(student)
        self.session.commit()
        return student

    def select_student(self, _id):
        student = self.session.query(models.Student).where(models.Student.id == _id).first()
        if student:
            return student
        else:
            raise ValueError(f"student with id: {_id} doesn't exist")

    def add_student_by_id_to_courses(self, _id: int, courses: list):
        student = self.select_student(_id)

        student_courses = [course.course_name for course in student.courses]
        courses = [self.get_course(course) for course in set(courses) if course not in student_courses]
        student.courses += courses

        self.session.add(student)
        self.session.commit()
        return student

    def remove_student_from_course(self, _id: int, course: str):
        student = self.select_student(_id)
        course_instance = self.get_course(course)
        for index, course in enumerate(student.courses):
            if course_instance == course:
                del student.courses[index]
                break
        self.session.add(student)
        self.session.commit()
        return student

    def get_students_by_course(self, course):
        course = self.get_course(course)
        students = [self.select_student(_id) for _id, _ in
                    self.session.query(models.student_course).filter_by(course_id=course.id).all()]
        return students

    def find_less_group(self):
        groups = {group.name: self.session.query(models.Student).filter_by(group=group.id).count()
                  for group in self.get_groups()}
        key = min(groups, key=groups.get)
        return {key: groups[key]}


class CreateRecords(SQLTools):
    """Class use for writing new randomly records"""

    def __init__(self, user, password, host, port, path_db, amount_of_students=2*10**5):
        super().__init__(user, password, host, port, path_db)

        self.generate_person = generators.GeneratePerson()

        self.add_groups()
        self.add_courses()
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
    postgresql = {'user': os.getenv('USER'),
                  'password': 'pass',
                  'host': 'localhost',
                  'port': 5432,
                  'path_db': 'test_database'}
    # import time
    # start_time = time.time()
    # CreateRecords(**postgresql, amount_of_students=1*10**3)
    # print(time.time() - start_time)

    database = SQL(**postgresql)
    for i in database.get_students():
        print(i)
    # print(database.get_students_by_course('C++'))
    # print(database.find_less_group())
    # database.insert_student('Ihor', 'Semy', 'ET_27', ['Python'])
    # print(database.get_groups())

    # print(database.remove_student_from_course(3, 'Python'))
    # print(database.select_student(3))
    # print(database.update_student(3, name='Ihor', surname='Semykopenko', group='UQ_26', courses=['Python']))
    # print(database.select_student(3))
    # print(database.find_less_group())

    # for i in database.get_students():
    #     print(list(map(str, i.courses)))

