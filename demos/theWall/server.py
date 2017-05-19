from flask import Flask, redirect, request, session, render_template, flash
app = Flask(__name__)
from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app, 'login_reg')
app.secret_key = 'this is top secret'
import md5 # imports the md5 module to generate a hash


import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    # validate the form input
    # store errors in list
    errors = []

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    password_confirmation = request.form['password_confirmation']

    # complete the validations
    # 1. First Name - letters only, at least 2 characters and that it was submitted
    if not  first_name.isalpha():
        errors.append('First name field must be characters only!')
    if len(first_name) < 2:
        errors.append('First name field must be at least 2 characters long!')
    # 2. Last Name - letters only, at least 2 characters and that it was submitted
    if not  last_name.isalpha():
        errors.append('Last name field must be characters only!')
    if len(last_name) < 2:
        errors.append('Last name field must be at least 2 characters long!')
    # 3. Email - Valid Email format, and that it was submitted
    if not len(email):
        errors.append('Email field must be present!')
    if not EMAIL_REGEX.match(email):
        errors.append('Email must be valid')
    # 4. Password - at least 8 characters, and that it was submitted
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long!')
    # 5. Password Confirmation - matches password
    if not password == password_confirmation:
        errors.append('Passwords must match!')

    # check for unique email address
    query = 'SELECT * FROM users WHERE email = :email'
    data = {
        'email':email
    }
    user = mysql.query_db(query, data)

    if user:
        errors.append('Email is already taken!')

    # check errors list
    if errors:
        # send errors back to client
        for error in errors:
            flash(error)
        return redirect('/')
    else:
        # save the user in db
        # encrypt the password we provided as 32 character string
        hashed_password = md5.new(password).hexdigest()

        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"

        data = {
            'first_name':first_name,
            'last_name':last_name,
            'email': email,
            'password': hashed_password
        }

        user = mysql.query_db(query, data)
        session['user_id'] = user
        return redirect('/success')

@app.route('/success')
def success():
    if not 'user_id' in session:
        return redirect('/')

    query = "SELECT messages.user_id, messages.id AS message_id, messages.content, DATE_FORMAT(messages.created_at, '%M %D, %Y') AS date, CONCAT(users.first_name, ' ', users.last_name) AS full_name FROM messages JOIN users on users.id = messages.user_id"

    messages = mysql.query_db(query)

    query = "SELECT comments.message_id AS comment_message_id, comments.content, DATE_FORMAT(comments.created_at, '%M %D, %Y') AS date, CONCAT(users.first_name, ' ', users.last_name) AS full_name FROM comments JOIN users on users.id = comments.user_id"

    comments = mysql.query_db(query)

    return render_template('success.html', all_messages = messages, all_comments = comments)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    # get a user from the DB
    query = 'SELECT * FROM users WHERE email = :email'
    data = {
        'email':request.form['email']
    }
    user = mysql.query_db(query, data)
    # if true
    if user:
        # continue with the login
        # check the passwords, make sure they match
        hashed_password = md5.new(request.form['password']).hexdigest()
        # if True
        if user[0]['password'] == hashed_password:
            # save user id in session
            session['user_id'] = user[0]['id']
            # send to success page
            return redirect('/success')
        else:
            # send message to client
            flash('Invalid email/ password combination!')
            # send to index page
            return redirect('/')

    else:
        flash("Email doesn't exist")
        # email does not exist
        # send message to client
        # send to index page
        return redirect('/')

@app.route('/messages', methods=['POST'])
def add_message():
    query = 'INSERT INTO messages (user_id, content, created_at, updated_at) VALUES (:user_id, :content, NOW(), NOW())'

    data = {
        'user_id': session['user_id'],
        'content': request.form['content']
    }

    mysql.query_db(query, data)


    return redirect('/success')

@app.route('/comments', methods=['POST'])
def comments():
    query = 'INSERT INTO comments (user_id, message_id, content, created_at, updated_at) VALUES (:user_id, :message_id, :content, NOW(), NOW())'

    data = {
        'user_id': session['user_id'],
        'message_id': request.form['message_id'],
        'content': request.form['content']
    }

    mysql.query_db(query, data)

    return redirect('/success')

@app.route('/delete_message/<message_id>', methods=['POST'])
def delete_message(message_id):
    query = 'DELETE FROM comments WHERE message_id = :message_id'
    data = {'message_id':message_id}
    mysql.query_db(query, data)

    query = 'DELETE FROM messages WHERE id = :message_id'
    data = {'message_id':message_id}
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug = True)
