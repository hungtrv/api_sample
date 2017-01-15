"""
	Authentication module
	An Authentication Token is required for all requests to resources
	1. Get Authentication Token
	http --auth username:password GET http://localhost:5000/get-auth-token

	2. Access resource
	http --auth auth_token: GET http://localhost:5000/customers/
"""
from main import app
from main.controllers.v1 import api
from main import auth
from main import auth_token

from main.models.users import User

from flask import jsonify
from flask import g

from main.decorators import json
from main.decorators import no_cache
from main.decorators import etag


@auth.verify_password
def verify_password(username, password):
    g.user = User.query.filter_by(username=username).first()
    if g.user is None:
        return False

    return g.user.verify_password(password)

@auth.error_handler
def unauthorized():
    response = jsonify({
        'status': 401,
        'error': 'unauthorized',
        'message': 'please authenticate'
    })
    response.status_code = 401

    return response

@auth_token.verify_password
def verify_auth_token(token, unused_password):
	g.user = User.verify_auth_token(token)
	return g.user is not None

@auth_token.error_handler
def unauthorized_token():
	response = jsonify({
		'status': 401,
		'error': 'unauthorized',
		'message': 'please send your authentication token'
		})
	response.status_code = 401

	return response


@api.before_request
@auth_token.login_required
def before_request():
	pass

@api.after_request
@etag
def after_request(rv):
	"""
		Generate etag and append to the response
	"""
	return rv


@app.route('/get-auth-token')
@auth.login_required
@no_cache
@json
def get_auth_token():
	return {'token': g.user.generate_auth_token()}
