"""
	This module contains enpoints to handle ITEMS resource
"""
from main import api
from main import db
from main.models.orders import Order
from main.models.items import Item

from flask import jsonify
from flask import request


@api.route('/items/<int:id>', methods=['GET'])
def get_item(id):
	"""
		Get detail info for a specific item identified by item id
	"""
	
	return jsonify(Item.query.get_or_404(id).export_data())
	


@api.route('/orders/<int:id>/items/', methods=['GET'])
def get_order_items(id):
	""""
		Get list of all items of a specific order identified by order id
	"""
	order = Order.query.get_or_404(id)

	return jsonify({'items': [item.get_url() for item in order.items.all()]})


@api.route('/orders/<int:id>/items/', methods=['POST'])
def add_new_order_item(id):
	"""
		Add an item to a specific order identified by order id.
		Input parameters:
		- product_url: URL, for examle http://www.example.com/products/1
		- quantity: Int
	"""
	order = Order.query.get_or_404(id)
	item = Item(order=order)
	item.import_data(request.json)
	db.session.add(item)
	db.session.commit()

	return jsonify({}), 201, {'Location': item.get_url()}


@api.route('/items/<int:id>', methods=['PUT'])
def edit_item(id):
	"""
		Edit a specific item identified by item id
		Input parameters:
		- order_id: Int
		- product_id: Int
		- quantity: Int
	"""
	item = Item.query.get_or_404(id)
	item.import_data(request.json)
	db.session.add(item)
	db.session.commit()

	return jsonify({})


@api.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
	"""
		Delete a specific item identified by item id
	"""
	item = Item.query.get_or_404(id)
	db.session.delete(item)
	db.session.commit()

	return jsonify({})

