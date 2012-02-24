import sys
import types
import flask

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

def _pwd(ignore, env):
  return env['dir']

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
        
def _help(folder, env):
  retval = "Commands: <br />"
  for func in dir(sys.modules[__name__]):
    if isinstance(sys.modules[__name__].__dict__.get(func), types.FunctionType):
      retval += '<div class="fleft">' + func[1:] + '</div>'
  return retval

def _echo(contents, env):
  return " ".join(contents)

def _cat(filename, env): 
  return "Meow!"

def _10(filename, env):
  return "10<br />9<br />8<br />7<br />6<br />5<br />4<br />3<br />2<br />1" + \
         "<br />0<br />Blastoff!"

def _redirect(url, env = None):
  if len(url) > 0:
    return 'REDIRECT: ' + url[0]
  else:
    return 'No url supplied to ' + sys._getframe().f_code.co_name
  
def _linkedin(ignore, env):
  return _redirect(['http://www.linkedin.com/pub/zachary-bush/1a/a78/671'])

def _github(ignore, env):
  return _redirect(['http://www.github.com/zipcodeman'])

def _static(ignore, env):
  return _redirect(['http://www.zmbush.com/static'])

def _exit(ignore, env):
  return _redirect(['http://www.google.com/'])
