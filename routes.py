from flask import request, jsonify, render_template, url_for, flash, redirect, session
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_session import Session
import numpy as np
import pandas as pd 
import ast
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
    return render_template('about.html')

@app.route('/weight')
@login_required
def weight():  
    return render_template('weight.html')

@app.route('/weight_api', methods=['GET', 'POST'])
def weight_api():
    #get the data from the form
    data =  [int(x) for x in request.form.values()]
    sum_of_data = sum(data)
    print(sum_of_data)
    if sum_of_data != 15:
        flash("You have to select a unique value", "danger")
        return render_template('weight.html')
    #get all the personality traits
    app = Personality_traits.query.all()
    
    applicant_list=[]
    trait_owner_list=[]
    total_list=[]

    performance_dict={}

    #turn the personality traits to dictionary
    #add them to a dictionary-applicant_list
    #also add the trait owner to trait_owner_dictionary
    for item in app:
        applicant = ast.literal_eval(item.traits)
        applicant_list.append(applicant)
        trait_owner_list.append(item.traitOwner)
    

    #multiply each personality score by the corresponding form data
    for item in range(len(applicant_list)):
        
        extroversion_score=data[0]*applicant_list[item]['extroversion_score']
        neuroticism_score=data[1]*applicant_list[item]['neuroticism_score']
        agreeableness_score=data[2]*applicant_list[item]['agreeableness_score']
        conscientiousness_score=data[3]*applicant_list[item]['conscientiousness_score']
        openness_score=data[4]*applicant_list[item]['openness_score']
        
        #find the total of each entry
        total=extroversion_score+neuroticism_score+agreeableness_score+conscientiousness_score+openness_score

        #append the total values to the total_list
        total_list.append("{:.2f} %".format(total/15*100))

    #sort the sum of performance values in assending order
    print(trait_owner_list)

    #map the traits to the corresponding taiit owner
    performance_dict=dict(zip(trait_owner_list,total_list))

    # print(performance_dict.values().sort())
    performance_dict=dict(sorted(performance_dict.items(),key= lambda x:x[1], reverse=True))
    #applicant = applicant_list
    Info_List = []

    for info in performance_dict.items():
        
        id = info[0]
        user = Applicants.query.filter(Applicants.id)
    
        for x in user:
            if x.id == id:
                new_list = {}
                new_list["email"] = x.email
                new_list["username"] = x.username
                new_list["id"] = id
                new_list["ranking"] = info[1]
                Info_List.append(new_list)
   
      
    return render_template('rank.html', Info_List=Info_List)

@app.route('/question')
@login_required
def question():  
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    #model = pickle.load(open("model.pkl", "rb"))
    data =  [float(x) for x in request.form.values()]
    final_data = [np.array(data)]
    data = model.predict(final_data)
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
    return render_template('result.html', prediction=nomalized_all_types_scores[prediction], data = data)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        var = {"Applicants" : Applicants, "Recruiter" : Recruiter }
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
        var = {"Applicants" : Applicants, "Recruiter" : Recruiter }
        userr = form.user_type.data
        if userr == "Applicants":
            user = var[userr].query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                session['user_type'] = form.user_type.data
                next_page = request.args.get('next')
                return redirect(url_for('question')) if form.user_type.data else redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        else:
            user = var[userr].query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                session['user_type'] = form.user_type.data
                next_page = request.args.get('next')
                return redirect(url_for('weight')) if form.user_type.data else redirect(url_for('index'))
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


@app.route('/predict_api', methods = ['POST'])
def predict_api():
    data = request.get_json(force = True)
    prediction = model.predict([np.array(list(data.values()))])
    output = prediction
    return jsonify(output)
