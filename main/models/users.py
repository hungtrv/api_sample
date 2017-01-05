from main import db

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True)
	password_hash = db.Column(db.String(128))


	def set_password(self, password):
		self.password_hash = generate_password_hash(password)


	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)