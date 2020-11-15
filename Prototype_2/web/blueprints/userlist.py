from flask import Blueprint, render_template
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

userlist_template = Blueprint('userlist', __name__, template_folder='../templates',static_folder='../static')

@userlist_template.route('/userlist')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
