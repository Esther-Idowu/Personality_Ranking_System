#import sys
#print(sys.path)
from app import db, login_manager
#from flask_login import login_user, current_user
from flask_login import UserMixin
from flask_session import Session
from flask import request, session
from sqlalchemy.orm import backref

#from flask_wtf import FlaskForm

#@login_manager.user_loader
#def load_user(user_id):
    #return Recruiter.query.get(int(user_id))
    
@login_manager.user_loader
def load_user(user_id):
    if 'user_type' in session:
        if session['user_type'] == 'Applicants':
            return Applicants.query.get(int(user_id))
        elif session['user_type'] == 'Recruiter':
            return Recruiter.query.get(int(user_id))
        else:
            return None

apps = db.Table('apps',
db.Column('recruiter_id', db.Integer, db.ForeignKey('recruiter.id')),
db.Column('applicants_id', db.Integer, db.ForeignKey('applicants.id'))
)


class Recruiter(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    apps = db.relationship('Applicants', secondary = apps, backref=db.backref('applications'),lazy = 'dynamic') 
    
    def __repr__(self):
        return f"Recruiter('{self.username}', '{self.email}')"
    
class Applicants(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    appId = db.relationship('Personality_traits', backref ="trait_owner", lazy= True, uselist = False)

    def __repr__(self):
        return f"Applicants('{self.username}','{self.email}')"

class Personality_traits(db.Model):
    traits_id = db.Column(db.Integer, primary_key=True)
    traits = db.Column(db.String(255))
    traitOwner = db.Column(db.Integer, db.ForeignKey("applicants.id"))
  

    