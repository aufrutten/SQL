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
                                        'path_db': 'other'}
    app.config['DATABASE'] = SQL.SQL(**app.config.get('config_to_DATABASE'))

    database = app.config.get('DATABASE')
    courses, groups, students = len(database.get_courses()), len(database.get_groups()), len(database.get_students())

    if courses == 0 and groups == 0 and students == 0:  # if database is empty
        SQL.CreateRecords(**app.config.get('config_to_DATABASE'), amount_of_students=2*10**5)
    return app


app = create_app()
app.register_blueprint(simple_page)

api_of_app = Api(app)
api_of_app.add_resource(api.Student, '/student/<int:_id>', '/student/')
api_of_app.add_resource(api.Students, '/students/<int:page>')
api_of_app.add_resource(api.Course, '/course/<string:course>')
api_of_app.add_resource(api.Tools, '/tool/<string:command>')


if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True)
