import requests
import psycopg2
from web.templates import
from sqlalchemy import create_engine

# Format: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = 'postgres+psycopg2://mcomm_dev_user:mcomm_dev_password@127.0.0.1:5432/mcommunity20'
engine = create_engine(DATABASE_URI, echo=True)


# Testing successful status code for each page

def test_basic_request():
    r = requests.get('http://127.0.0.1:5000/')
    assert r.status_code == 200

def test_routing_mainpage():
    r = requests.get('http://127.0.0.1:5000/mainpage')
    assert r.status_code == 200

def test_routing_register():
    r = requests.get('http://127.0.0.1:5000/register')
    assert r.status_code == 200

# Testing register with Google

# Testing register with Facebook

# Testing normal registration

def test_registration_success():
	details = {"exampleFirstName": "Alfonso","exampleLastName": "Santacruz","exampleInputEmail": "asantacruz@minerva.kgi.edu","exampleInputPassword": "MCommunity2020!","exampleRepeatPassword":"MCommunity2020!"}
	req_reg = requests.post('http://127.0.0.1:5000/register', data = details)
	deet_signin = {"exampleInputEmail":"asantacruz@minerva.kgi.edu", "exampleInputPassword":"MCommunity2020!"}
	req_login = request.post('http://127.0.0.1:5000/', data = deet_signin)
	assert req_login.url == 'http://127.0.0.1:5000/mainpage'

def test_registration_fail():
	details = {"exampleFirstName": "Alfonso","exampleLastName": "Santacruz","exampleInputEmail": "asantacruz@minerva.kgi.edu","exampleInputPassword": "MCommunity2020!","exampleRepeatPassword":"Randomdifferent"}
	req_reg = requests.post('http://127.0.0.1:5000/register', data = details)
	assert req_reg == 'http://127.0.0.1:5000/register'

# Testing login with Google

# Testing login with Facebook

# Testing standard login

def test_right_login():
	deet_signin = {"exampleInputEmail":"asantacruz@minerva.kgi.edu", "exampleInputPassword":"MCommunity2020!"}
	req_login = request.post('http://127.0.0.1:5000/', data = deet_signin)
	assert req_login.url == 'http://127.0.0.1:5000/mainpage'

def test_faulty_login():
	deet_signin = {"exampleInputEmail":"asantacruz@minerva.kgi.edu", "exampleInputPassword":"test123!"}
	req_login = request.post('http://127.0.0.1:5000/', data = deet_signin)
	assert req_login.url == 'http://127.0.0.1:5000/'
