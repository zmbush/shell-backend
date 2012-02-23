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

@app.route('/<command>')
@app.route('/<command>/')
@app.route('/<command>/<arguments>')
def execute(command, arguments = ""):
  if flask.session.new or 'dir' not in flask.session:
    flask.session['dir'] = '/'
  arguments = arguments.split(";")

  if(command == 'pwd'): return flask.session['dir'] + "<br />"
  elif(command == 'cd' and len(arguments) == 0):
    flask.session['dir'] = '/'
    return ''
  return command + ": command not found"

@app.route('/')
def index():
  error = None
  returnVal = flask.render_template('index.html', error=error)
  return returnVal

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  logger = logging.FileHandler('logfiles')
  logger.setLevel(logging.WARNING)
  app.secret_key = 'V\\aPV@@p5_!dlUWJM-//ky&Bg()84$Us'
  app.logger.addHandler(logger)
  app.run(host='0.0.0.0', port=port)


