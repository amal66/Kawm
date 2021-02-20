
## Set up environment
Set up the environment by running: 
    $ pip3 install virtualenv
    $ virtualenv -p python3 .venv
    $ source .venv/bin/activate
    $ pip3 install -r requirements.txt

## Run Application
Start the server by running:
    $ export SQLALCHEMY_DATABASE_URI='sqlite:///web.db'
    $ export FLASK_ENV=development
    $ export FLASK_APP=web
    $ export FLASK_RUN_CERT=adhoc
    $ python3 -m flask run

## Docker
    $docker build -t kawm:latest .
    $docker run --publish 5000:5000 --detach --name 285 kawm
