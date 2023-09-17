from flask import Flask, render_template, request, flash, url_for, redirect
from pymongo.errors import ServerSelectionTimeoutError

from db_config import connection
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.route("/", methods=['GET', 'POST'])
def fill_form():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        try:
            db = connection()
            db.insert_one({'name': name, 'email': email, 'message': message})
        except ServerSelectionTimeoutError:
            flash("Cannot connect to the server...", "error")
            return redirect(url_for('fill_form'))
        flash("Your data was saved successfully...", "success")
        return redirect(url_for('fill_form'))
    else:
        return render_template('main_form.html')


if __name__ == '__main__':
    app.run(debug=True)
