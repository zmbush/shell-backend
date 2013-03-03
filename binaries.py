import sys
import types
import flask
import urllib

desc = {}

desc['ls'] = \
"""
  list  
"""
def _ls(folder, env):
  currentDir = env['dir']
  selection = currentDir.split('/')[:-1]
  location = env['fs']
  if len(folder) > 0:
    fold = folder[0]
    for f in fold.split('/'):
      if f == '.':
        continue
      elif f == '..':
        selection.pop()
      elif f == '':
        continue
      else:
        selection.append(f)
  for f in selection:
    if f in location:
      location = location[f]
    else:
      return folder[0] + ": no such file or directory"
  retval = ''
  for entry in location:
    retval += '<div class="fleft">' + entry + '</div>'
  return retval

desc['pwd'] = \
"""
  list  
"""
def _pwd(ignore, env):
  return env['dir']

desc['cd'] = \
"""
  list  
"""
def _cd(folder, env):
  selection = env['dir'].split('/')[:-1]
  location = env['fs']
  if len(folder) > 0 and not folder[0] == '':
    fold = folder[0]
    for f in fold.split('/'):
      if f == '.':
        continue
      elif f == '..':
        selection.pop()
      elif f == '':
        continue
      else:
        selection.append(f)
  else:
    selection = ['']
  for f in selection:
    if f in location:
      location = location[f]
    else:
      return folder[0] + ": no such file or directory"
  retval = '/'.join(selection) + '/'
  flask.session['dir'] = retval
  return retval
        
desc['help'] = \
"""
  Display this help message
"""
def _help(folder, env):
  retval = "Commands: <br />"
  for func in dir(sys.modules[__name__]):
    if isinstance(sys.modules[__name__].__dict__.get(func), types.FunctionType):
      retval += '<div class="fleftCommand">' + func[1:] +                 \
                '</div><div class="fleftDesc">' + desc[func[1:]] + '</div>'
      # retval += '<div class="fleft">' + func[1:] + '</div>'
  return retval

desc['echo'] = \
"""
  Display what was passed in.
"""
def _echo(contents, env):
  return " ".join(contents)

desc['cat'] = \
"""
  Fluffy
"""
def _cat(filename, env): 
  return "Meow!"

desc['10'] = \
"""
  Countdown
"""
def _10(filename, env):
  return "10<br />9<br />8<br />7<br />6<br />5<br />4<br />3<br />2<br />1" + \
         "<br />0<br />Blastoff!"

desc['redirect'] = \
"""
  Move to another url
"""
def _redirect(url, env = None):
  if len(url) > 0:
    return 'REDIRECT: ' + url[0]
  else:
    return 'No url supplied to ' + sys._getframe().f_code.co_name
  
desc['linkedin'] = \
"""
  load my linkedin page
"""
def _linkedin(ignore, env):
  return _redirect(['http://www.linkedin.com/in/zmbush'])

desc['github'] = \
"""
  Load my github page
"""
def _github(ignore, env):
  return _redirect(['http://www.github.com/zipcodeman'])

desc['static'] = \
"""
  Redirect to the static page
"""
def _static(ignore, env):
  return _redirect(['http://static.zmbush.com/'])

desc['exit'] = \
"""
  Leave zmbush.com
"""
def _exit(ignore, env):
  return _redirect(['http://www.google.com/'])

desc['emacs'] = \
"""
  A text editor
"""
def _emacs(ignore, env):
  return "I'd rather not..."

desc['vim'] = \
"""
  A text editor
"""
def _vim(ignore, env):
  return "I would love to"

users = {
    'zach' : 'bush',
    'mary' : 'stufflebeam',
    'andre' : 'crabb'
  }
desc['login'] = \
"""
  Logs a user in. 
"""
def _login(arguments, env):
  if len(arguments) == 0 or arguments[0] == '':
    return "You must specify a username"
  elif len(arguments) == 1 and arguments[0] != '':
    return "GETQ: password"
  elif len(arguments) == 2:
    uname = arguments[0]
    passwd = arguments[1]
    if uname in users:
      if passwd == users[uname]:
        flask.session['user'] = uname
    return flask.session['user']

desc['whoami'] = \
"""
  Returns current user
"""
def _whoami(arguments, env):
  return env['user']

desc['logout'] = \
"""
  Return to a guest account
"""
def _logout(arguments, env):
  flask.session['user'] = 'guest'
  return 'guest'

desc['projects'] = \
"""
  List my Projects
"""
def _projects(arguments, env):
  return urllib.urlopen('http://static.zmbush.com/output/projects').read()

desc['resume'] = \
"""
  Display my resume
"""
def _resume(arguments, env):
  return _redirect(['static/resume.pdf'])

desc['hello'] = \
"""
  How are you?
"""
def _hello(ignore, env):
  return "Hi!"
