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
		pass





if __name__ == "__main__":
	print unittest.main()