# Project JAMS - Software Engineering Project

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)     # create an app

a_user = {'name': 'TestUser', 'email':'test@uncc.edu'}

task = {1: {'Task': 'Order shipment', 'Details': 'Shipment of office supplies', 'CurrentDate': '10-01-2020', 'Deadline': '10-05-2020'},
            2: {'Task': 'Train Robert about web app', 'Details': 'Teach the basics of web app and provide resources', 'CurrentDate': '10-02-2020', 'Deadline': '10-07-2020'},
            3: {'Task': 'Create database', 'Details': 'Create updated database for new clients', 'CurrentDate': '10-11-2020', 'Deadline': '10-15-2020'}
            }

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/user')
def user():
    return render_template('user.html', user=a_user)

@app.route('/tasks')
def user_view():
    return render_template('view.html', tasks=task, user=a_user)

@app.route('/clock')
def clock():
    return render_template('clock.html')


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.