import sys
import types
import flask

def ls(folder, env):
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

def pwd(ignore, env):
  return env['dir']

def cd(folder, env):
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
        
def help(folder, env):
  retval = "Commands: <br />"
  for func in dir(sys.modules[__name__]):
    if isinstance(sys.modules[__name__].__dict__.get(func), types.FunctionType):
      retval += '<div class="fleft">' + func + '</div>'
  return retval

def echo(contents, env):
  return " ".join(contents)
