FROM python:3.11

WORKDIR /app

ADD Pipfile Pipfile.lock ./

# INSTALL FROM Pipefile.lock FILE
RUN pipenv install --system

ADD . .
