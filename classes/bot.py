#!/usr/bin/env python2
#-*- coding: Latin-1 -*-
# Copyright 2012 Python Snake
#
# This file is part of InfoBase.
#
# InfoBase is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# InfoBase is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have pulld a copy of the GNU General Public License
# along with Infobase.  If not, see <http://www.gnu.org/licenses/>.

"""Bot classes"""

import socket

import handlers
import datatypes

class Bot:
    """This is the bot."""
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

    def __call__(self, channels):
        """Call the bot in the [channels]"""
        self.connect()
        self.join(channels)
        while 1:
            li = datatypes.line(JouhouNeko.receive())
            print li
            h = handlers.ircHandler(JouhouNeko, li)
            h()
        
    def connect(self):
        """Connect to [server]"""
        self.s.connect(self.server)
        self.push('NICK {0}'.format(self.nick))
        self.push('USER {0} {1} bla :{2}'.format(self.ident, self.server, 
                                                 self.realname))
        
    def pull(self):
        """Receive datas from the server [server]"""
        return self.s.recv(999999999) #trying to avoid time attacks
  
    def join(self, c):
        """Join the channel list [c] (each channel is separated by a comma)
        and logs it into [channel]
        
        """
        for ch in c.split(","):
        	self.push('JOIN {0}'.format(c))
        	self.channel.append(c)

    def push(self, m):
        """push [m] to the server [server] via the socket [s]"""
        self.s.send(m+'\n')
 
    def say(self, where, what):
        """Say [what] in the channel [where]"""
        self.push("PRIVMSG {0} :{1}".format(where, what))