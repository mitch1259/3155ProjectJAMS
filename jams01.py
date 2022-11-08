# Project JAMS - Software Engineering Project

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import render_template
from flask import Flask   # Flask is the web app that we will customize

app = Flask(__name__)     # create an app

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/user')
def user():
    a_user = {'name': 'Soumitri', 'email':'mogli@uncc.edu'}
    return render_template('user.html', user=a_user)

@app.route('/tasks')
def user_view():
    tasks = {1: {'Task': 'Order shipment', 'Details': 'Shipment of office supplies', 'CurrentDate': '10-01-2020', 'Deadline': '10-05-2020'},
            2: {'Task': 'Train Robert about web app', 'Details': 'Teach the basics of web app and provide resources', 'CurrentDate': '10-02-2020', 'Deadline': '10-07-2020'},
            3: {'Task': 'Create database', 'Details': 'Create updated database for new clients', 'CurrentDate': '10-11-2020', 'Deadline': '10-15-2020'}
            }
    return render_template('view.html', tasks=tasks)

# @app.route('/notes/<note_id>')
# def get_note(note_id):
#     notes = {1: {'title': 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
#             2: {'title': 'Second note', 'text': 'This is my second note', 'date': '10-2-2020'},
#             3: {'title': 'Third note', 'text': 'This is my third note', 'date': '10-3-2020'}}
#     return render_template('note.html', note=notes[int(note_id)])


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.