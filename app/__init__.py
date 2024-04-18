'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Description: Activity 20 - User Authentication Web App
'''

from flask import Flask
import os, time

app = Flask("Authentication Web App")
app.secret_key = 'do not share'

# db initialization
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@postgres.cvhpjdm21h9e.us-west-1.rds.amazonaws.com:5432/authentication'

db.init_app(app)

from app import models
with app.app_context(): 
    db.create_all()

# login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from app.models import User

# user_loader callback
@login_manager.user_loader
def load_user(id):
    try: 
        return db.session.query(User).filter(User.id==id).one()
    except: 
        return None

from app import routes