# Based on https://realpython.com/flask-google-login/
from flask import Blueprint, render_template, request, redirect, url_for, g, session
from ..serve import app
from ..models import User, Class, File, db
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)
import os
import json
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask_oauthlib.client import OAuth, OAuthException
import pytest
import ssl
import hashlib
from ..security import hash_string
ssl._create_default_https_context = ssl._create_unverified_context

# _____ CONFIG _____
'''
Sources
Google Login: https://realpython.com/flask-google-login/
Facebook login: https://github.com/lepture/flask-oauthlib/blob/master/example/facebook.py
Flask forget password: https://uniwebsidad.com/libros/explore-flask/chapter-12/forgot-your-password
Remember me code: https://www.roytuts.com/python-flask-login-logout-with-remember-me/
'''
#Commented till app context problems get solved 
google_credentials = app.config['OAUTH_CREDENTIALS']['google']
GOOGLE_CLIENT_ID = google_credentials['id']
GOOGLE_CLIENT_SECRET = google_credentials['secret']
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
facebook_credentials = app.config['OAUTH_CREDENTIALS']['facebook']
FACEBOOK_APP_ID = facebook_credentials['id']
FACEBOOK_APP_SECRET =facebook_credentials['secret']
SECRET_KEY =app.secret_key



# OAuth 2 client setup
google_client = WebApplicationClient(GOOGLE_CLIENT_ID)

oauth = OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

# Helper method to get user URL
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

login_template = Blueprint('login', __name__, template_folder='../templates',static_folder='../static')

# _____ ROUTES + CONTROLLERS _____
# On google login, redirect to Google authentication
@login_template.route('/login/google')
def google_login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

# On Google authentication callback, get user information and log user in
# create new user in database if does not exist
@login_template.route("/login/google/callback")
def google_callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens
    token_url, headers, body = google_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    google_client.parse_request_body_response(json.dumps(token_response.json()))

    # Query URL from Google that gives user's profile information, including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = google_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified, then get their information.

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    return check_and_login_user(users_name, users_email, 'google')

#Facebook login - follows similar flow as Google login 
#Made request none
@login_template.route('/login/facebook')
def facebook_login():
    callback_url = request.base_url + "/callback"
    print(callback_url)
    return facebook.authorize(callback=callback_url)
    
#Parses user information and inserts into database
@login_template.route('/login/facebook/callback')
@facebook.authorized_handler
def facebook_callback(resp): 
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    
    user_info = facebook.get('/me?fields=id,first_name,email,picture{url}')
    user_id = user_info.data['id']
    user_first_name = user_info.data['first_name']
    user_email = user_info.data['email']

    return check_and_login_user(user_first_name, user_email, 'facebook')

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')



#On logout, redirect to homepage
@login_template.route("/logout")
def logout():
    logout_user()
    print("HERE")
    return redirect(url_for('index.index'))

#Ensures that user eail exists, then logs in user. 
def check_and_login_user(user_first_name, user_email, platform_name): 
    user = User.query.filter_by(email=user_email).first()
    classes = Class.query.all()
    files = File.query.filter_by(class_id='Placeholder')
    if user is None:
        user = User(email=user_email, name=user_first_name, password=hash_string(platform_name))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return render_template('select_classes.html', name=user_first_name, email=user_email, classes = classes, files = files)
    else: 
        return render_template('select_classes.html', name=user_first_name, email=user_email, classes = classes, files = files )
    
