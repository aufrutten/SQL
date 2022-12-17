import json
from random import choice


class TestStudent:

    def test_get(self, app, database, new_student):
        student = app.test_client().get(f'api/v1/students/{new_student["id"]}').json

        assert student['name'] == new_student['name']
        assert student['surname'] == new_student['surname']
        assert student['group'] == new_student['group']
        courses_student = list(map(str, student['courses']))
        for course in new_student['courses']:
            assert course in courses_student

    def test_get_with_index_error(self, app):
        student = app.test_client().get('/api/v1/students/99999999999999').json
        assert student['status_code'] == 404
        assert student['message'] == "student with id: 99999999999999 doesn't exist"

    def test_delete(self, app, database, new_student):
        content = app.test_client().delete(f'api/v1/students/{new_student["id"]}').json
        try:
            database.select_student(content['id'])

        except ValueError as exception:
            assert str(exception) == f"student with id: {new_student['id']} doesn't exist"

    def test_delete_with_error(self, app):
        student = app.test_client().delete('api/v1/students/12000000').json
        assert student['status_code'] == 404
        assert student['message'] == "student with id: 12000000 doesn't exist"

    def test_put(self, app, database, new_student):
        person = {
            'name': 'Hags',
            'surname': 'Hamburg',
            'group': str(choice(database.get_groups())),
            'courses': ['GO', 'Java']
        }
        content = app.test_client().put(f'api/v1/students/{new_student["id"]}', data=json.dumps(person)).json
        assert content['status_code'] == 200

        student = database.select_student(new_student["id"])
        courses_student = list(map(str, student.courses))

        assert student.name == person['name']
        assert student.surname == person['surname']
        assert database.get_name_group(student.group) == person['group']
        for course in person['courses']:
            assert course in courses_student

    def test_put_with_wrong_data(self, app, database, new_student):
        person = {
            'name': 'Hags',
            'surname': 'Hamburg',
            'group': str(choice(database.get_groups())),
            'courses': ['GO', 'TEST']
        }
        content = app.test_client().put(f'api/v1/students/{new_student["id"]}', data=json.dumps(person)).json
        assert content['status_code'] == 404
        assert content['message'] == "course TEST doesn't exist"


class TestStudentCourses:

    def test_put(self, app, database, new_student):
        courses = {'courses': ['Python', 'Swift']}
        content = app.test_client().put(f'/api/v1/students/{new_student["id"]}/courses', data=json.dumps(courses))
        assert content.json['status_code'] == 200

        student_courses = list(map(str, database.select_student(new_student['id']).courses))
        for course in courses['courses']:
            assert course in student_courses

    def test_put_with_wrong_course(self, app, new_student):
        courses = {'courses': ['SuperTest']}
        content = app.test_client().put(f'/api/v1/students/{new_student["id"]}/courses', data=json.dumps(courses))
        assert content.json['status_code'] == 404
        assert content.json['message'] == "course SuperTest doesn't exist"

    def test_delete(self, app, database, new_student):
        course = {'course': 'Python'}
        content = app.test_client().delete(f'/api/v1/students/{new_student["id"]}/courses', data=json.dumps(course))
        assert content.json['status_code'] == 200
        student = list(map(str, database.select_student(new_student['id']).courses))
        assert course['course'] not in student

    def test_delete_with_wrong_course(self, app, new_student):
        course = {'course': 'SuperTest'}
        content = app.test_client().delete(f'/api/v1/students/{new_student["id"]}/courses', data=json.dumps(course))
        assert content.json['status_code'] == 404
        assert content.json['message'] == "course SuperTest doesn't exist"


class TestStudents:

    def test_get(self, app, database):
        content = app.test_client().get('/api/v1/students?page=1').json
        assert len(content) == 30

    def test_get_without_page(self, app, database):
        content = app.test_client().get('/api/v1/students').json
        assert len(content) == 30

    def test_post(self, app, database, new_student):
        student = database.select_student(new_student['id'])

        assert student.name == new_student['name']
        assert student.surname == new_student['surname']
        assert database.get_name_group(student.group) in new_student['group']
        courses_student = list(map(str, student.courses))
        for course in new_student['courses']:
            assert course in courses_student

    def test_post_with_error(self, app, database):
        person = {'name': 'Test',
                  'surname': 'Test',
                  'group': 'DoubleTest',
                  'courses': 'Testing'}
        student_post = app.test_client().post('/api/v1/students', data=json.dumps(person)).json
        assert student_post['status_code'] == 404
        assert student_post['message'] == "group DoubleTest doesn't exist"


class TestCourse:

    def test_get(self, app, database):
        content = app.test_client().get('/api/v1/courses/Java').json
        key = choice(list(content.keys()))
        assert "Java" in content[key]['courses']

    def test_get_with_wrong_course(self, app, database):
        content = app.test_client().get('/api/v1/courses/JavaDEU').json
        assert content['status_code'] == 404
        assert content['message'] == "course JavaDEU doesn't exist"


class TestTools:

    def test_get(self, app, database):
        content = app.test_client().get('/api/v1/tools/find_less_group').json
        key = list(content)[0]
        assert isinstance(content[key], int)

    def test_get_with_wrong_text(self, app):
        content = app.test_client().get('/api/v1/tools/test_nothing').json
        assert content['status_code'] == 404
        assert content['message'] == 'command not found'
