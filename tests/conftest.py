import json
from random import choice
import pytest
from SQL import create_temp_connection
from main import app

app.config['DATABASE'] = create_temp_connection()


@pytest.fixture
def database():
    return app.config.get('DATABASE')


@pytest.fixture
def new_student():
    student = {
        'name': 'TestName',
        'surname': 'TestSurname',
        'group': str(choice(app.config.get('DATABASE').get_groups())),
        'courses': ['Python', 'C++'],
    }
    student_post = app.test_client().post('/api/student/', data=json.dumps(student))
    student['id'] = json.loads(student_post.json)['id']
    return student
