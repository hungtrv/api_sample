from main import app
from main import db
from main.models.products import Product

from flask import jsonify
from flask import request


@app.route('/products/', methods=['GET'])
def get_products():
    return jsonify({'products': [product.get_url() for product in Product.query.all()]})


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    return jsonify(Product.query.get_or_404(id).export_data())


@app.route('/products/', methods=['POST'])
def add_product():
    product = Product()
    product.import_data(request.json)
    db.session.add(product)
    db.session.commit()

    return jsonify({}), 201, {'Location': product.get_url()}


@app.route('/products/<int:id>', methods=['PUT'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    product.import_data(request.json)
    db.session.add(product)
    db.session.commit()

    return jsonify({})
