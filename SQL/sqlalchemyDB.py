import os

from sqlalchemy.engine import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

import models
from generators import GeneratePerson, get_courses

postgresql = {  # test keys
    'user': os.getenv('USER'),
    'password': 'pass',
    'host': 'localhost',
    'port': 5432,
    'path_db': 'testd1b'
}


class SQL:

    def __init__(self, user, password, host, port, path_db):
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{path_db}"
        # url = "postgresql+psycopg2://ihorsemykopenko:password@localhost:5432/test"

        if not database_exists(url):
            create_database(url)
            models.Base.metadata.create_all(bind=create_engine(url))

        self.engine = create_engine(url, echo=False, future=True)
        self.session = sessionmaker(bind=self.engine)()

    def get_all_records(self):
        for i in self.session.query(models.Student).all():
            print(i)

        for i in self.session.query(models.Group).all():
            print(i)

        for i in self.session.query(models.Course).all():
            print(i)

    def find_less_group(self):
        pass

    def add_new_student(self, name, surname, group, courses):
        # TODO: complete the function 'adding'
        # right here i have been stop

        print(name, surname, group, courses)
        group_id = self.session.query(models.Group).where(models.Group.name == group).first()
        print(group_id)
        self.session.add(models.Student(name=name, surname=surname,))
        self.session.commit()

    def delete_student_by_id(self, _id: int):
        pass

    def add_new_student_by_id_to_courses(self, _id: int, courses: list):
        pass

    def remove_student_from_course(self, _id: int, course: str):
        pass


class CreateRecords(SQL):
    """Class use for writing new randomly records"""

    def __init__(self, user, password, host, port, path_db):
        super().__init__(user, password, host, port, path_db)

        self.generate_person = GeneratePerson()

        self.add_groups()
        self.add_courses()
        self.add_persons()

    def add_courses(self):
        courses = get_courses()
        list_courses = [models.Course(course_name=course, description=description) for course, description in courses]
        self.session.add_all(list_courses)
        self.session.commit()

    def add_groups(self):
        groups = self.generate_person.groups
        list_groups = [models.Group(name=group) for group in groups]
        self.session.add_all(list_groups)
        self.session.commit()

    def add_persons(self, amount=1):
        pass


if __name__ == '__main__':
    # CreateRecords(**postgresql)
    database = SQL(**postgresql)
    # database.add_new_student('Olaf', 'John', 'EU_20', ['Python'])
    # database.add_new_student('Olaf', 'John', 'EU_20', ['Python'])
    # database.add_new_student('Olaf', 'John', 'EU_20', ['Python'])
    # database.add_new_student('Olaf', 'John', 'EU_20', ['Python'])
    database.add_new_student('Olaf', 'John', 'QW_77', ['Python'])
    database.get_all_records()
#
