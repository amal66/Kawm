from flask import Blueprint, render_template
from flask import current_app as app

pages_template = Blueprint('pages', __name__, template_folder='../templates',static_folder='../static')

@pages_template.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')

@pages_template.route('/mgevents')
def manage_events():
    return render_template('manage_events.html')
