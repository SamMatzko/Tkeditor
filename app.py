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

import time
import tkinter
from tkinter.constants import *

import widgets
from constants import *

class App:
    """An application manager for TKEditor."""

    def __init__(self):
        
        # The list of windows
        self.windows = []

    def do_window_close(self, window):
        """Close WINDOW."""
        self.windows.pop(self.windows.index(window))
        window.destroy()
    
    def run(self, argv):
        """Run the app."""

        # Create a new window
        self.windows.append(AppWindow(application=self, className="TKEditor"))

        # Run the main loop
        self.main()
    
    def main(self):
        """Run the main loop of the application."""
        while True:

            # Stop the app if there are no windows left
            if self.windows == []:
                break

            for window in self.windows:
                
                # Update the windows
                window.update()
                
                time.sleep(0.01)
        exit()

class AppWindow(tkinter.Tk):
    """A window class for the main application windows."""

    def __init__(self, *args, application, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        # The App instance running this window
        self.app = application

        # Set the window's main attributes
        self.wm_title("TKEditor")

        # Bind all the events
        self.wm_protocol("WM_DELETE_WINDOW", self.close)

        # Create the window
        self.create_window()

        self.wm_geometry("2000x2000")

    def close(self):
        """Close the window."""
        self.app.do_window_close(self)

    def create_menu(self):
        """Create the window menu and all it's options."""

        self.menubar = tkinter.Menu(self)
        
        # The menus
        self.file_menu = tkinter.Menu(self.menubar, tearoff=False)

        # The file menu's actions
        self.file_menu.add_command(
            label="New File...    Ctrl+N",
            command=self.file_new
        )
        self.file_menu.add_command(
            label="Open File...    Ctrl+O",
            command=self.file_open
        )
        self.file_menu.add_command(
            label="Save File    Ctrl+S",
            command=self.file_save
        )

        self.menubar.add_cascade(label="File", menu=self.file_menu, underline=0)
        self.config(menu=self.menubar)

    def create_window(self):
        """Create all the widgets for the window."""

        # Create the menu
        self.create_menu()

        # The page
        self.page = widgets.Page(self)
        self.page.grid(row=0, column=0, sticky=NSEW)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def file_new(self, event):
        """Create a new file."""
        print("new file")

    def file_open(self, event):
        """Open an existing file."""
        print("open file")

    def file_save(self, event):
        """Save the current file."""
        print("save file")