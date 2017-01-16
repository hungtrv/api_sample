import functools
import hashlib
from flask import request
from flask import make_response
from flask import jsonify

def cache_control(*directives):
	"""
		Insert Cache-Control header with given directives
	"""
	def decorator(f):
		@functools.wraps(f)
		def wrapped(*args, **kwargs):
			rv = f(*args, **kwargs)
			rv = make_response(rv)
			rv.headers['Cache-Control'] = ', '.join(directives)
			return rv
		return wrapped
	return decorator


def no_cache(f):
	"""
		Insert no-cache directive to the response
	"""
	return cache_control('private', 'no-cache', 'no-store', 'max-age=0')(f)

def etag(f):
	"""
		Add entity tag (etag) handling to the decorated route
	"""
	@functools.wraps(f)
	def wrapped(*args, **kwargs):
		rv = f(*args, **kwargs)
		rv = make_response(rv)

		# Only support HEAD and GET requests
		#assert request.method in ['GET', 'HEAD'], '@etag is only supported in GET or HEAD requests'
		if request.method in ['GET', 'HEAD']:
			return rv

		# Make no change to responses with status code different than 200
		if (rv.status_code != 200):
			return rv

		# Generate etag for the request using MD5
		etag = '"' + hashlib.md5(rv.get_data()).hexdigest() + '"'
		rv.headers['ETag'] = etag

		# Handle If-Match and If-Non-Match headers if they are in the request
		if_match = request.headers.get('If-Match')
		if_none_match = request.headers.get('If-None-Match')

		# Only return response if etag is in If-Match from the request
		if if_match:
			etag_list = [tag.strip() for tag in if_match.split(',')]
			if etag not in etag_list and '*' not in etag_list:
				response = jsonify({
						'status': 402,
						'error': 'precondition failed',
						'message': 'precondition failed'
					})
				response.status_code = 402
				return response
		# Only return response if etag is not in If-None-Match
		elif if_none_match:
			etag_list = [tag.strip() for tag in if_none_match.split(',')]
			if etag in etag_list or '*' in etag_list:
				response = jsonify({
						'status': 304,
						'error': 'not modified',
						'message': 'resource not modified'
					})
				response.status_code = 304
				return make_response()

		# Return response 
		return rv
	return wrapped