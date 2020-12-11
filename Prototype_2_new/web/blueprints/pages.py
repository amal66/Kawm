from flask import Blueprint, render_template
from flask import current_app as app
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin
)
from ..models import Class, File

pages_template = Blueprint('pages', __name__, template_folder='../templates',static_folder='../static')

@pages_template.route('/classselection/<classname>')
@login_required
def select_classes(classname):
    '''
    Allows the user to select classes, and add classes if classes are not already there
    '''
    user_first_name = current_user.name
    user_email = current_user.email
    classes = Class.query.all()
    class_id = Class.query.filter_by(name = classname).first().id
    files = File.query.filter_by(class_id = class_id)

    return render_template('select_classes.html', name=user_first_name, email=user_email, classes = classes, files = files )

@pages_template.route('/mainpage')
@login_required
def mainpage():
    '''
    Render mainpage with group data from user logged in.
    '''
    return render_template('mainpage.html')


@pages_template.route('/profile', methods=["GET"])
@login_required
def profile():
    '''
    Render profile page for user logged in.
    '''
    return render_template('profile.html', name=current_user.name, email=current_user.email, createdAt=current_user.createdAt)
