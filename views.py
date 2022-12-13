from flask import current_app, Blueprint, render_template, request


simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates',
                        )


@simple_page.route('/students/')
@simple_page.route('/')
def student_page():
    page = int(request.values.get('page')) if request.values.get('page') else 0
    database = current_app.config.get('DATABASE')
    try:
        student_list = database.get_students()[page]
    except IndexError as exception:
        return render_template('404.html', message=str(exception))
    else:
        students = database.get_dict_students_from_list(student_list)
        return render_template('students.html', students=students, page=page)


@simple_page.route('/course/<string:course>')
def course_page(course):
    database = current_app.config.get('DATABASE')
    try:
        student_list = database.get_students_by_course(course)

    except ValueError as exception:
        return render_template('404.html', message=str(exception))

    else:
        students = database.get_dict_students_from_list(student_list)
        return render_template('students.html', students=students, page=0)

