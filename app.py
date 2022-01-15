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

import time
import tkinter
from tkinter.constants import *

import widgets
import widgets.dialogs
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

        # Open all the files in the window
        for a in argv[1:]:
            if os.path.exists(a):
                self.windows[len(self.windows) - 1].load_file(a)

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

        # The menus
        self.menus = (
            ("_File",
                (   # Label, event, accelerator label, accelerator
                    ("_New File", "<<new-file>>", "Ctrl+N", "<Control-n>"),
                    ("_Open File", "<<open-file>>", "Ctrl+O", "<Control-o>"),
                    ("_Save File", "<<save-file>>", "Ctrl+S", "<Control-s>"),
                    ("Save File _As", "<<save-file-as>>", "Ctrl+Shift+Z", "<Control-S>"),
                    None,
                    ("_Reload Current File", "<<file-reload>>", "Ctrl+R", "<Control-r>"),
                    ("Close Current _Tab", "<<tab-close>>", "Ctrl+W", "<Control-w>"),
                    None,
                    ("_Quit", "<<quit>>", "Ctrl+Q", "<Control-q>")
                )
            ),
            ("_Edit",
                (
                    ("_Undo", "<<undo-action>>", "Ctrl+Z", "<Control-z>"),
                    ("_Redo", "<<redo-action>>", "Control+Shift+Z", "<Control-Z>")
                )
            ),
            ("_Help",
                (
                    ("_About", "<<about>>", "", ""),
                )
            )
        )

        # Create the window
        self.create_window()

        # Set the theme
        # self.tk.call("source", "/home/sam/Sun-Valley-ttk-theme/sun-valley.tcl")
        # self.tk.call("set_theme", "dark")

        self.wm_attributes("-zoomed", True)

    def action_undo(self, event=None):
        """Undo the last action."""
        self.get_current_notebook().get_current_page().undo()
    
    def action_redo(self, event=None):
        """Redo the last undone action."""
        self.get_current_notebook().get_current_page().redo()

    def check_file_saved(self, page):
        """Check the file status for the given page."""

        # Compare the page's file with the text and return True if they match
        if os.path.exists(page.file):
            with open(page.file) as f:
                fcontents = f.read()
                f.close()
            if fcontents.strip() != page.text.get_all().strip():
                return False
            else:
                return True
        else:
            return None

    def check_file_empty_untitled(self, page):
        """Return True if PAGE's file is "Untitled" and if it is empty."""
        if page.title == "Untitled":
            if page.text.get_all() == "\n" or page.text.get_all() == "":
                return True

    def close(self, event=None):
        """Close the window."""
        for tab in self.get_current_notebook().tabs:
            self.close_tab(tab=tab, actually_close=False)
        self.app.do_window_close(self)

    def close_current_tab(self, event=None):
        """Close the current tab."""
        
        # Get the response from close_tab, and close the tab if it's True
        tab = self.get_current_notebook().get_current_tab()
        if tab is not None:
            self.get_current_notebook()._close_command(tab)

    def close_tab(self, tab, actually_close=True):
        """Close the current tab, asking the user if they want to save the file."""
        
        # Check first if the file is an "Untitled" and if it is emtpy, do not
        # ask to save it
        if not self.check_file_empty_untitled(tab.child):

            # If the file is not saved, ask the user if they want to save it
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
        
        # Go through the menu tuples and add the menus.
        for m in self.menus:
            menu = tkinter.Menu(self, tearoff=False)
            for menuitem in m[1]:
                if menuitem is None:
                    menu.add_separator()
                else:
                    # Create a function for the menu item to call and bind it
                    def command(event=None, eventname=menuitem[1]):
                        self.event_generate(eventname)
                    if menuitem[3] != "":
                        self.bind(menuitem[3], command)

                    # Set the underline for the menu item's label
                    menuitemlabel = menuitem[0].replace("_", "")

                    # Add the menu item
                    menu.add_command(
                        label=menuitemlabel,
                        command=command,
                        underline=menuitem[0].index("_"),
                        accelerator=menuitem[2]
                    )

            # Set the underline for the menu's label
            menulabel = m[0].replace("_", "")

            # Add the menu
            self.menubar.add_cascade(
                label=menulabel,
                menu=menu,
                underline=m[0].index("_")
            )

        # Add the menubar to the window
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
            notebook.bind_close(self.close_tab)
            notebook.bind_control_o(self.file_open)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Bind everything
        self.bind("<<new-file>>", self.file_new)
        self.bind("<<open-file>>", self.file_open)
        self.bind("<<save-file>>", self.file_save)
        self.bind("<<save-file-as>>", self.file_save_as)
        self.bind("<<undo-action>>", self.action_undo)
        self.bind("<<redo-action>>", self.action_redo)
        self.bind("<<file-reload>>", self.reload_file)
        self.bind("<<tab-close>>", self.close_current_tab)
        self.bind("<<quit>>", self.close)
        self.bind("<<about>>", self.show_about)

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

        # Get the current page and tab
        tab = self.get_current_notebook().get_current_tab()
        page = self.get_current_notebook().get_current_page()

        # If the file does not exist, save as
        if not os.path.exists(page.file): 
            self.file_save_as()
        else:
            self.save_file(tab, page.file)

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

        # Load the contents of the file
        with open(file) as f:
            fcontents = f.read()
            f.close()

        # Create a new Page instance and load the file to it
        page = widgets.Page(self.get_current_notebook().frame)
        page.load_string(fcontents, file)
        page.file = file

        # Add the page to a new tab in the notebook
        self.get_current_notebook().add_page(page)

    def reload_file(self, event=None):
        """Reload the contents of the currently open file and redisplay them in
        the text widget."""

        # Load the contents of the file
        with open(self.get_current_notebook().get_current_page().file) as f:
            fcontents = f.read()
            f.close()

        # Reinsert the text
        text = self.get_current_notebook().get_current_page().text
        text.replace(1.0, END, fcontents)

    def save_file(self, tab, file):
        """Save the contents of TAB's Text instance to FILE."""

        # Write the contents of TAB's Page instance to the page's file
        with open(file, "w") as f:
            f.write(tab.child.text.get(1.0, END))
            f.close()

        # Set the tab's file and label to the new file
        tab.file = file
        tab.child.file = file
        tab.set_text(os.path.basename(file))

    def show_about(self, event=None):
        """Show the about dialog."""

        dialog = widgets.dialogs.AboutDialog(self, className="TKEditor")