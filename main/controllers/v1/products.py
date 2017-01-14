"""
	This module contains enpoints to handle PRODUCTS resource
"""
from . import api
from main import db
from main.models.products import Product

from main.decorators.json import json
from flask import request


@api.route('/products/', methods=['GET'])
@json
def get_products():
	"""
		Get list of all products
	"""
	return {'products': [product.get_url() for product in Product.query.all()]}


@api.route('/products/<int:id>', methods=['GET'])
@json
def get_product(id):
	"""
		Get detailed information of a specific product identified by product id
	"""
	return Product.query.get_or_404(id).export_data()


@api.route('/products/', methods=['POST'])
@json
def add_new_product():
	"""
		Add new product to the database
		Input parameters
		- name: String
	"""
	product = Product()
	product.import_data(request.json)
	db.session.add(product)
	db.session.commit()

	return {}, 201, {'Location': product.get_url()}


@api.route('/products/<int:id>', methods=['PUT'])
@json
def edit_product(id):
	"""
		Update a specific product identified by product id
		Input parameter
		- name: String
	"""
	product = Product.query.get_or_404(id)
	product.import_data(request.json)
	db.session.add(product)
	db.session.commit()

	return {}
