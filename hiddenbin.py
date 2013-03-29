import flaskext.mail
import flask
from random import choice

def _mary(ignore, env):
  return 'hello, mary'

def _molly(ignore, env):
  return "Let's stay happy forever"

def _love(ignore, env):
  return "<img src='/images/molly-and-me.jpg' />"

def _bunnies(ignore, env):
  imgs = [
    "http://25.media.tumblr.com/797ca7857d59a583c48bd3bdf399587a/tumblr_mkbsuybwbx1s4n655o1_250.gif",
    "http://25.media.tumblr.com/556ece8d2e8a37778a669fec46cfc048/tumblr_mk5wu4khsl1s2g4gpo1_500.gif",
    "http://25.media.tumblr.com/ac4cba33c1911ee5bca6e1d6eccc8848/tumblr_mk03o8tA8I1s5fgmlo1_500.gif",
    "http://25.media.tumblr.com/42be686f0a3d3d3ba1f79884941ae212/tumblr_mjjmwtfb0i1s23il0o1_250.gif",
    "http://media.tumblr.com/c5c16cd17c48cdeb5ea946c6dec3ec4d/tumblr_inline_mjh6nnIzUU1qa3yy9.gif",
    "http://25.media.tumblr.com/b34d516ad3c8b5cc60a4b1e0e829d3f3/tumblr_mjf5id4UDO1s2g4gpo1_500.gif",
    "http://25.media.tumblr.com/d5e5d7f09078b318652400ac836c3a92/tumblr_mjf4umnVW91s2g4gpo1_500.gif",
    "http://24.media.tumblr.com/d6555aee4cfe75dbad720cb754e09679/tumblr_mj64zt00qb1s5fgmlo1_500.gif",
  ]
  return "<img src='" + choice(imgs) + "' />"

def _zayd(ignore, env):
  return "Zed"

def _abbeel(ignore, env):
  return "-_-"
