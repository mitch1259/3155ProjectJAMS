from database import db
import datetime

class Task(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	project_id = db.Column("project_id", db.Integer)
	name = db.Column("name", db.String(200))
	text = db.Column("text", db.String(200))
	deadline = db.Column("deadline", db.String(10))
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


	def __init__(self, project_id, name, text, deadline, user_id):
		self.project_id = project_id
		self.name = name
		self.text = text
		self.deadline = deadline
		self.user_id = user_id

class User(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	first_name = db.Column("first_name", db.String(100))
	last_name = db.Column("last_name", db.String(100))
	email = db.Column("email", db.String(100))
	password = db.Column(db.String(255), nullable=False)
	registered_on = db.Column(db.DateTime, nullable=False)
	clock = db.Column("clock", db.Integer)
	tasks = db.relationship("Task", backref="user", lazy=True)



	def __init__(self, first_name, last_name, email, password):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.registered_on = datetime.date.today()
		self.clock = 2

class Project(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column("name", db.String(100))
	user = db.Column("user", db.Integer)
	comments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)



	def __init__(self, name, user):
		self.name = name
		self.user = user

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False)
	content = db.Column(db.VARCHAR, nullable=False)
	project = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
	user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

	def __init__(self, content, project, user):
		self.date_posted = datetime.date.today()
		self.content = content
		self.project = project
		self.user = user