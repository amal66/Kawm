from flask import Flask
from datetime import datetime
from flask_login import LoginManager, UserMixin
from datetime import timedelta
import os
import sys

# _____ INIT + CONFIG ______
#Create a flask app
sys.path.append('web')
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

#migrate = Migrate(app, db)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['OAUTH_CREDENTIALS'] = {
    'google': {
        'id': '939432435286-hpmuqpflnbv1849vjpv4h8lnimo61oem.apps.googleusercontent.com',
        'secret': 'crl8PflESRN7xpQ6XvsX0Gxr'
    },
    'facebook': {
        'id': '236478454402152',
        'secret': '1c7eaa618d7ada24ea6d5d3ddfb66f32'
    }
}
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1)

# create database tables
from .models import db, User
db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()

# User session management setup with flask_login
login_manager = LoginManager()
login_manager.init_app(app)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403

# _____ ROUTES AND CONTROLLERS ____
from web.blueprints.index import index_template
from web.blueprints.login import login_template
from web.blueprints.user import user_template
from web.blueprints.pages import pages_template
# from web.blueprints.users import users_template # was only used for testing login


app.register_blueprint(index_template)
app.register_blueprint(login_template)
app.register_blueprint(user_template)
app.register_blueprint(pages_template)

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
