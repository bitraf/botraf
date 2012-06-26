#!/usr/bin/env python
"""
pyngelyng - from:
  UliBot - A Basic Uli-Oriented IRC Bot
  License: GPL 2; share and enjoy!
  Authors: 
     Sean B. Palmer, inamidst.com
     Suw Charman, chocnvodka.blogware.com
  Augmented by:
     Dave Menninger
  Requirements: 
     http://inamidst.com/proj/suwbot/ircbot.py

Vi har ikke noe kode igjen fra suwbot med mindre de har endret noe i
ircbot.py, noe de sikkert har.
"""

import ircbot, rpcgw
import urllib, sys # XXX

debug = False
nickname = 'pyngelyng'
channel = '#ping.uio.no'
prefix = "http://www.ping.uio.no/~pingbot/cgi-bin/"
server_host = 'irc.ifi.uio.no'
server_port = 6667
rpcgw_host = 'localhost'
rpcgw_port = 9042

import time, select
def conn_read_and_close(conn, timeout = 30):
   starttime = time.time()
   s = ""
   while time.time() - starttime < timeout:
      readyreads, ignor, ignored = select.select([conn], [], [], 1)
      if readyreads != []:
         nbytes = 1
         tmp = conn.read()
         s = s + tmp
         if len(tmp) < nbytes:
            conn.close()
            return s.split("\n")

   conn.close()
   return ["Error: Timeout exceeded"]


def command(sender, nick, text):
   """Run <text> issued by <nick>.  <text> is the full text, i.e.
   ",hepp hei hopp"

   TODO: Fix timeout
   """
   # strip prefix ','
   text = text[1:]

   # First word in text is filename, the rest is parameters
   pos = text.find(' ')

   file = ""
   params = ""

   if pos != -1:
     file = text[:pos]
     params = text[1+pos:]
   else:
     file = text

   url = prefix + file + ".cgi?" + urllib.urlencode({'nick': nick, 
'params': params})
   try:
     connection = urllib.urlopen(url)
  
     lines = 1
     recipient = sender

     if connection.headers.has_key("x-max-lines"):
       lines = int(connection.headers["x-max-lines"])

     if connection.headers.has_key("x-recipient"):
       recipient = connection.headers["x-recipient"]

     output = conn_read_and_close(connection)

     if len(output) == 0: return [""]

     # Crop output, 
     return output[:lines], recipient
   except:
     return ['Error'], sender


def pyngelyng(host, port, channels, nick=nickname):
   p = ircbot.Bot(nick=nick, channels=channels)

   def f_command(m, origin, (cmd, channel), text, p=p):
      """Run any command over HTTP"""
      if debug: p.notice(origin.sender, ',command: %s' % text)

      lines, recipient = command(origin.sender, origin.nick, text)

      for line in lines:
        p.notice(recipient, line)

   p.rule(f_command, ',command', "^,.+" )

   import thread
   thread.start_new_thread(rpcgw.rpcgw, (p, rpcgw_host, rpcgw_port, channel))

   p.run(host, port)

def main():
   if "--daemon" in sys.argv:
      ircbot.setDebug(False)
      ircbot.doubleFork()
      debug = False
   else:
      ircbot.setDebug(True)
   
   while 1:
	   pyngelyng(server_host, server_port, [channel])

if __name__=='__main__':
   main()
