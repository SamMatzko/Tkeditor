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

"""Widgets for the application."""

import tkinter
from tkinter.constants import *

class Page(tkinter.Frame):
    """The frame containing all the text field's widgets."""

    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        # The scrollbars
        self.xscrollbar = tkinter.Scrollbar(self, orient=HORIZONTAL)
        self.xscrollbar.grid(row=1, column=1, sticky=EW)
        
        self.yscrollbar = tkinter.Scrollbar(self, orient=VERTICAL)
        self.yscrollbar.grid(row=0, column=2, sticky=NS)

        # The text widget
        self.text = Text(
            self,
            xscrollcommand=self.xscrollbar.set,
            yscrollcommand=self.yscrollbar.set
        )
        self.text.grid(row=0, column=1, sticky=NSEW)

        self.xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)

        # The line numbers widget
        self.line_numbers = TextLineNumbers(self, width=10, height=1000)
        self.line_numbers.grid(row=0, column=0, sticky=W)
        self.line_numbers.attach(self.text)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.text.bind("<ButtonPress>", self.on_edit)
        self.text.bind("<KeyPress>", self.on_edit)
        self.text.bind("<<edit>>", self.line_numbers.redraw)

    def on_edit(self, event):
        self.line_numbers.after(2, self.line_numbers.redraw)
        self.text.event_generate("<<edit>>")

    def on_scroll_press(self, *args):
        self.yscrollbar.bind("<B1-Motion>", self.line_numbers.redraw)

    def on_scroll_release(self, *args):
        self.yscrollbar.unbind("<B1-Motion>", self.line_numbers.redraw)

class Text(tkinter.Text):
    """The text widget."""

    def __init__(self, *args, **kwargs):
        kwargs["wrap"] = "none"
        kwargs["background"] = "#000000"
        kwargs["foreground"] = "#ffffff"
        kwargs["insertbackground"] = "#ffffff"
        kwargs["selectbackground"] = "#ffffff"
        kwargs["selectforeground"] = "#000000"
        kwargs["font"] = "LiberationMono 10"
        tkinter.Text.__init__(self, *args, **kwargs)
        self.bind("<Control-o>", self._event_handler)
        
    def _event_handler(self, event):
        """Prevent the widget from creating a new line when Ctrl+O is hit."""
        return "break"

class TextLineNumbers(tkinter.Canvas):
    """A widget for displaying the text's line numbers."""
    
    def __init__(self, *args, **kwargs):
        tkinter.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """Redraw the line numbers."""
        self.delete(ALL)

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)
            self.config(width=len(linenum) * 10)