'''Launches the app on http://127.0.0.1:5000.'''

import os
from typing import *

import flask
import werkzeug.utils

from src.packages import transactions as transactions_lib


ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
UPLOAD_DIR = os.path.join(ROOT_DIR, 'uploads')


def register_endpoints(
    app: flask.Flask,
) -> None:
    '''Create endpoints.'''

    register_root(app)
    register_upload(app)
    register_transactions(app)


def register_root(
    app: flask.Flask,
) -> None:
    '''Create an endpoint for the main page.'''

    @app.route('/')
    def root() -> Any:
        '''Serve the main page.'''

        template = flask.render_template(
            'index.html',
            nav_options=[
                ('budgeting', 'Budgeting', 'template', None),
                ('investing', 'Investing', 'template', None),
            ],
        )

        return flask.make_response(template)


def register_upload(
    app: flask.Flask,
) -> None:
    '''Create an endpoint for upload requests.'''

    @app.route('/upload', methods=['POST'])
    def upload() -> Any:
        '''Handle a request to upload files.'''

        file = flask.request.files.get('file')

        if file is not None:
            file.save(os.path.join(
                UPLOAD_DIR,
                werkzeug.utils.secure_filename(file.filename),
            ))

        return flask.make_response('')


def register_transactions(
    app: flask.Flask,
) -> None:
    '''Create an endpoint for transaction data requests.'''

    @app.route('/transactions', methods=['POST'])
    def transactions() -> Any:
        '''Handle a request for transaction data.'''

        transactions = transactions_lib.request_transactions(
            DATA_DIR,
            UPLOAD_DIR,
            **flask.request.get_json(),
        )

        return flask.make_response(transactions.to_dict())


if __name__ == '__main__':

    app = flask.Flask(__name__)

    for directory in {
        DATA_DIR,
        UPLOAD_DIR,
    }:
        if not os.path.exists(directory):
            os.mkdir(directory)

    register_endpoints(app)

    app.run()
