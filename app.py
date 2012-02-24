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
import binaries

app = flask.Flask(__name__)
app.debug = True
flask.use_debugger = True

directories = {
  '' : {
    'projects' : {
      'hello' : {},
      'boop' : {},
      'floop' : {}
    },
    'github' : {
    },
    'linkedin' : {
    }
  }
}

@app.route('/<command>')
@app.route('/<command>/')
@app.route('/<command>/<arguments>')
def execute(command, arguments = ""):
  if flask.session.new or 'dir' not in flask.session:
    flask.session['dir'] = '/'
  arguments = arguments.replace("|-|", '/').replace('|_|', '.').split(";")
  env = {
    'dir' : flask.session['dir'],
    'fs' : directories
  }
  try:
    fun = getattr(binaries, command) 
    retval = { 'command' : command, 'output' : fun(arguments, env) }
    return json.dumps(retval)

  except AttributeError as e:
    if(command == 'pwd'): return flask.session['dir']
    elif(command == 'cd'):
      if(len(arguments) == 0 or arguments[0] == ''):
        flask.session['dir'] = '/'
        return ''
    elif(command == 'ls'):
      if(len(arguments) == 0 or arguments[0] == ''):
        folders = flask.session['dir'].split('/')[:-1]
        directory = directories
        for folder in folders:
          if folder in directory:
            directory = directory[folder]
        retval = ''
        for name in directory:
          retval += '<div class="fleft">' + name + '</div>'
        return retval
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
