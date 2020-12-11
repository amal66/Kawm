from flask import Blueprint, render_template,redirect,url_for,request,flash,make_response
from flask import current_app as app
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)
from ..models import User, db
from ..security import hash_string
from datetime import datetime
index_template = Blueprint('index', __name__, template_folder='../templates',static_folder='../static')

# Display home page based on authentication status
@index_template.route('/', methods=["GET","POST"])
def index():
    '''
    Display home page based on authentication status.
    '''
    if current_user.is_authenticated:
        return render_template('mainpage.html', name=current_user.name, email=current_user.email)
    else:
        if request.method == 'POST':
            email = request.form.get('InputEmail')
            password = request.form.get('InputPassword')
            remember_me = request.form.get('Remember_me')
            user_details = User.query.filter_by(email=email).first() 

            if user_details: 
                
                
                hashed_password = str(hash_string(password))
                
                if hashed_password == user_details.password:  
                    login_user(user_details)
                    resp = make_response(render_template('mainpage.html', name=user_details.name, email=user_details.email))
                    if remember_me == 'on': 
                        COOKIE_TIME_OUT = 60*60*24*7
                        resp.set_cookie('email',email, max_age=COOKIE_TIME_OUT)
                        resp.set_cookie('password',password, max_age=COOKIE_TIME_OUT)
                        resp.set_cookie('rem', 'on', max_age=COOKIE_TIME_OUT)
                        
                    else: 
                        resp = make_response(redirect('/'))
                        resp.set_cookie('email', '', expires = datetime.now(), max_age = 0)
                        resp.set_cookie('password', '', expires = datetime.now(), max_age = 0)
                        resp.set_cookie('rem', 'off', expires = datetime.now(), max_age = 0)
                    return resp
                else: 
                    if user_details.password == str(hash_string('google')): 
                        flash('Please login with Google login')
                    elif user_details.password == str(hash_string('facebook')): 
                        flash('Please login with Facebook login')
                    else: 
                        flash('Incorrect Password')
                    return redirect(url_for('index.index'))
                
                
            else: 
                flash('User not found')
                return redirect(url_for('index.index'))
                #Tell them no such user found 
        else: 
            print(request.cookies)
            return render_template('index.html')
