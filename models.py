from database import db

class Task(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column("name", db.String(200))
	text = db.Column("text", db.String(200))
	deadline = db.Column("deadline", db.String(50))

	def __init__(self, name, text, deadline):
		self.name = name
		self.text = text
		self.deadline = deadline

class User(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column("name", db.String(100))
	email = db.Column("email", db.String(100))

	def __init__(self, name, email):
		self.name = name
		self.email = email

class Project(db.Model):
	id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column("name", db.String(100))

	def __init__(self, name):
		self.name = name