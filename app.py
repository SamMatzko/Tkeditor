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
import widgets.filedialogs
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

    def check_file_saved(self, page):
        """Check the file status for the given page."""
        if os.path.exists(page.file):
            with open(page.file) as f:
                fcontents = f.read()
                f.close()
            if fcontents.strip() != page.text.get(1.0, page.text.index(END)).strip():
                return False
            else:
                return True
        else:
            return None

    def close(self):
        """Close the window."""
        for tab in self.get_current_notebook().tabs:
            self.close_tab(tab, False)
        self.app.do_window_close(self)

    def close_tab(self, tab, actually_close=True):
        """Close the current tab, asking the user if they want to save the file."""
        file_saved = self.check_file_saved(tab.child)
        if file_saved is False:
            response = tkinter.messagebox.askyesno(
                "Save file?", 
                'File "%s" has not been saved. Save?' % tab.child.title,
                parent=self
            )
            if response:
                self.file_save()
        elif file_saved is None:
            response = tkinter.messagebox.askyesno(
                "Save file?", 
                'File "%s" has not been saved. Save?' % tab.child.title,
                parent=self
            )
            if response:
                self.file_save_as()

        if actually_close:
            return True
        else:
            return False

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

        # The paned window for the notebooks
        self.paned_window = widgets.PanedWindow(self)
        self.paned_window.grid(row=0, column=0, sticky=NSEW)

        # The notebooks
        self.notebooks = [widgets.Notebook(self.paned_window)]
        for notebook in self.notebooks:
            self.paned_window.add_notebook(notebook)
            page = widgets.Page(notebook.frame)
            page2 = widgets.Page(notebook.frame)
            notebook.add_page(page, text=page.title)
            notebook.add_page(page2, text="Hello")
            notebook.bind_close(self.close_tab)
            notebook.get_current_page().bind_control_o(self.file_open)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Bind everything
        self.bind("<Control-n>", self.file_new)
        self.bind("<Control-s>", self.file_save)

    def file_new(self, event=None):
        """Create a new file."""
        self.get_current_notebook().add_page(widgets.Page(self.get_current_notebook().frame))

    def file_open(self, event=None):
        """Open an existing file."""
        response, file = widgets.filedialogs.Open(self).show()
        if response:
            self.load_file(file)

    def file_save(self, event=None):
        """Save the current file."""
        tab = self.get_current_notebook().get_current_tab()
        page = self.get_current_notebook().get_current_page()
        if not os.path.exists(page.file): 
            response, file = widgets.filedialogs.Save(self).show()
            if response:
                self.save_file(tab, file)
        else:
            self.save_file(tab, file)

    def file_save_as(self, event=None):
        """Save the current file under a different name."""
        response, file = widgets.filedialogs.SaveAs(self).show()
        if response:
            tab = self.get_current_notebook().get_current_tab()
            self.save_file(tab, file)

    def get_current_notebook(self):
        return self.notebooks[0]

    def load_file(self, file):
        """Insert the contents of FILE into the text widget."""
        with open(file) as f:
            fcontents = f.read()
            f.close()
        page = widgets.Page(self.get_current_notebook().frame)
        page.load_string(fcontents, file)
        page.file = file
        page.bind_control_o(self.file_open)
        self.get_current_notebook().add_page(page)

    def save_file(self, tab, file):
        """Save the contents of TAB's Text instance to FILE."""
        with open(file, "w") as f:
            f.write(tab.child.text.get(1.0, END))
            f.close()
        tab.file = file
        tab.set_text(os.path.basename(file))