'''...'''

import os

import flask
import werkzeug.utils

from src.packages import budgeting

UPLOAD_FOLDER = './uploads'


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
                app.config['UPLOAD_FOLDER'],
                werkzeug.utils.secure_filename(file.filename),
            ))

        return flask.make_response('')


def register_transactions(app):
    '''...'''

    @app.route('/transactions', methods=['POST'])
    def transactions():

        transactions = budgeting.parse_transactions(
            app.config['UPLOAD_FOLDER'],
            **flask.request.get_json(),
        )

        return flask.make_response(transactions.to_dict())


if __name__ == '__main__':

    app = flask.Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

    register_endpoints(app)

    app.run()
