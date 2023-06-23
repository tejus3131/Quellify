from flask import Blueprint, redirect, render_template, flash, url_for, session, request, jsonify
from . import users, queries, courses, unique_identifier, admins, create_admin
from .auth import admin_required, master_required, master
import random, string

admin = Blueprint('admin', __name__)

@admin.route('/')
@admin_required()
def admin_home():
    ismaster=False
    if session[unique_identifier]==master:
        ismaster=True
    user_data = users.find({})
    query_data = queries.find({})
    course_data = courses.find({})
    return render_template('admin.html', user_data=user_data, query_data=query_data, course_data=course_data, ismaster=ismaster, master=master)


@admin.route('/delete_user/<string:email>')
@master_required()
def delete_user(email):
    users.delete_one({unique_identifier: email})
    return redirect(url_for('admin.admin_home'))


@admin.route('/delete_query/<string:email>')
@admin_required()
def delete_query(email):
    queries.delete_one({unique_identifier: email})
    return redirect(url_for('admin.admin_home'))


@admin.route('/delete_course/<string:code>')
@admin_required()
def delete_course(code):
    all_user = users.find({})
    for user in all_user:
        course = user['courses']
        if code in course:
            course.remove(code)
            users.update_one({unique_identifier : user[unique_identifier]}, {'$set': {'courses': course}})
    courses.delete_one({"course_code": code})
    return redirect(url_for('admin.admin_home'))


@admin.route('/add_course/<string:code>', methods=['GET', 'POST'])
@admin_required()
def add_course(code):
    if request.method == "POST":
        course_name = request.form.get('name')
        course_description = request.form.get('desc')
        course_code = ''.join(random.choices(string.digits, k=5))
        course_creator = session[unique_identifier]
        print(course_code)
        if courses.find_one({"course_name":course_name}):
            return jsonify({'message':'Course name already exist.'})
        course_data = {
            'course_name': course_name,
            'course_description': course_description,
            'course_code': course_code,
            'course_step':"",
            'course_creator':course_creator
        }
        courses.insert_one(course_data)
        print(jsonify({'message':f'{course_code}'}))
        return jsonify({'message':'success', 'code':f'{course_code}'})
    course = courses.find_one({"course_code": code})
    course_name = course["course_name"]
    course_description = course["course_description"]
    course_step = course["course_step"]
    return render_template('add_step.html', name=course_name, desc=course_description, step=course_step, code=code)


@admin.route('/edit_course/<string:course_code>', methods=['POST'])
@admin_required()
def edit_course(course_code):
    course_name = request.form.get('name')
    course_description = request.form.get('desc')
    course_step = request.form.get('step')
    courses.update_one({"course_code": course_code}, {'$set': {
        'course_name': course_name,
        'course_description': course_description,
        'course_step':course_step
    }})
    return redirect(url_for('admin.admin_home'))


@admin.route('/add_admin/<string:email>')
@master_required()
def add_admin(email):
    user = users.find_one({unique_identifier: email})
    if user['admin']:
        flash('User is already an admin', 'danger')
        return redirect(url_for('admin.admin_home'))
    admins.append(email)
    users.update_one({unique_identifier: email}, {'$set': {'admin': True}})
    flash('User is now an admin', 'success')
    return redirect(url_for('admin.admin_home'))


@admin.route('/remove_admin/<string:email>')
@master_required()
def remove_admin(email):
    user = users.find_one({unique_identifier: email})
    if not user['admin']:
        flash('User is not an admin', 'danger')
        return redirect(url_for('admin.admin_home'))
    admins.remove(email)
    users.update_one({unique_identifier: email}, {'$set': {'admin': False}})
    flash('User is no longer an admin', 'success')
    return redirect(url_for('admin.admin_home'))


@admin.route('/delete_all_users')
@master_required()
def delete_all_users():
    users.delete_many({})
    create_admin()
    return redirect(url_for('admin.admin_home'))


@admin.route('/delete_all_queries')
@master_required()
def delete_all_queries():
    queries.delete_many({})
    return redirect(url_for('admin.admin_home'))

@admin.route('/delete_all_courses')
@master_required()
def delete_all_courses():
    courses.delete_many({})
    return redirect(url_for('admin.admin_home'))


@admin.route('/delete_all_admins')
@master_required()
def delete_all_admins():
    user = users.find({})
    for i in user:
        if i['admin']:
            users.update_one({unique_identifier: i[unique_identifier]}, {
                             '$set': {'admin': False}})
    admins.clear()
    create_admin()
    return redirect(url_for('admin.admin_home'))


@admin.route('/delete_all_data')
@master_required()
def delete_all_data():
    users.delete_many({})
    queries.delete_many({})
    courses.delete_many({})
    admins.clear()
    create_admin()
    return redirect(url_for('admin.admin_home'))
