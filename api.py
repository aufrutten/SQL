
__all__ = ('api_v1',)

from flask import request
from flask_restful import Resource, current_app, Api
import json


class Student(Resource):
    """get/update/delete student"""

    def get(self, _id):
        """get student"""
        database = current_app.config.get('DATABASE')
        try:
            student = database.select_student(abs(int(_id))).dict
            student['group'] = str(database.get_name_group(student.get('group')))

        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}

        else:
            return student

    def delete(self, _id):
        """delete student"""
        database = current_app.config.get('DATABASE')
        try:
            database.delete_student(abs(int(_id)))

        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}

        else:
            return {'status_code': 200, 'message': f'user {_id} has been deleted', 'id': _id}

    def put(self, _id):
        """update student"""
        database = current_app.config.get('DATABASE')
        student = json.loads(request.data)
        try:
            database.update_student(_id, **student)

        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}

        else:
            return {'status_code': 200, 'message': f'user {_id} has been updated'}


class Students(Resource):

    def get(self):
        """get dict of students, default page=0, or api/students?page=X"""
        database = current_app.config.get('DATABASE')
        page = int(request.values.get('page')) if request.values.get('page') else 0
        list_students = database.get_students()[page]
        students = database.get_dict_students_from_list(list_students)
        return students

    def post(self):
        """insert student in database"""
        database = current_app.config.get('DATABASE')
        student = json.loads(request.data)
        try:
            student_model = database.insert_student(**student)

        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}

        else:
            return {'status_code': 200,
                    'message': f'student {student_model.id} has been added',
                    'id': student_model.id}


class StudentCourses(Resource):
    """api for adding or removing student from course"""

    def put(self, _id):
        database = current_app.config.get('DATABASE')
        courses = json.loads(request.data)['courses']

        try:
            student = database.add_student_to_courses(_id, list(courses))
        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}
        else:
            return {'status_code': 200,
                    'message': f'user {_id} has been updated, courses:{student.courses}'}

    def delete(self, _id):
        database = current_app.config.get('DATABASE')
        course = json.loads(request.data)['course']

        try:
            student = database.remove_student_from_course(_id, str(course))
        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}
        else:
            return {'status_code': 200,
                    'message': f'user {_id} has been updated, courses:{student.courses}'}


class Courses(Resource):
    """class for getting student from the course"""

    def get(self, course):
        database = current_app.config.get('DATABASE')
        try:
            list_students = database.get_students_by_course(course)
        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}
        else:
            students = database.get_dict_students_from_list(list_students)
            return students


class Tools(Resource):

    def get(self, command):
        database = current_app.config.get('DATABASE')
        if command == 'find_less_group':
            return database.find_less_group()
        else:
            return {'status_code': 404, 'message': 'command not found'}


def api_v1(app):
    api_instance = Api(app, prefix='/api/v1')

    api_instance.add_resource(Students, '/students')  # post student, get students
    api_instance.add_resource(Student, '/students/<int:_id>')  # get student, update, delete
    api_instance.add_resource(StudentCourses, '/students/<int:_id>/courses')  # for adding and rm courses to student

    api_instance.add_resource(Courses, '/courses/<string:course>')

    api_instance.add_resource(Tools, '/tools/<string:command>')


if __name__ == '__main__':  # pragma: no cover
    pass
