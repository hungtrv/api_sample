from main import db
from main.errors import ValidationError
from flask import url_for

from main.engines.utils import split_url

from main.models.products import Product

class Item(db.Model):
	__tablename__ = 'items'

	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), index=True)
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'), index=True)
	quantity = db.Column(db.Integer)

	def get_url(self):
		return url_for('api.get_item', id=self.id, _external=True)

	def export_data(self):
		return {
			'self_url': self.get_url(),
			'order_url': self.order.get_url(),
			'product_url': self.product.get_url(),
			'quantity': self.quantity
		}

	def import_data(self, data):
		try:
			endpoint, args = split_url(data['product_url'])
			self.quantity = int(data['quantity'])
		except KeyError as e:
			raise ValidationError('Invalid order: missing ' + e.args[0])

		if endpoint != 'get_product' or not 'id' in args:
			raise ValidationError('Invalid product URL: ' + data['product_url'])

		self.product = Product.query.get(args['id'])
		if self.product is None:
			raise ValidationError('Invalid product URL: ' + data['product_url'])

		return self

