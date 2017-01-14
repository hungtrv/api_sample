import functools
from flask import jsonify

def json(f):
	"""
		Generate a JSON response for an endpoint
		- Input: A dictionary [A HTTP Status Code] [A Dictionary of HTTP Headers]
		- Output: JSON response
	"""
	@functools.wraps(f)
	def wrapped(*args, **kwargs):
		rv = f(*args, **kwargs)
		"""
			Output of f can be:
			- Just a dictionary
			- A dictionary and A Satus Code
			- A dictionary and and Headers
			- A dictionary, A Status Code, and Headers
		"""
		status = None
		headers = None
		if isinstance(rv, tuple):
			rv, status, headers = rv + (None,) * (3 - len(rv))

		if isinstance(status, (dict, list)):
			headers, status = status, None

		if not isinstance(rv, dict):
			rv = rv.export_data()

		rv = jsonify(rv)
		if status is not None:
			rv.status_code = status
		if headers is not None:
			rv.headers.extend(headers)

		return rv
	return wrapped