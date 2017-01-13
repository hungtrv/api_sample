__all__ = [
	'index',
	'customers',
	'orders',
	'items',
	'products'
]

from flask import Blueprint

api = Blueprint('api', __name__)