'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Description: Activity 20 - Routes for the User Authentication Web App
'''

from app import app, db, load_user
from app.models import User
from app.forms import SignUpForm, SignInForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    form = SignInForm()
    if form.validate_on_submit(): 
        try: 
            user = load_user(form.id.data)
            print(user)
            if bcrypt.checkpw(
                form.passwd.data.encode('utf-8'), 
                user.passwd
            ): 
                login_user(user)
                return "Login Successful!!!"
            else:
                return '<p>Wrong password!</p>'
        except Exception as ex: 
                return f'<p>Could not find a user with the given id: {ex}</p>'
    else:
        return render_template('users_signin.html', form=form)

# copy the sign-up functionality from previous homework
@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    form = SignUpForm()
    if form.validate_on_submit(): 
        if form.passwd.data != form.passwd_confirm.data: 
            return '<p>Passwords do not match!</p>'
        try: 
            passwd = bcrypt.hashpw(
                form.passwd.data.encode('utf-8'), 
                bcrypt.gensalt()
            )
            user = User(
                id = form.id.data,
                name = form.name.data, 
                passwd = passwd
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as ex: 
            return f'<p>Problem signing up the user: {ex}</p>' 
    else:
        return render_template('users_signup.html', form=form)
    
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))
