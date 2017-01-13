from main import app

@app.route('/')
def index():
	return "<H1>Welcome! This is a sample API project built on top of Flask!</H1>"