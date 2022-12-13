# Project JAMS - Software Engineering Project

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask, render_template, request, redirect, url_for, session
from database import db
from models import Task as Task, User as User, Project as Project, Comment as Comment
from forms import RegisterForm, LoginForm, CommentForm
import bcrypt
import json
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)     # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jams_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'SE3155'
db.init_app(app)
with app.app_context():
    db.create_all()
blueprint = make_github_blueprint(client_id='8253f47264e5b958d78d', client_secret='b2c4240987cdc9326a3c6a96f713c96a8acb6a87')
app.register_blueprint(blueprint, url_prefix='/github_login')

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/user')
#List Projects
def user():
    #a_user =  db.session.query(User).filter_by(email='mmart196@uncc.edu').one()
    #my_projects = db.session.query(Project).filter_by(user_id=session['user_id']).all()
    if session.get('user'):
        my_projects = db.session.query(Project).all()
        return render_template("user.html", projects=my_projects, user=session['user'], usern=session['user_name'])
    return redirect(url_for('login'))

@app.route('/<project_id>')
#View Project
def project(project_id):
    if session.get('user'):
        my_project = db.session.query(Project).filter_by(id=project_id).one()
        my_tasks = db.session.query(Task).filter_by(project_id=project_id).all()
        return render_template('view.html', project=my_project, tasks=my_tasks, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/<project_id>/create', methods=['GET', 'POST'])
#Create task in project
def create(project_id):
    if session.get('user'):
        if request.method == 'POST':
            project_id = project_id
            name = request.form['name']
            text = request.form['text']
            deadline = request.form['deadline']
            imageUrl = request.form['imageUrl']
            new_record = Task(project_id, name, text, deadline, imageUrl, session['user'])
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('.project', project_id=project_id))
        else:
            my_project = db.session.query(Project).filter_by(id=project_id).one()
            return render_template('create.html', project=my_project, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/user/createproject', methods=['GET', 'POST'])
def createproject():
    if session.get('user'):
        if request.method == 'POST':
            name = request.form['name']
            new_record = Project(name, session['user'])
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('user'))
        else:
            return render_template('projectcreate.html', user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/<project_id>/edit/<task_id>', methods=['GET', 'POST'])
#Edit task in project
def edit(project_id, task_id):
    if session.get('user'):
        if request.method == 'POST':
            task_id = task_id
            project_id = project_id
            name = request.form['name']
            text = request.form['text']
            deadline = request.form['deadline']
            imageUrl = request.form['imageUrl']
            task = db.session.query(Task).filter_by(id=task_id).one()
            task.task_id = task_id
            task.project_id = project_id
            task.name = name
            task.text = text
            task.deadline = deadline
            task.imageUrl = imageUrl
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('.project', project_id=project_id))
        else:
            my_task = db.session.query(Task).filter_by(id=task_id).one()
            my_project = db.session.query(Project).filter_by(id=project_id).one()
            return render_template('create.html', task=my_task, project=my_project, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/<project_id>/edit', methods=['GET', 'POST'])
def editproject(project_id):
    if session.get('user'):
        if request.method == 'POST':
            project_id = project_id
            name = request.form['name']
            owner = request.form['owner']
            project = db.session.query(Project).filter_by(id=project_id).one()
            project.project_id = project_id
            project.name = name
            project.user = owner
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('.project', project_id=project_id))
        else:
            project=db.session.query(Project).filter_by(id=project_id).one()
            return render_template('editproject.html', project=project, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/delete/<project_id>', methods=['GET'])
def deleteproject(project_id):
    if session.get('user'):
        project = db.session.query(Project).filter_by(id=project_id).one()
        tasks = db.session.query(Task).filter_by(project_id=project_id).all()
        for i in tasks:
            db.session.delete(i)
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

@app.route('/<task_id>/delete', methods=['POST'])
#Delete task in project
def delete(task_id):
    if session.get('user'):
        task = db.session.query(Task).filter_by(id=task_id).one()
        project_id = task.project_id
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('.project', project_id=project_id))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
#register a user
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        
        new_user = User(first_name, last_name, request.form['email'], h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user_name'] = first_name
        session['user'] = new_user.id
        return redirect(url_for('user'))
    return render_template('register.html', form=form)

@app.route('/login/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        print(github.get('/user'))
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            first_name = format(account_info_json['login'])
            try:
                user = db.session.query(User).filter_by(email=first_name).one()
                session['user_name'] = user.first_name
                session['user'] = user.id
            except:
                print("Error caught")
                user = User(first_name, first_name, first_name, first_name)
                db.session.add(user)
                db.session.commit()
                session['user_name'] = user.first_name
                session['user'] = user.id
            return redirect(url_for('user'))

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user_name'] = the_user.first_name
            session['user'] = the_user.id
            return redirect(url_for('user'))

        login_form.password.errors = ["Incorrect username or password"]
        return render_template("login.html", form=login_form)
    else:
        return render_template("login.html", form=login_form)

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('login'))

@app.route('/clock')
def clock():
    if session.get('user'):
        clock = db.session.query(User).filter_by(id=session['user']).one().clock
        display = int((clock-2)/2)
        return render_template("clock.html", clock=clock, display=display)
    else:
        return redirect(url_for('login'))

@app.route('/clocklogic')
def clocklogic():
    if session.get('user'):
        curruser = db.session.query(User).filter_by(id=session['user']).one()
        curruser.id = curruser.id
        curruser.first_name = curruser.first_name
        curruser.last_name = curruser.last_name
        curruser.email = curruser.email
        curruser.password = curruser.password
        curruser.registered_on = curruser.registered_on
        curruser.clock = curruser.clock + 1
        db.session.add(curruser)
        db.session.commit()
        return redirect(url_for('clock'))
    else:
        return redirect(url_for('login'))

@app.route('/<project_id>/comment', methods=['POST', 'GET'])
def comment(project_id):
    if session.get('user'):
        comment_form = CommentForm()
        project = db.session.query(Project).filter_by(id=project_id).one()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, project_id, session['user'])
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('.project', project_id=project_id))
        return render_template("comment.html", project=project, form=comment_form)
    else:
        return redirect(url_for('login'))

@app.route('/calendar')
def calendar():

    if session.get('user'):
        my_projects = db.session.query(Project).all()
        my_tasks = db.session.query(Task).order_by(Task.deadline).all()

        return render_template("calendar.html", projects=my_projects, tasks=my_tasks, user=session['user'], usern=session['user_name'])
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.