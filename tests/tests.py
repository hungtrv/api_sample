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
		pass

	def tearDown(self):
		pass

	def test_customers(self):
		pass





if __name__ == "__main__":
	print unittest.main()