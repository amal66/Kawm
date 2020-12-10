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
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

# _____ LOGIN MANAGER ______

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

# _____ SOCKETIO EVENTS _____
socketio = SocketIO(app)

@socketio.on('send_message')
def on_send_message(data, methods=['GET','POST']):
    '''
    Once a message is sent, commit to database (save info).
    Socket.io allows real time updating.
    '''
    # for debugging
    print('received send message event: ' + str(data))
    # save info
    with app.app_context():
        msg = Message(
            content=data['message'], group_id=data['group'], user_id=data['user'])
        db.session.merge(msg)
        db.session.commit()
    # emit recieved event back + info contained
    socketio.emit('recieved_message', data, room=data['group'])

@socketio.on('join_room')
def on_join_room(data):
    '''
    Uses socket join_room to enable user movement to group chats.
    '''
    # for debugging
    print('user  ' + str(data['user']) + 'joined:' + str(data['group']))
    room = data['group']
    join_room(room)

# # _____ ROUTES AND CONTROLLERS ____
from blueprints.index import index_template
from blueprints.login import login_template
from blueprints.user import user_template
from blueprints.pages import pages_template
from blueprints.userlist import userlist_template
from blueprints.chat import chat_template
from blueprints.groups import groups_template

app.register_blueprint(index_template)
app.register_blueprint(login_template)
app.register_blueprint(user_template)
app.register_blueprint(pages_template)
app.register_blueprint(userlist_template)
app.register_blueprint(chat_template)
app.register_blueprint(groups_template)


if __name__ == '__main__':
    socketio.run(app, keyfile=os.environ.get("KEY_PATH"), certfile=os.environ.get("CERT_PATH"))
