from main import app
from main import db
from main.models.customers import Customer

from flask import jsonify
from flask import request


@app.route('/customers/', methods=['GET'])
def get_customers():
    return jsonify({'customers': [customer.get_url() for customer in Customer.query.all()]})


@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    return jsonify(Customer.query.get_or_404(id).export_data())


@app.route('/customers/', methods=['POST'])
def new_customer():
    customer = Customer()
    customer.import_data(request.json)
    db.session.add(customer)
    db.session.commit()

    return jsonify({}), 201, {'Location': customer.get_url()}

@app.route('/customers/<int:id>', methods = ['PUT'])
def edit_customer(id):
	customer = Customer.query.get_or_404(id)
	customer.import_data(request.json)
	db.session.add(customer)
	db.session.commit()

	return jsonify({})