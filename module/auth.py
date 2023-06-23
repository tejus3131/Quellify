from flask import Blueprint, session, url_for, redirect, render_template, flash, request, jsonify
from . import users, unique_identifier, admins
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

master="admin@quellify.com"

def login_required(func):
    def check_login(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login to access this page', 'danger')
            return redirect(url_for('views.home'))
        return func(*args, **kwargs)
    check_login.__name__ = func.__name__
    return check_login

def master_required():
    def check_master(func):
        def check_login(*args, **kwargs):
            if 'logged_in' not in session:
                flash('please login to use these commands', 'danger')
                return redirect(url_for('views.home'))
            elif 'admin' not in session:
                flash('Only admin can use these commands', 'danger')
                return redirect(url_for('views.home'))
            elif session[unique_identifier] != master:
                flash("Only owner can use these commands", "danger")
                return redirect(url_for('views.home'))
            return func(*args, **kwargs)
        check_login.__name__ = func.__name__
        return check_login
    return check_master


def admin_required():
    def check_admin(func):
        def check_login(*args, **kwargs):
            if 'logged_in' not in session:
                flash('Please login as a administrator to access admin pages', 'danger')
                return redirect(url_for('views.home'))
            if not session['admin']:
                flash('Only admins can access admin pages', 'danger')
                print(session['email'])
                print(admins)
                return redirect(url_for('views.home'))
            return func(*args, **kwargs)
        check_login.__name__ = func.__name__
        return check_login
    return check_admin

@auth.route('/')
def checkAuth():
    if 'logged_in' in session:
        return redirect(url_for('auth.logout'))
    return render_template('userAuth.html')


@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('loginEmail')
    password = request.form.get('loginPassword')
    user = users.find_one({unique_identifier: email})
    if user:
        if check_password_hash(user['password'], password):
            session['logged_in'] = True
            session[unique_identifier] = email
            if email in admins or user['admin'] == True:
                session['admin'] = True
            else:
                session['admin'] = user['admin']
            return jsonify({'message': 'success'})
        else:
            return jsonify({'message': 'Incorrect password'})
    else:
        return jsonify({'message': 'User does not exist'})


@auth.route('/register', methods=['POST'])
def register():
    email = request.form.get('registerEmail')
    password = request.form.get('registerPassword')
    confirm_password = request.form.get('registerRepeatPassword')

    if password != confirm_password:
        return jsonify({'message': 'Passwords do not match'})
    if users.find_one({unique_identifier: email}):
        return jsonify({'message': 'User already exists'})
    hashed_password = generate_password_hash(password, method='scrypt')
    admin = False
    if email in admins:
        admin = True
    users.insert_one({
        unique_identifier: email,
        'password': hashed_password,
        'courses': [],
        'admin':admin,
    })
    session['logged_in'] = True
    session[unique_identifier] = email
    session['admin'] = admin
    return jsonify({'message': 'success'})
@auth.route('/logout')


@login_required
def logout():
    session.clear()
    return redirect(url_for('views.home'))