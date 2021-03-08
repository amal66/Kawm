#! Not functional! only frontend
'''
Sources
Google Login: https://realpython.com/flask-google-login/
Facebook login: https://github.com/lepture/flask-oauthlib/blob/master/example/facebook.py
Flask forget password: https://uniwebsidad.com/libros/explore-flask/chapter-12/forgot-your-password
Remember me code: https://www.roytuts.com/python-flask-login-logout-with-remember-me/
'''

from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account

from flask import Blueprint,render_template,redirect,url_for,request,flash, session
from flask import current_app as app
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)
from flask_mail import Message,Mail
from ..models import User, db
from ..security import hash_string
from .index import index
import os
user_template = Blueprint('user', __name__, template_folder='../templates',static_folder='../static')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

#Gets information from form and registers user. 
@user_template.route('/register', methods=['GET', 'POST'] )
def register():
    if request.method == 'POST':
        email = request.form.get('InputEmail')
        first_name = request.form.get('FirstName')
        last_name = request.form.get('LastName')
        password = request.form.get('InputPassword')
        confirmation_password = request.form.get('RepeatPassword')
        user = User.query.filter_by(email=email).first() 

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('user.register'))
        
        
        if password != confirmation_password: 
            flash('Passwords do not match')
            return redirect(url_for('user.register'))
        

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=email, name=first_name, password = hash_string(password))
        #new_user = User(email=email, name=first_name)
        # add the new user to the database 

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        #return render_template('logged_in.html', name=users_name, email=users_email)
        return render_template('select_courses.html', name=first_name, email=email)
    else: 
        return render_template('register.html')

#
@user_template.route('/forgotpassword', methods=["GET","POST"])
def forgot_password():
    if request.method == 'GET': 
        return render_template('forgot_password.html')
    else: 
        user_email = request.form.get('InputEmail')
        user = User.query.filter_by(email=user_email).first()
        if user is None:
            flash('No such user!')
            return redirect(url_for('user.forgot_password'))
        else: 
            return_url = send_reset_email(user)
            flash(f"Email sent! Go to {return_url}")
            return redirect(url_for('user.forgot_password'))

def send_reset_email(user):
    token = user.get_reset_token()
    print(token)
    sender='amal@minerva.kgi.edu'
    recipient = user.email
    subject = 'Kawm Reset Link'
    message_body = f'''To reset your password, visit the following link:
                {url_for('user.reset_token', token=token, _external=True)}
                If you did not make this request then simply ignore this email and no changes will be made.
                '''
    return message_body

  

@user_template.route("/forgotpassword/<token>", methods=['GET', 'POST'])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('index.index'))

    user_exists = User.verify_reset_token(token=token)
    if user_exists is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_token'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

def get_google_service(sender):
  SCOPES = ['https://www.googleapis.com/auth/gmail.send']
  SERVICE_ACCOUNT_FILE = 'credentials.json'

  credentials = service_account.Credentials.from_service_account_file(
          SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  delegated_credentials = credentials.with_subject(sender)
  service = build('gmail', 'v1', credentials=delegated_credentials)
  return service

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except (errors.HttpError, error):
    print ('An error occurred: %s' % error)
