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



def initial_load_database(app, db): 
    with app.app_context():
        db.drop_all()
        db.create_all()

        #Load classes
        cs166 = Class(name='CS166', description='Modeling and Simulation')
        db.session.add(cs166)
        cs162 = Class(name='CS162', description='Building Powerful software applications')
        db.session.add(cs162)

        #Load resources 
        cs166_id = account = db.session.query(Class).filter_by(name = 'CS166').first().id
        cs162_id = account = db.session.query(Class).filter_by(name = 'CS162').first().id
        
        
        cs166_resource_1 = File(name='MLOps Research paper', description = 'Reading for 3.2', link = 'https://drive.google.com/file/d/1SCxJMaS3Bdf1Ul39elFhUj6N_OfRpESX/view?usp=sharing', class_id = cs166.id)
        db.session.add(cs166_resource_1)
        cs166_resource_2 = File(name='MLOps Research paper2', description = 'Reading for 3.2', link = 'https://drive.google.com/file/d/1SCxJMaS3Bdf1Ul39elFhUj6N_OfRpESX/view?usp=sharing', class_id = cs166.id)
        db.session.add(cs166_resource_2)
        cs162_resource_1 = File(name='MLOps Research paper3', description = 'Reading for 3.2', link = 'https://drive.google.com/file/d/1SCxJMaS3Bdf1Ul39elFhUj6N_OfRpESX/view?usp=sharing', class_id = cs166.id)
        db.session.add(cs162_resource_1)
        cs162_resource_2 = File(name='MLOps Research paper4', description = 'Reading for 3.2', link = 'https://drive.google.com/file/d/1SCxJMaS3Bdf1Ul39elFhUj6N_OfRpESX/view?usp=sharing', class_id = cs166.id)
        db.session.add(cs162_resource_2)

        db.session.commit()

# create database tables
from .models import db, User, Class, File

db.init_app(app)

with app.app_context():
    initial_load_database(app, db)


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
