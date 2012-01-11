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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Infobase. If not, see <http://www.gnu.org/licenses/>.

"""A very simple Python bot.
This bot responds to simple commands. It retrieves and manipulates datas
from a database.

"""

from classes import bot

jouhou_neko = bot(socket.socket())

if __name__ == '__main__':
    jouhou_neko('#openneko)

