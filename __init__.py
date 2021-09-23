#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#from flask_login_multi.login_manager import LoginManager
#from app.forms import RegistrationForm, LoginForm

#import sys
#print(sys.path)
app = Flask(__name__, template_folder = 'templates')
app.config['SECRET_KEY'] = 'fef623631de66e6080b2b0e1052ed019'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from app import routes
#from app.models import Recruiter, Applicants