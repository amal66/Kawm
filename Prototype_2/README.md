
# Prototype 2 

This prototype shows the user flow of the app and allows users to collaborate on readings asynchronously. 

Course readings were scraped from Minerva course descriptions using helper.py and stored on resources.csv. They were then hosted on a Google Drive, and are categorized by class. Students are able to register and log in using their Minerva email or Minerva email-linked Google or Facebook account, and find relevant readings that they can read collaboratively, ask questions and get answers on with other classmates. The prototype's functional purpose is to collect user feedback and data on the user flow and utility of the question and answer feature. 


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

Open the resulting link in Firefox for the best user experience - due to scrambled security certificates to enable Google and Facebook login, Chrome may not allow opening of the locally hosted website without custom configuration

While a locally hosted version was sufficient for the purposes of this prototype, future extensions would dockerize this app and deploy it on a Heroku instance, and also incorporate the dictionary and resource embedding features. 