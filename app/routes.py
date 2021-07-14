from flask import request, jsonify, render_template, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from app.models import Personality_traits, Recruiter, Applicants
from app import app, db, bcrypt
import pickle

import os
print(os.listdir())

#import sys
#print(sys.path)

model = pickle.load(open("./app/model.pkl", "rb"))
words = ['','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
nomalized_all_types_scores = {'one': {'extroversion_score': 1.0,
  'neuroticism_score': 1.0,
  'agreeableness_score': 0.0,
  'conscientiousness_score': 1.0,
  'openness_score': 1.0},
 'two': {'extroversion_score': 0.0,
  'neuroticism_score': 0.5266774246070499,
  'agreeableness_score': 1.0,
  'conscientiousness_score': 0.0,
  'openness_score': 0.2706157962700227},
 'three': {'extroversion_score': 0.5829270329409761,
  'neuroticism_score': 0.0,
  'agreeableness_score': 0.35354534551605604,
  'conscientiousness_score': 0.20782480416763896,
  'openness_score': 0.0},
 'four': {'extroversion_score': 0.8441415528469063,
  'neuroticism_score': 0.9505598140676451,
  'agreeableness_score': 0.1261143679011729,
  'conscientiousness_score': 0.8600415240193192,
  'openness_score': 0.8848220750657754},
 'five': {'extroversion_score': 0.361530138488812,
  'neuroticism_score': 0.7200735181736958,
  'agreeableness_score': 0.5500146874169198,
  'conscientiousness_score': 0.3895502283488151,
  'openness_score': 0.5814584822317371},
 'six': {'extroversion_score': 0.6383968118713308,
  'neuroticism_score': 0.8505468840751043,
  'agreeableness_score': 0.4948730789601586,
  'conscientiousness_score': 0.6943433416976627,
  'openness_score': 0.7786318930322362},
 'seven': {'extroversion_score': 0.9679850092640017,
  'neuroticism_score': 0.992179085813225,
  'agreeableness_score': 0.12629622067379756,
  'conscientiousness_score': 0.9919914909312427,
  'openness_score': 0.9778946053054914},
 'eight': {'extroversion_score': 0.2701741425915709,
  'neuroticism_score': 0.6947865700517648,
  'agreeableness_score': 0.6448240430741015,
  'conscientiousness_score': 0.2818516132604176,
  'openness_score': 0.45443483292844916},
 'nine': {'extroversion_score': 0.2138600748635372,
  'neuroticism_score': 0.6419369629131259,
  'agreeableness_score': 0.7427255275584419,
  'conscientiousness_score': 0.21180927976540873,
  'openness_score': 0.41636629914564033},
 'ten': {'extroversion_score': 0.5177260056644333,
  'neuroticism_score': 0.7481189667368449,
  'agreeableness_score': 0.7394776039875329,
  'conscientiousness_score': 0.5467162284678114,
  'openness_score': 0.6371790792165047}}



@app.route('/')
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/weight')
@login_required
def weight():  
    return render_template('weight.html')

@app.route('/weight_api', methods=['GET', 'POST'])
def weight_api():
    data =  [int(x) for x in request.form.values()]
    final_data = [np.array(data)]
    #print(final_data)
    return render_template('rank.html', final_data=final_data)

@app.route('/question')
@login_required
def question():  
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    #model = pickle.load(open("model.pkl", "rb"))
    data =  [float(x) for x in request.form.values()]
    final_data = [np.array(data)]
    prediction = words[int(model.predict(final_data))]
    plt.figure(figsize =(15,5))
    plt.ylim(0,1)
    plt.bar(list(nomalized_all_types_scores[prediction].keys()), nomalized_all_types_scores[prediction].values(), color = 'y')
    plt.savefig('./app/static/plot.png')
    
    filepath = r"C:\Users\HP\flaskproject\env\database\data.csv.pkl" 
    with open(filepath ,'ab') as f:
        result = nomalized_all_types_scores[prediction]
        pickle.dump(result, f)
        Traits = Personality_traits(trait_owner = current_user, traits = str(result))
        db.session.add(Traits)
        db.session.commit()
        flash('Your personality data is saved', 'success')
    return render_template('result.html', prediction=nomalized_all_types_scores[prediction])


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        var = {"1" : Applicants, "2" : Recruiter }
        userr = form.user_type.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        rrr = user = var[userr]
        user = rrr(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        var = {"1" : Applicants, "2" : Recruiter }
        userr = form.user_type.data
        user = var[userr].query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('question')) if form.user_type.data else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/personality")
@login_required
def test():
    return render_template('test.html', title='test')

@app.route('/predict_api', methods = ['POST'])
def predict_api():
    data = request.get_json(force = True)
    prediction = model.predict([np.array(list(data.values()))])
    output = prediction
    return jsonify(output)
