from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc

from main import db
from main.errors import ValidationError

from flask import url_for


class Order(db.Model):
	__tablename__ = 'orders'

	id = db.Column(db.Integer, primary_key=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), index=True)
	date = db.Column(db.DateTime, default=datetime.now)
	items = db.relationship('Item', backref='order', lazy='dynamic', cascade='all, delete-orphan')

	def get_url(self):
		return url_for('api.get_order', id=self.id, _external=True)

	def export_data(self):
		return {
			'self_url': self.get_url(),
			'customer_url': self.customer.get_url(),
			'date': self.date.isoformat() + 'Z',
			'items_url': url_for('api.get_order_items', id=self.id, _external=True)

		}

	def import_data(self, data):
		try:
			self.date = datetime_parser.parse(data['date']).astimezone(tzutc()).replace(tzinfo=None)
		except KeyError as e:
			raise ValidationError('Invalid order: missing ' + e.args[0])

		return self
