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

"""Parses the bits received from the server
to something usable for the handlers

"""

class Line(str):
    """line class that parses datas pulld 
    from the irc server [server]
    
    """
    def __init__(self, strline):
        """
        Initialization;
        [line] - line to act on of format 
        [Action], [Msg], [User], [Chan]. Pretty verbose
        :nick!user@host action channel/user :message
        eg. :who!me@there.org PRIVMSG #whatever :blahblah
        
        """
        self.line = strline
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
            return self.line
        

    def action(self):
        if self.line.startswith('PING'):
            return 'ping'
        elif self.line.startswith(':'):
            if ' 372 ' in self.line or ' PRIVMSG ' in self.line:
                if self.line[1:].split(":", 1)[1][0] == "[" and \
                   self.line.strip()[1:].split(":", 1)[1][-1] is "]":
                    return 'cmd'
                return 'msg'
            elif ' KICK ' in self.line:
                return 'kick'
            elif ' MODE ' in self.line:
                return 'mode'
        return ''
    
    def msg(self):
        if self.Action and self.Action in 'msg kick cmd':
            return self.line[1:].strip().split(":", 1)[1]
        else:
            return ''

    def user(self):
        if self.Action:
            return self.line[1:].split(" ")[0]
        else:
            return ''
    
    def chan(self):
        if len(self.Action) > 2 and self.Action in 'msg kick cmd':
            return self.line[1:].split(" ")[2]


class Cmd(str):
    """cmd class that parses the command pulled"""
    def __init__(self, s):
        """Initialization;
        [command], [ctgry], [query], [thing], [args(list)] are verbose.
        
        """
        self.command = s.strip()[1:-1].lower().split(" ")
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
        a = []
        if len(self.command) > 2:
            for x in self.command[2:]:
                if x.startswith("-"):
                    a.append(x)
        return a
