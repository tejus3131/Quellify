from flask import Flask, redirect, render_template, url_for
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
import random
import string

admins = []
unique_identifier = "email"

ADMIN = "admin@quellify.com"
PASSWORD = "admin@quellify"
MONGO_URI = 'mongodb+srv://tejusgupta:tZvn1Apfs423uXnA@quellify.nngjgqq.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(MONGO_URI)
db = client['user_database']
users = db['users']
queries = db['queries']
courses = db['courses']


def create_admin():
    user = users.find_one({unique_identifier: ADMIN})
    if user:
        users.update_one({unique_identifier: ADMIN},
                         {'$set': {'admin': True}})
    else:
        users.insert_one({
            unique_identifier: ADMIN,
            'password': generate_password_hash(PASSWORD, method='scrypt'),
            'admin': True,
            'courses': []
        })


def website():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ''.join(random.choices(
        string.ascii_letters + string.digits, k=50))

    from .admin import admin
    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html")

    @app.errorhandler(403)
    def forbidden(e):
        return redirect(url_for('views.home'))

    @app.errorhandler(410)
    def gone(e):
        return redirect(url_for('views.home'))

    @app.errorhandler(400)
    def bad_request(e):
        return redirect(url_for('views.home'))

    create_admin()

    return app


__version__ = "0.0.1"
