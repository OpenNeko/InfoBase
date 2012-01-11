#!/usr/bin/env python
#-*- coding: Latin-1 -*-
#  Copyright 2012 Python Snake

 """A very simple Python bot.
 
 This bot responds to simple commands. It retrieves and manipulates datas 
 from a database.
 
 """

import socket
from time import time
from datetime import timedelta

#import sqlite3 #Useless... for now

class bot:
    """This is the bot.
    
    """
    
    def __init__(self, sock):
        """Initialization;
        Attributes:
            Logging
                [start]: start time
                [channel]: joined channels
            Identification
                [nick]![ident]@hostmask: [realname]
            [server]: server to connect
            [owner]: hostmask of the owner
            [s]: the socket to use
            
        """
        self.start = time()
        self.server = ("holmes.freenode.net", 6667)
        self.nick = 'JouhouNeko'
        self.realname = '=3'
        self.ident = 'cat'
        self.owner = 'unaffiliated/pythonsnake'
        self.s = sock
        self.channel = []
        
    def connect(self):
        """Connect to [server]
        
        """
        self.s.connect(self.server)
        self.Send('NICK {0}'.format(self.nick))
        self.Send('USER {0} {1} bla :{2}'.format(self.ident, self.server, 
                                                 self.realname))
        
    def receive(self):
        """Receive datas from the server [server]
        
        """
        return self.s.recv(999999999) #trying to avoid time attacks
  
    def join(self, c):
        """Join the channel list [c] (each channel is separated by a comma)
        and logs it into [channel]
        
        """
        for ch in c.split(","):
        	self.Send('JOIN {0}'.format(c))
        	self.channel.append(c)

    def Send(self, m):
        """Send [m] to the server [server] via the socket [s]
        
        """
        self.s.send(m+'\n')
 
    def say(self, where, what):
        """Say [what] in the channel [where]
        
        """
        self.Send("PRIVMSG {0} :{1}".format(where, what))


class ircHandler:
    """Irc Handler - Manages the irc 
    
    """

    def __init__(self, actor, datar):
        """Initialization;
        [actor] - Bot actor
        [datar] - line object to manipulate
        
        """
        self.actor = actor
        self.datar = datar

    def __call__(self):
        """Calls the functions associated to the data
        
        """
        if self.datar.Action and hasattr(self, 
                                         'on_' + self.datar.Action):
            getattr(self, 'on_' + self.datar.Action)()
        else:
            pass #TODO

    def on_kick(self):
        self.actor.join(self.actor.channel[0])

    def on_ping(self):
        self.actor.Send('PONG')

    def on_msg(self):
        if self.actor.nick.lower() in self.datar.Msg.lower():
            self.actor.say(self.datar.Chan, "Nya!")
 
    def on_cmd(self):
        c = cmd(self.datar.Msg.lower())
        cmdHandler(self.actor, c, self.datar.Chan)()

class cmdHandler:
    """Manages the commands
    
    """
    def __init__(self, actor, cmd, chan):
        """Initilization;
        [actor] - Bot actor
        [cmd] - cmd object to manipulate
        """
        self.bot = actor
        self.cmd = cmd
        self.chan = chan

    def __call__(self):
        """Calls the functions associated to the command
        
        """
        if self.cmd.ctgry and hasattr(self, 'on_' + self.cmd.ctgry):
            getattr(self, 'on_' + self.cmd.ctgry)()
        else:
            self.bot.say(self.chan, '...') #TODO

    def on_uptime(self):
        self.bot.say(self.chan, str(timedelta(seconds=time() - 
                                    self.bot.start)))

    def on_ping(self):
        self.bot.say(self.chan, 'Pong')
          

class line(str):
    """line class that parses datas received 
    from the irc server [server]
    
    """
    def __init__(self, strline):
        """
        Initialization;
        [l] - line to act on of format 
        [Action], [Msg], [User], [Chan]. Pretty verbose
        :nick!user@host action channel/user :message
        eg. :who!me@there.org PRIVMSG #whatever :blahblah
        
        """
        self.l = strline
        self.Action = self.action()
        self.Msg = self.msg()
        self.User = self.user()
        self.Chan = self.chan()

    def __str__(self):
        """Prints the line
        [Action] from [User]: [Msg]
        
        """
        if self.Action and self.Msg:
            return "{0} from {1}: {2}".format(self.Action, self.User, self.Msg)
        else:
            return self.l
        

    def action(self):
        if self.l.startswith('PING'):
            return 'ping'
        elif self.l.startswith(':'):
            if ' 372 ' in self.l or ' PRIVMSG ' in self.l:
                if self.l[1:].split(":", 1)[1][0] == "[" and \
                   self.l.strip()[1:].split(":", 1)[1][-1] is "]":
                    return 'cmd'
                return 'msg'
            elif ' KICK ' in self.l:
                return 'kick'
            elif ' MODE ' in self.l:
                return 'mode'
        return ''
    
    def msg(self):
        if self.Action and self.Action in 'msg kick cmd':
            return self.l[1:].strip().split(":", 1)[1]
        else:
            return ''

    def user(self):
        if self.Action:
            if self.Action == 'ping':
                return self.l.split(":")[1].strip()
            else:
                return self.l[1:].split(" ")[0]
        else:
            return ''
    
    def chan(self):
        if len(self.Action) > 2 and self.Action in 'msg kick cmd':
            return self.l[1:].split(" ")[2]


class cmd(str):
    """cmd class
    
    """
    def __init__(self, s):
        """Initialization;
        [command], [ctgry], [query], [thing], [args(list)] are verbose.
        
        """
        self.command = s.strip()[1:-1].split(" ")
        self.ctgry = self.ctg()
        self.query = self.qry()
        self.thing = self.thi()
        self.args = self.arg()

    def __str__(self):
        """Prints the command
        From [ctgry], do [query] with [thing]~ [args]
        
        """
        return "From {0}, do {1} with {2}~ {3}".format(self.ctgry, self.query, 
                                                       self.thing, self.args)

    def thi(self):
        if len(self.command) > 2:
            return self.command[2]
        else:
            return ''

    def ctg(self):
        if self.command:
            return self.command[0]
        else:
            return ''

    def qry(self):
        if len(self.command) > 1:
            return self.command[1] 
        else:
            return ''

    def arg(self):
        a=[]
        if len(self.command) > 2:
            for x in self.command[2:]:
                if x.startswith("-"):
                    a.append(x)
        return a
        


#Deploying the bot. 
JouhouNeko = bot(socket.socket())
JouhouNeko.connect()
JouhouNeko.join('#openneko,##theonewhohelps')

while 1:
    li = line(JouhouNeko.receive())
    print li
    h = ircHandler(JouhouNeko, li)
    h()
    
    

