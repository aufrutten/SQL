from bs4 import BeautifulSoup as parser_bs
import re


class TestStudents:

    def test_main_case(self, app):
        response = app.test_client().get('/students/')
        content = parser_bs(response.text, 'html.parser')
        assert response.status_code == 200
        assert len(content.find_all('tr')) == 31

    def test_wrong_case(self, app):
        response = app.test_client().get('/students/?page=90000000000000000')
        content = parser_bs(response.text, 'html.parser')
        assert response.status_code == 200
        assert ' '.join(content.text.split()) == 'Error Error 404 list index out of range'


class TestCourse:

    def test_main_case(self, app):
        response = app.test_client().get('/course/Python')
        content = parser_bs(response.text, 'html.parser')
        result = [bool(re.search('Python', course.text)) for course in content.find_all('th', class_='courses')]
        assert all(result) is True

    def test_wrong_case(self, app):
        response = app.test_client().get('/course/Test')
        content = parser_bs(response.text, 'html.parser')
        assert response.status_code == 200
        assert ' '.join(content.text.split()) == "Error Error 404 course Test doesn't exist"
