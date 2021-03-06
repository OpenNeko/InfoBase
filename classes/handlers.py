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

"""Handlers that manages the bot and the datas"""

from time import time
from datetime import timedelta

from datatypes import Cmd, Line

class IrcHandler:
    """Irc Handler - Manages the irc"""

    def __init__(self, actor, data):
        """Initialization;
        [actor] - Bot actor
        [datas] - line object to manipulate
        
        """
        self.actor = actor
        self.data = data

    def __call__(self):
        """Calls the functions associated to the data"""
        if self.data.Action and hasattr(self, 'on_' + self.data.Action):
            getattr(self, 'on_' + self.data.Action)()

    def on_kick(self):
        self.actor.join(self.actor.channel[0])

    def on_ping(self):
        self.actor.push('PONG {0}'.format(self.actor.server))

    def on_msg(self):
        if self.actor.nick.lower() in self.data.Msg.lower():
            self.actor.say(self.data.Chan, "Nya!")
 
    def on_cmd(self):
        c = Cmd(self.data.Msg)
        CmdHandler(self.actor, self.data.User, c, self.data.Chan)()

class CmdHandler:
    """Manages the commands"""
    def __init__(self, actor, wanter, cmd, chan):
        """Initilization;
        [actor] - Bot actor
        [cmd] - cmd object to manipulate
        """
        self.bot = actor
        self.cmd = cmd
        self.chan = chan
        self.wanter = wanter

    def __call__(self):
        """Calls the functions associated to the command"""
        if self.cmd.ctgry and hasattr(self, 'on_' + self.cmd.ctgry):
            getattr(self, 'on_' + self.cmd.ctgry)()
        else:
            self.bot.say(self.chan, '...') #TODO

    def on_uptime(self):
        self.bot.say(self.chan, str(timedelta(seconds=time() - 
                                    self.bot.start)))

    def on_ping(self):
        self.bot.say(self.chan, 'pong')

    def on_quit(self):
        self.bot.quit()

    def on_sudo(self):
        w = " ".join(self.cmd.command[1:]).strip().lower()
        if self.wanter.split('@')[1] in self.bot.owner_host:
            if hasattr(self, 'on_' + w):
                getattr(self, 'on_' + w)()
            else:
                self.bot.push(w)
        else:
            self.bot.say(self.chan, "No, sir.")
