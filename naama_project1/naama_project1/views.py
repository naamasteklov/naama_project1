"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from naama_project1 import app
from naama_project1.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from flask_wtf import FlaskForm

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField, RadioField
from wtforms import ValidationError

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from naama_project1.Models.QueryFormStructure import QueryFormStructure 
from naama_project1.Models.QueryFormStructure import UserRegistrationFormStructure 
from naama_project1.Models.QueryFormStructure import LoginFormStructure 

class Alcoholform(FlaskForm):
    famsize = RadioField('Family size greater than 3?' , validators = [DataRequired] , choices=[('GT3', 'GT3'), ('LE3', 'LE3')])
    sex = RadioField('Choose gender:' , validators = [DataRequired] , choices=[('F', 'F'), ('M', 'M')])
    activities = RadioField('Activities?' , validators = [DataRequired] , choices=[('yes', 'yes'), ('no', 'no')])
    romantic = RadioField('In a romantic relationship?' , validators = [DataRequired] , choices=[('yes', 'yes'), ('no', 'no')])
    submit = SubmitField('submit')


db_Functions = create_LocalDatabaseServiceRoutines() 
#-----------------------------------
# Landing page - home page - תמונות עם קישורים
#-----------------------------------
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

#-----------------------------------
# contact page - דף קשר עם הפרטים שלי
#-----------------------------------
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )
#-----------------------------------
# about page - מידע על הנושא
#-----------------------------------
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )



@app.route('/query', methods=['GET', 'POST'])
def query():

    #קורא את הטבלה 
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\MyData\\student-mat.csv'))
    
    #משתמש בקלאס שרשמתי למעלה 
    form = Alcoholform()
    #תמונה שתופיע בעמוד
    chart = 'https://www.kipa.co.il/userFiles/1_0b5bfd0ec6fb3616911f87a366a10e97.jpg'
    if (request.method == 'POST' ):
        famsize = form.famsize.data
        sex = form.sex.data
        romantic = form.romantic.data
        activities = form.activities.data
        #מוציא את הדברים שלא חשובים בטבלה
        df = df.drop(['school', 'Fedu', 'Medu', 'reason','guardian','traveltime', 'studytime', 'paid','G1', 'G2','G3', 'address','Pstatus','Mjob','Fjob','failures','schoolsup','famsup','nursery','higher','internet','famrel','freetime','goout','health','absences','Dalc'], 1)
   
        df = df.loc[df["famsize"]==famsize]
        df = df.loc[df["sex"]==sex]
        df = df.loc[df["activities"]==activities]
        df = df.loc[df["romantic"]==romantic]
        df = df.groupby('age').mean()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #גרף
        df.plot(kind = 'bar', ax=ax)
        chart = plot_to_img(fig)




    return render_template('query.html', 
            form = form, 
            title='Query by the user',
            chart = chart
           
        )

# -------------------------------------------------------
# Register new user page
# This function will get user details, will check if the user already exists
# and if not, it will save the details in the users data base
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('query')
            
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',

        )

# -------------------------------------------------------
# Data model description, used by the site
# -------------------------------------------------------
@app.route('/dataModel')
def dataModel():
    """Renders the contact page."""
    return render_template(
        'dataModel.html',
        title='This is my Data Model page abou UFO',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )

# -------------------------------------------------------
# Data Set page - הטבלה 
# -------------------------------------------------------
@app.route('/DataSet1')
def DataSet1():
    
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\MyData\\student-mat.csv'))
    
    df = df.drop(['school', 'Fedu', 'Medu', 'reason','guardian','traveltime', 'studytime', 'paid','G1', 'G2','G3', 'address','Pstatus','Mjob','Fjob','failures','schoolsup','famsup','nursery','higher','internet','famrel','freetime','goout','health','absences','Dalc'], 1)
   
    raw_data_table = df.to_html(classes = 'table table-hover')
   
    """Renders the contact page."""
    return render_template(
        'DataSet1.html',
      
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'

    )
def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


