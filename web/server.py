"""
Main entry point for the web server.
"""
from __future__ import absolute_import
import os

import flask

import util


APP = flask.Flask('new-awesome',
                  static_folder=os.path.join(util.ROOT, 'web', 'static'),
                  template_folder=os.path.join(util.ROOT, 'web', 'templates'))
APP.config.update({
    'DEBUG': True,
})
APP.config.from_envvar('FLASK_SETTINGS', silent=True)


@APP.route('/')
def index():
    """
    The main web page.
    """
    return flask.render_template('index.html')


if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=5001)
