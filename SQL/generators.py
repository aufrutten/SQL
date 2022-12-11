
__all__ = ['GeneratePerson', 'courses']

from random import choice, randint
import requests
from bs4 import BeautifulSoup as bs4_parser


courses = (
    ('Python', 'backend developing in python'),
    ('C++', 'developing games'),
    ('Query', 'frontend developing in Query'),
    ('JavaScript', 'frontend developing in JavaScript'),
    ('Swift', 'IOS developing in swift'),
    ('PHP', 'backend developing in PHP'),
    ('Java', 'android developing in Java'),
    ('WordPress', 'fullstack developing in WordPress'),
    ('GO', 'Go dev'),
    ('UI/UX', 'Ich weiß nicht was ich muss machen'),
    ('C#', 'Test Test Test'),
)


def get_random_courses():
    while True:
        amount_of_course = randint(1, 3)
        courses_index = [choice(courses)[0] for _ in range(amount_of_course)]
        yield courses_index


def gen_name_of_groups():
    letters = [chr(letter) for letter in range(65, 91)]
    numbers = [num for num in range(0, 10)]
    result = "{}{}_{}{}"
    while True:
        yield result.format(choice(letters), choice(letters), choice(numbers), choice(numbers))


def generate_groups(amount=100):
    name = gen_name_of_groups()
    return [next(name) for _ in range(amount)]


def get_content(url):
    r = requests.get(url)
    return bs4_parser(r.content, 'html.parser')


def gen_surname_of_student():
    url = 'https://nachnamen.net/deutschland'
    content = get_content(url)
    surnames = [con.findNext('a').text[1:] for con in content.find_all('li', class_='list-item col-lg-6 mb-1')]
    while True:
        yield choice(surnames)


def gen_name_of_student():
    url = 'https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_häufigsten_männlichen_Vornamen_Deutschlands'
    content = get_content(url)
    names = [con.find_next('a').text for con in content.find_all('li')][:-30]
    while True:
        yield choice(names)


class GeneratePerson:
    courses = get_random_courses()
    groups = generate_groups()
    names = gen_name_of_student()
    surnames = gen_surname_of_student()

    def __call__(self, *args, **kwargs):
        return {"name": next(self.names),
                "surname": next(self.surnames),
                "group": choice(self.groups),
                "courses": next(self.courses)}


if __name__ == '__main__':
    import time
    a = GeneratePerson()
    time_start = time.time()
    for _ in range(6 * 10**1):
        print(a())
    print(time.time() - time_start)

