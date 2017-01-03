"""
	This module contains enpoints to handle ORDERS resource
"""
from main import app
from main import db
from main.models.orders import Order
from main.models.customers import Customer

from flask import jsonify
from flask import request

@app.route('/orders/', methods=['GET'])
def get_orders():
	"""
		Get list of all the orders
	"""
	return jsonify({'orders': [order.get_url() for order in Order.query.all()]})


@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
	"""
		Get information of a specific order
	"""
	return jsonify(Order.query.get_or_404(id).export_data())


@app.route('/orders/<int:id>', methods=['PUT'])
def edit_order(id):
	"""
		Edit a specific order identified by order id
	"""
	order = Order.query.get_or_404(id)
	order.import_data(request.json)
	db.session.add(order)
	db.session.commit()

	return jsonify({})


@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
	"""
		Delete a specific order identified by order id
	"""
	order = Order.query.get_or_404(id)
	db.session.delete(order)
	db.session.commit()

	return jsonify({})


@app.route('/customers/<int:id>/orders/', methods=['GET'])
def get_customer_orders(id):
	"""
		Get list of all the orders or a specific customer identified by customer id
	"""
	customer = Customer.query.get_or_404(id)
	return jsonify({'orders': [order.get_url() for order in customer.orders.all()]})


@app.route('/customers/<int:id>/orders/', methods=['POST'])
def add_customer_order(id):
	"""
		Add a new order to a specific customer identify by customer id
		Input paramerter:
		- date: ISO format, for example 2017-01-01T11:59:59Z
	"""
	customer = Customer.query.get_or_404(id)
	order = Order(customer=customer)
	order.import_data(request.json)
	db.session.add(order)
	db.session.commit()

	return jsonify({}), 201, {'Location': order.get_url()}
