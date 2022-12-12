from flask import request
from flask_restful import Resource, current_app
import json


class Student(Resource):

    def get(self, _id):
        database = current_app.config.get('DATABASE')
        try:
            student = database.select_student(_id)

        except ValueError as exception:
            return json.dumps({'status_code': 404, 'message': str(exception)})

        else:
            return json.dumps({'name': str(student.name),
                               'surname': str(student.surname),
                               'group': str(database.get_name_group(student.group)),
                               'courses': list(map(str, student.courses))
                               })

    def post(self):
        database = current_app.config.get('DATABASE')
        student = json.loads(request.data)
        try:
            student_model = database.insert_student(**student)

        except ValueError as exception:
            return json.dumps({'status_code': 404, 'message': str(exception)})

        else:
            return json.dumps({'status_code': 200, 'message': f'student {student_model.id} has been added',
                               'id': student_model.id})

    def delete(self, _id):
        database = current_app.config.get('DATABASE')
        try:
            database.delete_student(_id)

        except ValueError as exception:
            return json.dumps({'status_code': 404, 'message': str(exception)})

        else:
            return json.dumps({'status_code': 200, 'message': f'user {_id} has been deleted', 'id': _id})

    def patch(self, _id):
        database = current_app.config.get('DATABASE')
        student = json.loads(request.data)
        try:
            database.update_student(_id, **student)

        except ValueError as exception:
            return json.dumps({'status_code': 404, 'message': str(exception)})

        else:
            return json.dumps({'status_code': 200, 'message': f'user {_id} has been updated'})


class StudentCourse(Resource):

    def patch(self, _id):
        database = current_app.config.get('DATABASE')
        courses = json.loads(request.data)['courses']

        try:
            student = database.add_student_by_id_to_courses(_id, list(courses))
        except IndexError as exception:
            return json.dumps({'status_code': 404, 'message': str(exception)})
        else:
            return json.dumps({'status_code': 200,
                               'message': f'user {_id} has been updated, courses:{student.courses}'})

    def delete(self, _id):
        database = current_app.config.get('DATABASE')
        course = json.loads(request.data)['course']

        try:
            student = database.remove_student_from_course(_id, str(course))
            print(student)
        except IndexError as exception:
            return json.dumps({'status_code': 404, 'message': str(exception)})
        else:
            return json.dumps({'status_code': 200,
                               'message': f'user {_id} has been updated, courses:{student.courses}'})


class Students(Resource):

    def get(self, page):
        database = current_app.config.get('DATABASE')
        try:
            list_students = database.get_students(count_in_the_page=20)[page-1]
        except IndexError as exception:
            return json.dumps({'status_code': 404, 'message': str(exception)})
        else:
            students = database.get_dict_students_from_list(list_students)
            return json.dumps(students)


class Course(Resource):

    def get(self, course):
        database = current_app.config.get('DATABASE')
        try:
            list_students = database.get_students_by_course(course)
        except ValueError as exception:
            return json.dumps({'status_code': 404, 'message': str(exception)})
        else:
            students = database.get_dict_students_from_list(list_students)
            return json.dumps(students)


class Tools(Resource):

    def get(self, command):
        database = current_app.config.get('DATABASE')
        if command == 'find_less_group':
            return json.dumps(database.find_less_group())
        else:
            return json.dumps({'status_code': 404, 'message': 'command not found'})


if __name__ == '__main__':
    pass
