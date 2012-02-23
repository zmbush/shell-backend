import os
import time
import flask
import logging
import werkzeug
import urllib2
import urllib
import subprocess
import eyedadata
import json
import eyeD3.tag as TAG
from mxm import *
from Song import *
from echonest import track


app = flask.Flask(__name__)
app.debug = True
flask.use_debugger = True
app.config['UPLOAD_FOLDER'] = '~/'
import sys


#@app.route('/')
#def hello():
  #return '<a href="dropbox">Drag and Drop test</a><br /><a href="andre">Andre\'s code</a>'

@app.route('/andre')
def helloAndre():
  # tracks = TRACK.search(q='Rick Astley Never Gonna Give You Up')
  # for k in range(min(3, len(tracks))):
  #   print tracks[k]
  #/return "Hello MEEEEE!"
  # return str(tracks)
  song = makeSong('Shinedown', 'Devour(Album Version)')
  if song != None:
    return str(song).replace('\n', '<br />')
  return ":("


@app.route('/')
def dropboxPage():
  error = None
  returnVal = flask.render_template('dropbox.html', error=error)
  return returnVal


@app.route('/file_upload', methods=['GET', 'POST'])
def recieveDroppedFile():
  try:
    os.mkdir(app.config['UPLOAD_FOLDER'])
  except:
    pass
  file = flask.request.files['uploaded_file']
  filename = werkzeug.secure_filename(file.filename) 
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  print path
  file.save(path)
  flask.redirect(flask.url_for('uploaded_file', filename=filename))
  newTrack = track.track_from_filename(path)
  # return newTrack.id
  retval = [newTrack.artist, newTrack.title, filename]
  return ','.join(retval)

@app.route('/error')
def displayError():
  print
  pass

@app.route('/bridge/<artist>/<song>/<filename>')
def bridgeTheGap(artist, song, filename):
  print "Artist: " + artist
  print "Song: " + song
  song = makeSong(artist, song)
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  
  try:
    if song == None:
      raise AttributeError
    eyedadata.updateFile(path, song)
  except TypeError as e:
    return json.dumps({'status':'error', 'message':e})
    # return e
  except TAG.TagException as f:
    return json.dumps({'status':'error', 'message':'Could not write ID3 tags. :('})
    # return f
  except AttributeError as g:
    return json.dumps({'status':'error', 'message':'Could not identify song. :('})
  except ValueError as h:
    return json.dumps({'status':'error', 'message':'File uploaded is not mp3. :('})

    # return g
    # print "SOMETHING WENT WRONG :("
  # print "FILENAME: " + filename
  filename = rename(filename, song.getName())
  return json.dumps({'status':'success', 'message':'/uploads/'+filename})
  # return flask.redirect('/uploads/' + filename)
  # return song.htmlStr()

def rename(filename, newName):
  path = filename.split('/')
  path[-1] = newName + '.mp3'
  newfilename = ''.join(path)
  print 'NEWFILENAME:', newfilename
  os.rename(app.config['UPLOAD_FOLDER'] + filename,
    app.config['UPLOAD_FOLDER'] + newfilename)
  return newfilename



# @app.route('/fixmeta', methods=['POST'])
# def fixMeta():
#   filename = flask.request['filename']
#   lyrics = flask.request['lyrics']


@app.route('/echo_id/<id>')
def bridgeEchoId(id):
  song = IDSong(echoID = id)
  return song.htmlStr()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
  return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename,
                                   as_attachment=True)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  logger = logging.FileHandler('logfiles')
  logger.setLevel(logging.WARNING)
  app.logger.addHandler(logger)
  app.run(host='0.0.0.0', port=port)
