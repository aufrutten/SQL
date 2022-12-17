import json
from random import choice
import pytest
from SQL import create_temp_connection
from main import create_app

app_flask = create_app()
app_flask.config['DATABASE'] = create_temp_connection()


@pytest.fixture
def app():
    return app_flask


@pytest.fixture
def database():
    return app_flask.config.get('DATABASE')


@pytest.fixture
def new_student():
    student = {
        'name': 'TestName',
        'surname': 'TestSurname',
        'group': str(choice(app_flask.config.get('DATABASE').get_groups())),
        'courses': ['Python', 'C++'],
    }
    student_post = app_flask.test_client().post('/api/v1/students', data=json.dumps(student))
    student['id'] = student_post.json['id']
    return student
