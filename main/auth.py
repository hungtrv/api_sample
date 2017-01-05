from main import app
from main import auth

from main.models.users import User

from flask import jsonify
from flask import g


@auth.verify_password
def verify_password(username, password):
    g.user = User.query.filter_by(username=username).first()
    if g.user is None:
        return False

    return g.user.verify_password(password)


@app.before_request
@auth.login_required
def before_request():
	"""
	In order to access the API requests must provide username and password
	Example: http --auth hungtrv:123456 GET http://localhost:5000/customers/
	"""
	pass


@auth.error_handler
def unauthorized():
    response = jsonify({
        'status': 401,
        'error': 'unauthorized',
        'message': 'please authenticate'
    })
    response.status_code = 401

    return response
