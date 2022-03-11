'''...'''

import os

import flask
import werkzeug.utils

from src.packages import budgeting


ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
UPLOAD_DIR = os.path.join(ROOT_DIR, 'uploads')


def register_endpoints(app):
    '''...'''

    register_root(app)
    register_upload(app)
    register_transactions(app)


def register_root(app):
    '''...'''

    @app.route('/')
    def root():

        return flask.render_template(
            'index.html',
            nav_options=[
                ('budgeting', 'Budgeting', 'template', None),
                ('investing', 'Investing', 'template', None),
            ],
        )


def register_upload(app):
    '''...'''

    @app.route('/upload', methods=['POST'])
    def upload():

        file = flask.request.files.get('file')

        if file is not None:
            file.save(os.path.join(
                UPLOAD_DIR,
                werkzeug.utils.secure_filename(file.filename),
            ))

        return flask.make_response('')


def register_transactions(app):
    '''...'''

    @app.route('/transactions', methods=['POST'])
    def transactions():

        transactions = budgeting.parse_transactions(
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
