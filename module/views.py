from flask import Blueprint, redirect, render_template, flash, url_for, session, request
from . import queries, unique_identifier, courses, users
from .auth import login_required

views = Blueprint('views', __name__)


@views.route('/')
def home():
    if 'logged_in' in session:
        if session['admin'] == True:
            return redirect(url_for('admin.admin_home'))
        course = courses.find({})
        user = users.find_one({unique_identifier: session[unique_identifier]})
        user_code = user['courses']
        all_course = []
        user_course = []
        for item in course:
            if item['course_code'] in user_code:
                user_course.append(item)
            else:
                all_course.append(item)
        return render_template('home.html', user=True, all_course=all_course, user_course=user_course)
    return render_template('index.html', user=False)


@views.route('/contactUs', methods=['POST'])
@login_required
def contactUs():
    email = session[unique_identifier]
    query = request.form.get('query')
    queries.insert_one({
        unique_identifier: email,
        'query': query,
    })
    flash('Your query has been submitted', 'success')
    return redirect(url_for('views.home'))


@views.route('/register_course/<string:code>', methods=['GET'])
@login_required
def registerCourse(code):
    user = users.find_one({unique_identifier: session[unique_identifier]})
    courses = user['courses']
    courses.append(code)
    users.update_one({unique_identifier: session[unique_identifier]}, {
                     '$set': {'courses': courses}})
    return redirect(url_for('views.home'))


@views.route('/remove_course/<string:code>', methods=['GET'])
@login_required
def removeCourse(code):
    user = users.find_one({unique_identifier: session[unique_identifier]})
    courses = user['courses']
    courses.remove(code)
    users.update_one({unique_identifier: session[unique_identifier]}, {
                     '$set': {'courses': courses}})
    return redirect(url_for('views.home'))


@views.route('/view_course/<string:code>', methods=['GET'])
@login_required
def viewCourse(code):
    course = courses.find_one({"course_code": code})
    return render_template('views.html', course=course, user=True)
