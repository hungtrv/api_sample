import coverage
COV = coverage.coverage(branch=True, include='main*')
COV.start()

from werkzeug.exceptions import NotFound
import unittest
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.insert(0, app_dir)

os.environ['ENVIRONMENT'] = 'development'
API_VERSION = '/v1'

from main import app
from main import db 
from main.models.users import User

from test_client import TestClient

class TestAPI(unittest.TestCase):
	default_username = 'hungtrv'
	default_password = '123456'

	def setUp(self):
		self.app = app
		self.ctx = self.app.app_context()
		self.ctx.push()
		db.drop_all()
		db.create_all()
		user = User(username=self.default_username)
		user.set_password(self.default_password)
		db.session.add(user)
		db.session.commit()
		self.client = TestClient(self.app, user.generate_auth_token(), '')


	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.ctx.pop()


	def test_customers(self):
		customers_endpoint = API_VERSION + '/customers/'
		# Get list of customers
		rv, json = self.client.get(customers_endpoint)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['customers'] == [])

		# Add a new customer
		customer_data = {'name': 'Hung Tran'}
		rv, json = self.client.post(customers_endpoint, data=customer_data)
		self.assertTrue(rv.status_code == 201)
		location = rv.headers['Location']
		rv, json = self.client.get(location)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == customer_data['name'])
		rv, json = self.client.get(customers_endpoint)
		self.assertTrue(rv.status_code == 200)
		self.assertIn(location, json['customers'])

		# Edit a customer
		new_customer_data = {'name': 'Ha An'}
		rv, json = self.client.put(location, data=new_customer_data)
		self.assertTrue(rv.status_code == 200)
		rv, json = self.client.get(location)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == new_customer_data['name'])


	def test_products(self):
		products_endpoint = API_VERSION + '/products/'
		# Get a list of products
		rv, json = self.client.get(products_endpoint)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['products'] == [])

		# Add a new product
		product_data = {'name': 'product_1'}
		rv, json = self.client.post(products_endpoint, data=product_data)
		self.assertTrue(rv.status_code == 201)
		location = rv.headers['Location']
		rv, json = self.client.get(location)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == product_data['name'])
		rv, json = self.client.get(products_endpoint)
		self.assertTrue(rv.status_code == 200)
		self.assertIn(location, json['products'])

		# Edit a product
		new_product_data = {'name': 'iPhone 7'}
		rv, json = self.client.put(location, data=new_product_data)
		self.assertTrue(rv.status_code == 200)

		rv, json = self.client.get(location)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == new_product_data['name'])


	def test_orders_and_items(self):
		# Add a new customer
		customers_endpoint = API_VERSION + '/customers/'
		customer_data = {'name': 'Hung Tran'}
		rv, json = self.client.post(customers_endpoint, data=customer_data)
		self.assertTrue(rv.status_code == 201)

		customer = rv.headers['Location']
		rv, json = self.client.get(customer)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == customer_data['name'])

		orders_url = json['orders_url']
		rv, json = self.client.get(orders_url)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['orders'] == [])

		# Add products to the db
		products_endpoint = API_VERSION + '/products/'
		product_1 = {'name': 'product 1'}
		rv, json = self.client.post(products_endpoint, data=product_1)
		self.assertTrue(rv.status_code == 201)
		product_1_link = rv.headers['Location']
		rv, json = self.client.get(product_1_link)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == product_1['name'])

		product_2 = {'name': 'product 2'}
		rv, json = self.client.post(products_endpoint, data=product_2)
		self.assertTrue(rv.status_code == 201)
		product_2_link = rv.headers['Location']
		rv, json = self.client.get(product_2_link)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == product_2['name'])

		# Create a new order
		orders_endpoint = API_VERSION + '/orders/'
		rv, json = self.client.post(orders_url, data={'date': '2017-01-10T00:00:00Z'})
		self.assertTrue(rv.status_code == 201)
		order = rv.headers['Location']
		rv, json = self.client.get(order)
		items_url = json['items_url']
		rv, json = self.client.get(items_url)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['items'] == [])
		rv, json = self.client.get(orders_endpoint)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(len(json['orders']) == 1)
		self.assertTrue(order in json['orders'])

		# Edit order
		rv, json = self.client.put(order, data={'date': '2017-01-10T23:59:59Z'})
		self.assertTrue(rv.status_code == 200)
		rv, json = self.client.get(order)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['date'] == '2017-01-10T23:59:59Z')

		# Add items to order
		rv, json = self.client.post(items_url, data={'product_url': product_1_link, 'quantity': 2})
		self.assertTrue(rv.status_code == 201)
		item_1 = rv.headers['Location']

		rv, json = self.client.post(items_url, data={'product_url': product_2_link, 'quantity': 3})
		self.assertTrue(rv.status_code == 201)
		item_2 = rv.headers['Location']

		rv, json = self.client.get(items_url)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(len(json['items']) == 2)
		self.assertIn(item_1, json['items'])
		self.assertIn(item_2, json['items'])

		rv, json = self.client.get(item_1)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['product_url'] == product_1_link)
		self.assertTrue(json['quantity'] == 2)
		self.assertTrue(json['order_url'] == order)

		rv, json = self.client.get(item_2)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['product_url'] == product_2_link)
		self.assertTrue(json['quantity'] == 3)
		self.assertTrue(json['order_url'] == order)

		# Edit 2nd item
		rv, json = self.client.put(item_2, data={'product_url': product_2_link, 'quantity': 1})
		self.assertTrue(rv.status_code == 200)
		rv, json = self.client.get(item_2)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['product_url'] == product_2_link)
		self.assertTrue(json['quantity'] == 1)
		self.assertTrue(json['order_url'] == order)

		# Delete 1st item
		rv, json = self.client.delete(item_1)
		self.assertTrue(rv.status_code == 200)
		rv, json = self.client.get(items_url)
		self.assertNotIn(item_1, json['items'])
		self.assertIn(item_2, json['items'])

		# Delete order
		rv, json = self.client.delete(order)
		self.assertTrue(rv.status_code == 200)
		with self.assertRaises(NotFound):
			rv, json = self.client.get(item_2)
		rv, json = self.client.get(orders_endpoint)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(len(json['orders']) == 0)


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
	unittest.TextTestRunner(verbosity=2).run(suite)
	COV.stop()
	COV.report()