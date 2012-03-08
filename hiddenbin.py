import flaskext.mail
import flask

def _mary(ignore, env):
  return 'hello, mary'

def _molly(ignore, env):
  mail = env['mail']
  ip = flask.request.remote_addr
  msg = flaskext.mail.Message("Molly Command",
                              sender="zach@zmbush.com",
                              recipients=["zabu.other@gmail.com"])
  msg.body="Someone executed the molly command from " + ip
  mail.send(msg)
  return "I love you, Molly"
