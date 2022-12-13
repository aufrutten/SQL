import os

from flask import Flask
from flask_restful import Api

import SQL
import api
from views import simple_page


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        FLASK_DEBUG=True,
        instance_relative_config=True,
    )

    app.config['config_to_DATABASE'] = {'user': os.getenv('USER'),
                                        'password': 'pass',
                                        'host': 'localhost',
                                        'port': 5432,
                                        'path_db': 'main_database_test'}
    app.config['DATABASE'] = SQL.create_connection_postgresql(**app.config.get('config_to_DATABASE'))

    return app


app = create_app()
app.register_blueprint(simple_page)

api_of_app = Api(app)
api_of_app.add_resource(api.Student, '/api/student/<int:_id>', '/api/student/')
api_of_app.add_resource(api.StudentCourse, '/api/student/course/<int:_id>')
api_of_app.add_resource(api.Students, '/api/students/<int:page>')
api_of_app.add_resource(api.Course, '/api/course/<string:course>')
api_of_app.add_resource(api.Tools, '/api/tool/<string:command>')


if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
