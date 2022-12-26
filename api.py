
__all__ = ('api_v1',)

import json

from flask import request
from flask_restful import Resource, current_app, Api


class Student(Resource):
    """get/update/delete student"""

    def get(self, _id: int) -> dict:
        """
        get student by id
        ---
        parameters:
            - name: _id
              in: path
              required: true
              schema:
                format: int

        responses:
            '200':    # status code
              description: A JSON of student
            '404':
              description: status_code, message_error
        """
        database = current_app.config.get('DATABASE')
        try:
            student = database.select_student(abs(int(_id))).dict
            student['group'] = str(database.get_name_group(student.get('group')))

        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}

        else:
            return student

    def delete(self, _id: int) -> dict:
        """
        delete student by id
        ---
        parameters:
            - name: _id
              in: path
              required: true
              schema:
                format: int

        responses:
            '200':    # status code
              description: A JSON status of student
            '404':
              description: status_code, message_error
        """
        database = current_app.config.get('DATABASE')
        try:
            database.delete_student(abs(int(_id)))

        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}

        else:
            return {'status_code': 200, 'message': f'user {_id} has been deleted', 'id': _id}

    def put(self, _id) -> dict:
        """
        update student by id
        ---
        parameters:
            - name: _id
              in: path
              required: true
              schema:
                format: int
            - name: body
              in: body
              required: true
              schema:
                  id: Student
                  required:
                    - name
                    - surname
                    - group
                    - courses

                  properties:
                    name:
                      type: string
                      default: "testName"

                    surname:
                      type: string
                      default: "testSurname"

                    group:
                      type: string
                      default: "SS-20"

                    courses:
                      type: array
                      default: ["Python", "C++"]
        responses:
            '200':    # status code
              description: A JSON status of student
            '404':
              description: status_code, message_error
        """
        database = current_app.config.get('DATABASE')
        try:
            student = json.loads(request.data)
            database.update_student(_id, **student)

        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}

        else:
            return {'status_code': 200, 'message': f'user {_id} has been updated'}


class Students(Resource):

    def get(self) -> dict:
        """
        get dict of students, default page=0, or api/students?page=X
        ---
        parameters:
            - name: page
              in: query
              format: inter
              required: false

        responses:
            '200':    # status code
              description: A JSON status of student
            '404':
              description: status_code, message_error
        """
        database = current_app.config.get('DATABASE')
        page = int(request.values.get('page')) if request.values.get('page') else 0
        list_students = database.get_students()[page]
        students = database.get_dict_students_from_list(list_students)
        return students

    def post(self) -> dict:
        """
        insert student in database
        ---
        parameters:
            - name: body
              in: body
              required: true
              schema:
                  id: Student
                  required:
                    - name
                    - surname
                    - group
                    - courses

                  properties:
                    name:
                      type: string
                      default: "testName"

                    surname:
                      type: string
                      default: "testSurname"

                    group:
                      type: string
                      default: "SS-20"

                    courses:
                      type: array
                      default: ["Python", "C++"]
        responses:
            '200':    # status code
              description: A JSON status of student
            '404':
              description: status_code, message_error
        """
        database = current_app.config.get('DATABASE')
        try:
            student = json.loads(request.data)
            student_model = database.insert_student(**student)

        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}

        else:
            return {'status_code': 200,
                    'message': f'student {student_model.id} has been added',
                    'id': student_model.id}


class StudentCourses(Resource):
    """
    api for adding or removing student from course
    """

    def put(self, _id: int) -> dict:
        """
        api for adding courses to student
        ---
        parameters:
            - name: _id
              in: path
              required: true
              schema:
                format: int
            - name: body
              in: body
              required: true
              schema:
                  id: Courses
                  required:
                    - courses

                  properties:
                    courses:
                      type: array
                      default: ["Python", "C++"]
        responses:
            '200':    # status code
              description: A JSON status of student
            '404':
              description: status_code, message_error
        """
        database = current_app.config.get('DATABASE')

        try:
            courses = json.loads(request.data)['courses']
            student = database.add_student_to_courses(_id, list(courses))
        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}
        else:
            return {'status_code': 200,
                    'message': f'user {_id} has been updated, courses:{student.courses}'}

    def delete(self, _id: int) -> dict:
        """
        api for removing course of student
        ---
        parameters:
            - name: _id
              in: path
              required: true
              schema:
                format: int
            - name: body
              in: body
              required: true
              schema:
                  id: Course
                  required:
                    - course

                  properties:
                    course:
                      type: string
                      default: "Python"
        responses:
            '200':    # status code
              description: A JSON status of student
            '404':
              description: status_code, message_error
        """
        database = current_app.config.get('DATABASE')

        try:
            course = json.loads(request.data)['course']
            student = database.remove_student_from_course(_id, str(course))
        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}
        else:
            return {'status_code': 200,
                    'message': f'user {_id} has been updated, courses:{student.courses}'}


class Courses(Resource):

    def get(self, course: str) -> dict:
        """
        class for getting students from the course
        ---
        parameters:
            - name: course
              in: path
              required: true
              schema:
                format: string

        responses:
            '200':    # status code
              description: A JSON status of student
            '404':
              description: status_code, message_error
        """
        database = current_app.config.get('DATABASE')
        try:
            list_students = database.get_students_by_course(course)
        except ValueError as exception:
            return {'status_code': 404, 'message': str(exception)}
        else:
            students = database.get_dict_students_from_list(list_students)
            return students


class Tools(Resource):

    def get(self, command: str) -> dict:
        """
        getting result command;
        ---
        parameters:
            - name: command
              in: path
              required: true
              enum: ['find_less_group']
              schema:
                format: string


        responses:
            '200':    # status code
              description: A JSON status of student
            '404':
              description: status_code, message_error
        """
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
