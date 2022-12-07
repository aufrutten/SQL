
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
import models
from generators import GeneratePerson, get_courses


class SQL:

    def __init__(self, url='sqlite:///test.db'):
        self.engine = create_engine(url, echo=True, future=True)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def find_less_group(self):
        pass

    def add_new_student(self, name, surname, group, courses):
        # TODO: complete the function 'adding'
        # right he i have been stop
        print(name, surname, group, courses)
        self.session.add(models.Student(name=name, surname=surname))
        self.session.commit()

    def delete_student_by_id(self, _id: int):
        pass

    def add_new_student_by_id_to_courses(self, _id: int, courses: list):
        pass

    def remove_student_from_course(self, _id: int, course: str):
        pass


class CreateDataBase(SQL):

    def __init__(self, url='sqlite:///test.db'):
        super().__init__(url)
        models.Base.metadata.create_all(bind=self.engine)

        self.generate_person = GeneratePerson()
        self.groups = self.generate_person.groups
        self.add_groups()

        self.add_courses()

    def add_courses(self):
        courses = get_courses()
        list_courses = [models.Course(course_name=course, description=description) for course, description in courses]
        self.session.add_all(list_courses)
        self.session.commit()

    def add_groups(self):
        list_groups = [models.Group(name=group) for group in self.groups]
        self.session.add_all(list_groups)
        self.session.commit()

    def add_persons(self, amount=1):
        pass


if __name__ == '__main__':
    # CreateDataBase()
    database = SQL()
    database.add_new_student('Olaf', 'John', 'EU_20', ['Python'])

