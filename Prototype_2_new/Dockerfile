###
FROM python:3.8.0
COPY requirements.txt .

MAINTAINER Your Name "amal@minerva.kgi.edu"

# Set the working directory to /web
WORKDIR /web

# Copy the current directory contents into the container at /web
ADD . /web

RUN pip3 install -r requirements.txt
ENV SQLALCHEMY_DATABASE_URI='sqlite:///web.db'
ENV FLASK_ENV=development
ENV FLASK_APP=web
ENV FLASK_RUN_CERT=adhoc

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "-m", "flask", "run"]
