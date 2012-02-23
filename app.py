import os
import time
import flask
import logging
import werkzeug
import urllib2
import urllib
import subprocess
import json
import sys

app = flask.Flask(__name__)
app.debug = True
flask.use_debugger = True


@app.route('/')
def hello():
  return '<a href="dropbox">Drag and Drop test</a><br /><a href="andre">Andre\'s code</a>'

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  logger = logging.FileHandler('logfiles')
  logger.setLevel(logging.WARNING)
  app.logger.addHandler(logger)
  app.run(host='0.0.0.0', port=port)
