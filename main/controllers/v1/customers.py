"""
	This module contains enpoints to handle CUSTOMERS resource
"""
from . import api
from main import db
from main.models.customers import Customer
from main.decorators import json

from flask import request


@api.route('/customers/', methods=['GET'])
@json
def get_customers():
	"""
		Get list of all customers
	"""
	return {'customers': [customer.get_url() for customer in Customer.query.all()]}


@api.route('/customers/<int:id>', methods=['GET'])
@json
def get_customer(id):
	"""
		Get detailed information of a specific customer identified by customer id
	"""
	return Customer.query.get_or_404(id).export_data()


@api.route('/customers/', methods=['POST'])
@json
def add_new_customer():
	"""
		Add a new customer
		Input parameters:
		- name: String
	"""
	customer = Customer()
	customer.import_data(request.json)
	db.session.add(customer)
	db.session.commit()

	return {}, 201, {'Location': customer.get_url()}


@api.route('/customers/<int:id>', methods = ['PUT'])
@json
def edit_customer(id):
	"""
		Update a specific customer identified by customer id
		Input parameters:
		- name: String
	"""
	customer = Customer.query.get_or_404(id)
	customer.import_data(request.json)
	db.session.add(customer)
	db.session.commit()

	return {}