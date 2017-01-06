from main import db
from main.errors import ValidationError
from flask import url_for

class Product(db.Model):
	__tablename__ = 'products'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	items = db.relationship('Item', backref='product', lazy='dynamic')

	def get_url(self):
		return url_for('api.get_product', id=self.id, _external=True)

	def export_data(self):
		return {
			'self_url': self.get_url(),
			'name': self.name
		}

	def import_data(self, data):
		try:
			self.name = data['name']
		except KeyError as e:
			raise ValidationError('Invalid product: missing ' + e.args[0])

		return self
