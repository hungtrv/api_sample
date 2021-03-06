from main import db
from main.errors import ValidationError
from flask import url_for

class Customer(db.Model):
	__tablename__ = "customers"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	orders = db.relationship('Order', backref='customer', lazy='dynamic')

	def get_url(self):
		return url_for('api.get_customer', id=self.id, _external=True)

	def export_data(self):
		return {
			'self_url': self.get_url(),
			'name': self.name,
			'orders_url': url_for('api.get_customer_orders', id=self.id, _external=True)
		}

	def import_data(self, data):
		try:
			self.name = data['name']
		except KeyError as e:
			raise ValidationError('Invalid customer: missing ' + e.args[0])
		return self

	def __repr__(self):
		return "<Customer {0}>".format(self.name)