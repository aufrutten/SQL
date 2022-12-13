import json
from random import choice

from main import app


class TestStudent:

    def test_get(self, database, new_student):
        student = json.loads(app.test_client().get(f'api/student/{new_student["id"]}').json)

        assert student['name'] == new_student['name']
        assert student['surname'] == new_student['surname']
        assert student['group'] == new_student['group']
        courses_student = list(map(str, student['courses']))
        for course in new_student['courses']:
            assert course in courses_student

    def test_get_with_index_error(self):
        student = app.test_client().get('/api/student/99999999999999')
        assert json.loads(student.json)['status_code'] == 404
        assert json.loads(student.json)['message'] == "student with id: 99999999999999 doesn't exist"

    def test_delete(self, database, new_student):
        content = app.test_client().delete(f'api/student/{new_student["id"]}')
        try:
            database.select_student(json.loads(content.json)['id'])

        except ValueError as exception:
            assert str(exception) == f"student with id: {new_student['id']} doesn't exist"

    def test_delete_with_error(self):
        student = app.test_client().delete('api/student/12000000').json
        assert json.loads(student)['status_code'] == 404
        assert json.loads(student)['message'] == "student with id: 12000000 doesn't exist"

    def test_post(self, database, new_student):
        student = database.select_student(new_student['id'])

        assert student.name == new_student['name']
        assert student.surname == new_student['surname']
        assert database.get_name_group(student.group) in new_student['group']
        courses_student = list(map(str, student.courses))
        for course in new_student['courses']:
            assert course in courses_student

    def test_post_with_error(self, database):
        person = {'name': 'Test',
                  'surname': 'Test',
                  'group': 'DoubleTest',
                  'courses': 'Testing'}
        student_post = app.test_client().post('/api/student/', data=json.dumps(person)).json

        assert json.loads(student_post)['status_code'] == 404
        assert json.loads(student_post)['message'] == "group DoubleTest doesn't exist"

    def test_patch(self, database, new_student):
        person = {
            'name': 'Hags',
            'surname': 'Hamburg',
            'group': str(choice(database.get_groups())),
            'courses': ['GO', 'Java']
        }
        content = app.test_client().patch(f'api/student/{new_student["id"]}', data=json.dumps(person))
        assert json.loads(content.json)['status_code'] == 200

        student = database.select_student(new_student["id"])
        courses_student = list(map(str, student.courses))

        assert student.name == person['name']
        assert student.surname == person['surname']
        assert database.get_name_group(student.group) == person['group']
        for course in person['courses']:
            assert course in courses_student

    def test_patch_with_wrong_data(self, database, new_student):
        person = {
            'name': 'Hags',
            'surname': 'Hamburg',
            'group': str(choice(database.get_groups())),
            'courses': ['GO', 'TEST']
        }
        content = app.test_client().patch(f'api/student/{new_student["id"]}', data=json.dumps(person))
        assert json.loads(content.json)['status_code'] == 404
        assert json.loads(content.json)['message'] == "course TEST doesn't exist"


class TestStudentCourses:

    def test_patch(self, database, new_student):
        courses = {'courses': ['Python', 'Swift']}
        content = app.test_client().patch(f'/api/student/course/{new_student["id"]}', data=json.dumps(courses))
        assert json.loads(content.json)['status_code'] == 200

        student_courses = list(map(str, database.select_student(new_student['id']).courses))
        for course in courses['courses']:
            assert course in student_courses

    def test_patch_with_wrong_course(self, new_student):
        courses = {'courses': ['SuperTest']}
        content = app.test_client().patch(f'/api/student/course/{new_student["id"]}', data=json.dumps(courses)).json
        assert json.loads(content)['status_code'] == 404
        assert json.loads(content)['message'] == "course SuperTest doesn't exist"

    def test_delete(self, database, new_student):
        course = {'course': 'Python'}
        content = app.test_client().delete(f'/api/student/course/{new_student["id"]}', data=json.dumps(course))
        assert json.loads(content.json)['status_code'] == 200
        student = list(map(str, database.select_student(new_student['id']).courses))
        assert course['course'] not in student

    def test_delete_with_wrong_course(self, new_student):
        course = {'course': 'SuperTest'}
        content = app.test_client().delete(f'/api/student/course/{new_student["id"]}', data=json.dumps(course))
        assert json.loads(content.json)['status_code'] == 404
        assert json.loads(content.json)['message'] == "course SuperTest doesn't exist"


class TestStudents:

    def test_get(self, database):
        content = app.test_client().get('/api/students/1')
        assert len(json.loads(content.json)) == 30


class TestCourse:

    def test_get(self, database):
        content = app.test_client().get('/api/course/Java').json
        course = json.loads(content)
        key = choice(list(course.keys()))
        assert "Java" in course[key]['courses']

    def test_get_with_wrong_course(self, database):
        content = app.test_client().get('/api/course/JavaDEU').json
        response = json.loads(content)
        assert response['status_code'] == 404
        assert response['message'] == "course JavaDEU doesn't exist"


class TestTools:

    def test_get(self, database):
        content = json.loads(app.test_client().get('/api/tool/find_less_group').json)
        key = list(content)[0]
        assert isinstance(content[key], int)

    def test_get_with_wrong_text(self):
        content = json.loads(app.test_client().get('/api/tool/test_nothing').json)
        assert content['status_code'] == 404
        assert content['message'] == 'command not found'
