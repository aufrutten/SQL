import json

from main import app
from random import choice


class TestStudent:

    def test_get(self):
        content = app.test_client().get('/student/5')
        print(content.json)

    def test_delete(self):
        content = app.test_client().delete('/student/1')
        print(content.json)

    def test_put(self):
        database = app.config.get('DATABASE')
        person = {
            'name': 'Olaf',
            'surname': 'Schwarz',
            'group': str(choice(database.get_groups())),
            'courses': ['Python', 'C++']
        }
        content = app.test_client().put('/student/', data=json.dumps(person))
        print(content.json)

    def test_patch(self):
        database = app.config.get('DATABASE')
        person = {
            'name': 'Test',
            'surname': 'Hamburg',
            'group': str(choice(database.get_groups())),
            'courses': ['Python', 'C++']
        }
        content = app.test_client().patch('/student/10', data=json.dumps(person))
        print(content.json)


class TestStudents:

    def test_get(self):
        content = app.test_client().get('/students/1')
        print(content.json)


class TestCourse:

    def test_get(self):
        content = app.test_client().get('/course/Java')
        print(content.json)


class TestTools:

    def test_get(self):
        content = app.test_client().get('/tool/find_less_group')
        print(content.json)
