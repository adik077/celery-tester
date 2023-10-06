from flask import Flask, render_template, request, flash, url_for, redirect
from celery import Celery
from pymongo.errors import ServerSelectionTimeoutError
from time import sleep

from db_config import connection
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['CELERY_BROKER_URL'] = os.environ['CELERY_BROKER_URL']
app.config['CELERY_RESULT_BACKEND'] = os.environ['CELERY_RESULT_BACKEND']

celery = Celery('worker', broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)


@app.route("/", methods=['GET', 'POST'])
def fill_form():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        if not name or not email or not message:
            flash("Empty fields...", "error")
            return redirect(url_for('fill_form'))
        try:
            parallel_task.delay()
            save_to_db(name, email, message)
        except ServerSelectionTimeoutError:
            flash("Cannot connect to the server...", "error")
            return redirect(url_for('fill_form'))
        flash("Your data was saved successfully...", "success")
        return redirect(url_for('fill_form'))
    else:
        return render_template('main_form.html')


@celery.task
def parallel_task():
    sleep(10)


def save_to_db(name, email, message):
    db = connection()
    db.insert_one({'name': name, 'email': email, 'message': message})


if __name__ == '__main__':
    app.run(debug=True)
