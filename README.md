# Simple REST API with Flask and SQLAlchemy
Adapted from miguelgrinberg's training course
## Features
1. HTTP Basic Authentication
2. Token Authentication
3. Pagination
4. HTTP Caching
5. Request Rate Limit
6. Versioning
7. Unit Testing

## REST Resources
1. Customers (/customers/ GET, POST, PUT)
2. Orders (/orders/ GET, POST, PUT, DELETE)
3. Items (/items/ GET, POST, PUT, DELETE)
4. Products (/products/ GET, POST, PUT, DELETE)

## Installation
```
$ git clone https://github.com/hungtrv/api_sample.git
$ virtualenv venv
$ source venv/bin/activate 
(venv) $ pip install -r requirements.txt
(venv) $ python manage.py init_db
(venv) $ python manage.py create_user admin:123456
```
## Testing
### Starting API server
```
(venv) $ export FLASK_APP=run.py
(venv) $ export FLASK_DEBUG=1
(venv) $ flask run
```
### Get Access Token: 
```
(venv) $ http --auth admin:123456 GET http://localhost:5000/get-auth-token
```
### Request to API Endpoints
```
(venv) $ http --auth <token>: GET http://localhost:5000/v1/customers/
(venv) $ http --auth <token>: POST http://localhost:5000/v1/customers/ name="Vu Nguyen"
(venv) $ http --auth <token>: PUT http://localhost:5000/v1/customers/1 name="Victor Nguyen"
```

## Unit Testing
```python
(venv) $ python tests/tests.py
```
