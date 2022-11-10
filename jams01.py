# Project JAMS - Software Engineering Project

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask, render_template, request, redirect, url_for, session
from database import db
from models import Task as Task, User as User

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jams_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db.init_app(app)
with app.app_context():
    db.create_all()

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/user')
#List Projects
def user():
    a_user =  db.session.query(User).filter_by(email='mmart196@uncc.edu').one()
    return render_template('user.html', user=a_user)

@app.route('/tasks')
#View Project
def user_view():
    return render_template('view.html', tasks=task, user=a_user)

@app.route('/tasks/create')
#Create task in project
def create():
    return redirect(url_for('user'))

@app.route('/tasks/edit')
#Edit task in project
def edit():
    return redirect(url_for('user'))

@app.route('/delete')
#Delete task in project
def delete():
    return redirect(url_for('user'))

@app.route('/clock')
def clock():
    return render_template('clock.html')


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.