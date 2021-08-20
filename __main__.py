#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TKEditor is a basic chess application that uses the Stockfish chess engine.
# Copyright (C) 2021  Samuel Matzko

# This file is part of TKEditor.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
# or see <http://www.gnu.org/licenses/>

"""The main module for TKEditor."""

import json
import sys

import app
from constants import *

appinfo = json.load(open(JSON_APPINFO))
print("%s %s" % (appinfo["program_name"], appinfo["version"]))

if __name__ == "__main__":
    app = app.App()
    app.run(sys.argv)