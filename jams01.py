# Project JAMS - Software Engineering Project

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask, render_template, request, redirect, url_for, session
from database import db
from models import Task as Task, User as User, Project as Project

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
    my_projects = db.session.query(Project).all()
    return render_template('user.html', user=a_user, projects=my_projects)

@app.route('/<project_id>')
#View Project
def project(project_id):
    print(project_id)
    a_user =  db.session.query(User).filter_by(email='mmart196@uncc.edu').one()
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    my_tasks = db.session.query(Task).filter_by(project_id=project_id).all()
    return render_template('view.html', project=my_project, user=a_user, tasks=my_tasks)

@app.route('/<project_id>/create', methods=['GET', 'POST'])
#Create task in project
def create(project_id):
    if request.method == 'POST':
        project_id = project_id
        name = request.form['name']
        text = request.form['text']
        deadline = request.form['deadline']
        new_record = Task(project_id, name, text, deadline)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('.project', project_id=project_id))
    else:
        a_user = db.session.query(User).filter_by(email='mmart196@uncc.edu').one()
        my_project = db.session.query(Project).filter_by(id=project_id).one()
        return render_template('create.html', user=a_user, project=my_project)


@app.route('/<project_id>/edit/<task_id>', methods=['GET', 'POST'])
#Edit task in project
def edit(project_id, task_id):
    if request.method == 'POST':
        task_id = task_id
        project_id = project_id
        name = request.form['name']
        text = request.form['text']
        deadline = request.form['deadline']
        task = db.session.query(Task).filter_by(id=task_id).one()
        task.task_id = task_id
        task.project_id = project_id
        task.name = name
        task.text = text
        task.deadline = deadline
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('.project', project_id=project_id))
    else:
        a_user = db.session.query(User).filter_by(email='mmart196@uncc.edu').one()
        my_task = db.session.query(Task).filter_by(id=task_id).one()
        my_project = db.session.query(Project).filter_by(id=project_id).one()
        return render_template('create.html', task=my_task, project=my_project, user=a_user)

@app.route('/<task_id>/delete', methods=['POST'])
#Delete task in project
def delete(task_id):
    task = db.session.query(Task).filter_by(id=task_id).one()
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('.project', project_id=project_id))

@app.route('/clock')
def clock():
    return render_template('clock.html')


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.