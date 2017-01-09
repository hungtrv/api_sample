import coverage
COV = coverage.coverage(branch=True, include='main*')
COV.start()

import unittest
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '../'))
sys.path.insert(0, app_dir)

os.environ['ENVIRONMENT'] = 'development'

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
		# Get list of customers
		rv, json = self.client.get('/customers/')
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['customers'] == [])

		# Add a new customer
		customer_data = {'name': 'Hung Tran'}
		rv, json = self.client.post('/customers/', data=customer_data)
		self.assertTrue(rv.status_code == 201)
		location = rv.headers['Location']
		rv, json = self.client.get(location)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == customer_data['name'])
		rv, json = self.client.get('/customers/')
		self.assertTrue(rv.status_code == 200)
		self.assertIn(location, json['customers'])

		# Edit a customer
		new_customer_data = {'name': 'Ha An'}
		rv, json = self.client.put(location, data=new_customer_data)
		self.assertTrue(rv.status_code == 200)
		rv, json = self.client.get(location)
		self.assertTrue(rv.status_code == 200)
		self.assertTrue(json['name'] == new_customer_data['name'])


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
	unittest.TextTestRunner(verbosity=2).run(suite)
	COV.stop()
	COV.report()