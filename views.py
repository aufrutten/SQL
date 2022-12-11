from flask import current_app, Blueprint, render_template, request


simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates',
                        )


@simple_page.route('/students.html/')
@simple_page.route('/')
def student_page():
    page = int(request.values.get('page')) if request.values.get('page') else 0
    database = current_app.config.get('DATABASE')
    try:
        student_list = database.get_students(count_in_the_page=20)[page]
    except IndexError:
        return render_template('404.html')
    else:
        students = database.get_dict_students_from_list(student_list)
        return render_template('students.html', students=students, page=page)