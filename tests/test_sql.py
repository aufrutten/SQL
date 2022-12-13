import SQL
import os
from sqlalchemy_utils import database_exists


class TestSQL:

    def test_create_db(self):
        postgresql = {'user': os.getenv('USER'),
                      'password': 'pass',
                      'host': 'localhost',
                      'port': 5432,
                      'path_db': 'test_database'}
        database = SQL.create_connection_postgresql(**postgresql)
        url = database.url
        assert database_exists(url), 'database is not exist'

        assert len(database.get_courses())
        assert len(database.get_students())
        assert len(database.get_groups())

        database._drop_database()
        assert not database_exists(url), 'database still exist'

    def test_get_name_group_with_error(self, database):
        _id = 12312312341
        try:
            database.get_name_group(_id)
        except ValueError as exception:
            assert str(exception) == f"group with {_id} id doesn't exist"

    def test_print_models_student(self, database):
        student = database.select_student(3)
        text = "{0.id}:{0.name}:{0.surname}:{0.group}:{0.courses}".format(student)
        assert repr(student) == text
