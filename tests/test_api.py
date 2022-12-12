import json

import pytest

from main import app
from random import choice

database = app.config.get('DATABASE')


class TestStudent:

    def test_get(self):
        person = {
            'name': 'Olaf',
            'surname': 'Schwarz',
            'group': str(choice(database.get_groups())),
            'courses': ['Python', 'C++']
        }
        student_post = app.test_client().post('api/student/', data=json.dumps(person))

        student = json.loads(app.test_client().get(f'api/student/{json.loads(student_post.json)["id"]}').json)
        assert student['name'] == person['name']
        assert student['surname'] == person['surname']
        assert student['group'] == person['group']
        courses_student = list(map(str, student['courses']))
        for course in person['courses']:
            assert course in courses_student

    def test_delete(self):

        person = {
            'name': 'Olaf',
            'surname': 'Schwarz',
            'group': str(choice(database.get_groups())),
            'courses': ['Python', 'C++']
        }
        student = app.test_client().post('api/student/', data=json.dumps(person))

        content = app.test_client().delete(f'api/student/{json.loads(student.json)["id"]}')
        with pytest.raises(ValueError):
            database.select_student(json.loads(content.json)['id'])

    def test_post(self):
        person = {
            'name': 'Olaf',
            'surname': 'Schwarz',
            'group': str(choice(database.get_groups())),
            'courses': ['Python', 'C++']
        }
        content = app.test_client().post('api/student/', data=json.dumps(person))
        assert json.loads(content.json)['status_code'] == 200
        student = database.select_student(json.loads(content.json)['id'])
        assert student.name == person['name']
        assert student.surname == person['surname']
        assert database.get_name_group(student.group) in person['group']
        courses_student = list(map(str, student.courses))
        for course in person['courses']:
            assert course in courses_student

    def test_patch(self):
        new_person = database.insert_student(name='test0', surname='test1',
                                             group=str(choice(database.get_groups())),
                                             courses=['Swift', 'Java'],)
        person = {
            'name': 'Test',
            'surname': 'Hamburg',
            'group': str(choice(database.get_groups())),
            'courses': ['Python', 'C++']
        }
        content = app.test_client().patch(f'api/student/{new_person.id}', data=json.dumps(person))
        assert json.loads(content.json)['status_code'] == 200

        student = database.select_student(new_person.id)
        assert student.name == person['name']
        assert student.surname == person['surname']
        assert database.get_name_group(student.group) == person['group']
        courses_student = list(map(str, student.courses))
        for course in person['courses']:
            assert course in courses_student
        database.delete_student(student.id)


class TestStudentCourses:

    def test_patch(self):
        _id = 20
        courses = {'courses': ['Python', 'Swift']}
        content = app.test_client().patch(f'/api/student/course/{_id}', data=json.dumps(courses))
        assert json.loads(content.json)['status_code'] == 200
        student = list(map(str, database.select_student(_id).courses))
        for course in courses['courses']:
            assert course in student

    def test_delete(self):
        _id = 20
        course = {'course': 'Python'}
        content = app.test_client().delete(f'/api/student/course/{_id}', data=json.dumps(course))
        assert json.loads(content.json)['status_code'] == 200
        student = list(map(str, database.select_student(_id).courses))
        assert course['course'] not in student


class TestStudents:

    def test_get(self):
        content = app.test_client().get('api/students/1')
        print(content.json)


class TestCourse:

    def test_get(self):
        content = app.test_client().get('api/course/Java')
        print(content.json)


class TestTools:

    def test_get(self):
        content = app.test_client().get('/tool/find_less_group')
        print(content.json)
