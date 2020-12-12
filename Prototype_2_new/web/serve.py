from flask import Flask
from datetime import datetime
from flask_login import LoginManager, UserMixin
from datetime import timedelta
import os
import sys
import pandas as pd

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

        #get all unique values from column 1, then add them to database with generic description
        #for each of them, create an id. Then create and commit all files that are related to them. 
        data = pd.read_csv('resources.csv')
        x = data.iloc[:,0]
        y = x.drop_duplicates()
        for subject in y.to_numpy(): 
            class_name = Class(name=subject, description=subject)
            db.session.add(class_name)
        
        for index, row in data.iterrows():
            class_name = row[0]
            text_name = row[1]
            url = row[2]
            description = "Readings for " + text_name
            class_id = db.session.query(Class).filter_by(name=class_name).first().id
            resource = File(name=description, description=text_name, link=url, class_id=class_id)
            db.session.add(resource)


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
