from flask import Flask, session, request, render_template, redirect
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.forma['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = data['first_name']

    return redirect('/recipes')