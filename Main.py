from flask import Flask, request, redirect, session
from flask.templating import render_template
from DatabaseConnection import DatabaseConnection
import re

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

login_error_message = "Invalid username or password."
register_error_password_match = "Passwords do not match."
register_error_password_invalid = \
    "Password must respect format. (min 6 characters containing: upper, lower, special character)"
register_error_user_exists = "Username already exists."
db_text_placeholder = "Here will be your database extracted text."
administrator_name = "administrator"

@app.route('/')
@app.route('/index.html')
def index():
    if session.get('logged'):
        return redirect('/info')
    return app.send_static_file('index.html')

@app.route('/info', methods=['GET'])
def info():
    if not session.get('logged'):
        return redirect('/login')
    else:
        values = DatabaseConnection.get_instance().database.Values
        record = values.find_one({"id" : values.count()-1})
        humidity = record['humidity']
        temperature = record['temperature']
        pressure = record['pressure']

    return render_template('info.html',humidity=humidity,temperature=temperature,pressure=pressure)


@app.route('/login', methods=['GET', 'POST'])
def login_request():
    if session.get('logged'):
        return redirect('/info')
    if request.method == 'GET':
        return render_template('login.html', message="")
    else:
        username = request.form['username']
        password = request.form['password']
        users = DatabaseConnection.get_instance().database.Users
        record = users.find_one({"username" : username})
        if record is None:
            return render_template("login.html", message=login_error_message)
        else:
            if password == record['password']:
                session['logged'] = True
                session['userId'] = record['id']
                return redirect("info")
            else:
                return render_template("login.html", message=login_error_message)


@app.route('/register', methods=['GET', 'POST'])
def register_request():
    if session.get('logged'):
        return redirect('/info')
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        rpassword = request.form['rpassword']
        users = DatabaseConnection.get_instance().database.Users
        valid = False
        message = ""

        record = users.find_one({"username" : username})
        if record is not None:
            message = register_error_user_exists
        else:
            if password != rpassword:
                message = register_error_password_match
            else:
                passwordRegex = re.compile("[A-Za-z0-9@#$%^&+=!?.]{6,}")
                passwordMatch = passwordRegex.match(password)
                if passwordMatch != None and passwordMatch.end() == len(password) and passwordMatch.start() == 0:
                    valid = True
                else:
                    message = register_error_password_invalid

        if valid:
            users.insert_one({"id" : users.count() + 1, "username" : username, "password" : password})
            history = DatabaseConnection.get_instance().database.History
            history.insert_one({"id" : history.count() + 1, "texts" : []})

            return redirect('login')
        else:
            return render_template('register.html', message=message)




if __name__ == "__main__":
    app.run(debug=True)

