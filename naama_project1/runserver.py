"""
This script runs the naama_project1 application using a development server.
"""

from os import environ
from naama_project1 import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.config['SECRET_KEY'] = 'naama'
    app.run(HOST, PORT)
