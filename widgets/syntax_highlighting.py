# TKEditor is a basic text editor
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

import ast
import json
import tkinter
from tkinter.constants import *

from constants import *

"""A class for syntax highlighting in a text widget."""

class Python:
    """Syntax highlighting for Python 3.X syntax."""

    def __init__(self, text):
        
        # Our text widget
        self.text = text

        # Load the syntax file
        self.syntax = json.load(open(JSON_COLORS))
        self.colors = self.syntax["colors"]

        # Set the tags for the text widget
        for color in self.colors:
            self.text.tag_config(color, foreground=self.colors[color])

    def _highlight_body(self, unit):
        """Highlight all the items in the body of UNIT."""
        
        for i in unit.body:

            # Set the text indexes for this body
            start_index = "%s.%s" % (i.lineno, i.col_offset)
            end_index = "%s.%s" % (i.end_lineno, i.end_col_offset)

            # Check if the unit has a "body" attribute, and if so, call this
            # method with that body
            if "body" in i.__dict__:
                self._highlight_body(i)
            # Otherwise, highlight the unit
            else:
                print((i.lineno, i.col_offset), (i.end_lineno, i.end_col_offset))

    def update(self):
        """Update the highlighting."""
        
        # Get the list of grammar syntax
        # module = ast.parse(self.text.get_all())

        # Highlight the syntax
        # self._highlight_body(module)