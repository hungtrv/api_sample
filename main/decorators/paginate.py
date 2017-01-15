import functools
from flask import url_for
from flask import request

def paginate(collection, max_per_page=25):
	"""
		Decorator for generating pagination for a collection
		- Functions that use this decorator must return SQLAlchemy query
		- Output is Python dictionary with paginated results
		- Application must turn the results into response object either by 
		another decorator or using custom response object accepting dictionary
		input
	"""
	def decorator(f):
		@functools.wraps(f)
		def wrapped(*args, **kwargs):
			query = f(*args, **kwargs)

			# Get pagination arguments from query string
			page = request.args.get('page', 1, type=int)
			per_page = min(request.args.get('per_page', max_per_page, type=int), max_per_page)

			# Run query with pagination parameters
			p = query.pagniate(page, per_page)

			# Pagination meta data to be included in the response
			pages = {'page': page, 'per_page': per_page, 'total': p.total, 'pages': p.pages}

			# Endpoint for the previous page if there is any
			if p.has_prev:
				pages['prev_url'] = url_for(request.endpoint, page=p.prev_num, per_page=per_page, _external=True, **kwargs)
			else:
				pages['prev_url'] = None

			# Endpoint for the next page if there is any
			if p.has_next:
				pages['next_url'] = url_for(request.endpoint, page=p.next_num, per_page=per_page, _external=True, **kwargs)
			else:
				pages['next_url'] = None

			# Endpoint of the first page
			pages['first_url'] = url_for(request.endpoint, page=1, per_page=per_page, _external=True, **kwargs)

			# Endpoint of the last page
			pages['last_url'] = url_for(request.endpoint, page=1, per_page=p.pages, _external=True, **kwargs)

			# Return a dictionary with items of the curent page and the pagination metadata
			return {collection: [item.get_url() for item in p.items], 'pages': pages}
		return wrapped
	return decorator