
__all__ = ('create_app',)

import os

from flask import Flask
from flasgger import Swagger

import SQL
from api import api_v1
from views import simple_page


def create_app():
    app = Flask(__name__)

    # <-----------SWAGGER-------------->
    app.config['swagger'] = Swagger(app)
    app.config['swagger'].load_swagger_file('templates/swagger.yaml')

    # <-----------INIT_APP------------->
    app.config.from_mapping(
        SECRET_KEY='dev',
        FLASK_DEBUG=True,
        instance_relative_config=True,
    )

    # <-----------DATABASE------------->
    app.config['config_to_DATABASE'] = {'user': os.getenv('USER'),
                                        'password': 'pass',
                                        'host': 'localhost',
                                        'port': 5432,
                                        'path_db': 'main_database_test1'}
    app.config['DATABASE'] = SQL.create_connection_postgresql(**app.config.get('config_to_DATABASE'))

    # <-----------VIEWS---------------->
    app.register_blueprint(simple_page)

    # <-----------APIs----------------->
    api_v1(app)

    return app


if __name__ == '__main__':  # pragma: no cover
    app_main = create_app()
    app_main.run(debug=True)
