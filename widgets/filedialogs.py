# TKEditor is a basic Python IDE
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

"""File dialogs."""

import os
import sys
import time
import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter.constants import *

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from constants import *

class _FileDialog(tkinter.Toplevel):
    """The base class for the file dialogs."""

    def __init__(self, *args, title="Choose a file.", initialdir=os.environ["HOME"]  + "/", askoverwrite=True, confirmexsists=True, showhidden=True, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.wm_title(title)
        self.wm_geometry("800x600")
        self.wm_protocol("WM_DELETE_WINDOW", self._cancel)

        self.initialdir = initialdir
        self.askoverwrite = askoverwrite
        self.confirmexsists = confirmexsists
        self.show_hidden_files = showhidden

        # What to return when the dialog is closed
        self.response = "duh"

        # The currently-selected file
        self.current_file = self.initialdir

        # Create the window
        self._create_window()

        self.focus_force()

    def _cancel(self):
        """Cancel the dialog."""
        self.destroy()
        self.response = None

    def _create_buttons(self):
        """Create the buttons at the top of the dialog."""

        # The buttons' frame
        self.button_frame = tkinter.Frame(self)
        self.button_frame.grid(row=0, column=0, columnspan=3, sticky=NSEW)
        
        # The cancel button
        self.cancel_button = tkinter.Button(
            self.button_frame,
            text="Cancel",
            command=self._cancel
        )
        self.cancel_button.grid(row=0, column=0, sticky=W)

        # The current-directory label
        self.dir_entry = tkinter.Entry(self.button_frame)
        self.dir_entry.insert(0, self.initialdir)
        self.dir_entry.grid(row=0, column=1, sticky=EW)

        # The previous-directory button and it's image
        self.parent_dir_image = tkinter.PhotoImage(file=IMAGE_BUTTON_PARENT_DIR)
        self.parent_dir_button = tkinter.Button(
            self.button_frame,
            image=self.parent_dir_image,
            command=self._show_parent_directory
        )
        self.parent_dir_button.grid(row=0, column=2, sticky=EW)

        # The ok button
        self.ok_button = tkinter.Button(
            self.button_frame,
            text="Ok",
            command=self._ok
        )
        self.ok_button.grid(row=0, column=3, sticky=E)

        self.button_frame.columnconfigure(1, weight=1)

    def _create_tree(self):
        """Create the file dialog's file tree."""

        # The list of files and directories
        self.files_tree = ttk.Treeview(
            self,
            columns=("size", "modified"),
            yscrollcommand=self.scrollbar.set
        )
        self.files_tree.grid(row=1, column=1, sticky=NSEW)

        # The name column
        self.files_tree.heading("#0", text="Name")
        self.files_tree.column("#0", anchor=W, minwidth=200)
        
        # The size column
        self.files_tree.heading("size", text="Size")
        self.files_tree.column("size", anchor=W, minwidth=100)

        # The modified column
        self.files_tree.heading("modified", text="Modified")
        self.files_tree.column("modified", anchor=W, minwidth=300)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def _create_window(self):
        """Add all the widgets to the dialog."""

        # The images
        self.dir_image = tkinter.PhotoImage(file=IMAGE_DIRECTORY)
        self.file_image = tkinter.PhotoImage(file=IMAGE_FILE)

        # The scrollbar
        self.scrollbar = tkinter.Scrollbar(self)
        self.scrollbar.grid(row=1, column=2, sticky=NS)

        # Add the buttons to the top
        self._create_buttons()

        # Create the tree
        self._create_tree()
        self.scrollbar.config(command=self.files_tree.yview)

    def _get_dirs_parent_dir(self, directory):
        """Return a path representing the parent directory of DIRECTORY."""
        if len(directory) > 1:
            return os.path.normpath(os.path.dirname(directory[:len(directory) - 1])) + "/"
        else:
            return directory

    def _get_sorted_directory_contents(self, directory):
        """Return two sorted lists containing all the contents of DIRECTORY."""
        
        filesanddirs = []
        dirslist = []
        fileslist = []

        # Get the files and directories
        filesanddirs = os.listdir(directory)

        # Append them to the proper lists
        for i in filesanddirs:
            if os.path.isdir(directory + i):
                if not self.show_hidden_files:
                    if os.path.basename(i).startswith("."):
                        pass
                    else:
                        dirslist.append(directory + i)
                else:
                    dirslist.append(directory + i)
            else:
                if not self.show_hidden_files:
                    if os.path.basename(i).startswith("."):
                        pass
                    else:
                        fileslist.append(directory + i)
                else:
                    fileslist.append(directory + i)

        fileslist.sort()
        dirslist.sort()
        return fileslist, dirslist

    def _ok(self):
        """Close the dialog and return OK status."""
        self.current_file = self.dir_entry.get()
        if self.confirmexsists:
            if os.path.isfile(self.current_file):
                if self.askoverwrite:
                    response = tkinter.messagebox.askyesno(
                        "Replace File?",
                        'File "%s" already exists. Replacing it will overwrite it!' % (
                            os.path.basename(self.current_file)
                        ),
                        parent=self
                    )
                    if response == True:
                        self.response = True
                        self.destroy()
                    else:
                        pass
                else:
                    self.response = True
                    self.destroy()
            else:
                tkinter.messagebox.showinfo(
                    "No file selected",
                    "No file was selected.",
                    parent=self
                )
        else:
            self.response = True
            self.destroy()

    def _on_dir_click(self, event):
        """Handle stuff for when a directory is double-clicked."""
        self._show_directory(self.files_tree.selection()[0])

    def _on_file_click(self, event):
        """Handle stuff for when a file is double-clicked."""
        self._ok()

    def _on_file_single_click(self, event):
        """Handle stuff for when a file is clicked."""
        self.files_tree.after(2, self._set_dir_entry_to_file)

    def _set_dir_entry_text(self, text):
        """Set the directory entry's text to TEXT."""
        self.dir_entry.delete(0, END)
        self.dir_entry.insert(0, text)

    def _set_dir_entry_to_file(self):
        """Set the directory entry's text to the currently selected file."""
        sf = self.files_tree.selection()[0]
        if sf.endswith("/"):
            sf = sf[:len(sf) - 1]
        self._set_dir_entry_text(sf)
        self.current_file = sf

    def _show_directory(self, directory):
        """Show the contents of DIRECTORY."""

        # Delete all the old rows
        for i in self.files_tree.get_children():
            self.files_tree.delete(i)

        # Get the sorted list of files and directories
        files, dirs = self._get_sorted_directory_contents(directory)

        for d in dirs:
            self.files_tree.insert(
                "",
                END,
                d + "/",
                text=os.path.basename(d),
                values=("", "%s" % time.ctime(os.path.getmtime(d))),
                image=self.dir_image,
                tags=("dir")
            )

        if  self.confirmexsists:
            for f in files:
                self.files_tree.insert(
                    "",
                    END,
                    f + "/",
                    text=os.path.basename(f),
                    values=("%s" % os.path.getsize(f), "%s" % time.ctime(os.path.getmtime(f))),
                    image=self.file_image,
                    tags=("file")
                )
            self.files_tree.tag_bind("file", "<Button-1>", self._on_file_single_click)
            self.files_tree.tag_bind("file", "<Double-Button-1>", self._on_file_click)

        self.files_tree.tag_bind("dir", "<Double-Button-1>", self._on_dir_click)

        # Set directory button and label
        self.parent_dir_button.file_path = self._get_dirs_parent_dir(directory)
        self._set_dir_entry_text(directory)

        # Select the first item
        self.files_tree.selection_set(self.files_tree.get_children()[0])

    def _show_parent_directory(self):
        """Show the parent directory."""
        self._show_directory(self.parent_dir_button.file_path)

    def show(self):
        """Show the dialog."""
        self._show_directory(self.initialdir)
        while True:
            try: self.update()
            except tkinter.TclError as e:
                break
            if self.response != "duh":
                self.destroy()
                break
        return self.response, self.current_file

class Open(_FileDialog):
    """Open a file."""

    def __init__(self, *args, title="Open", initialdir=os.environ["HOME"] + "/", askoverwrite=False, confirmexsists=True, showhidden=True, **kwargs):
        _FileDialog.__init__(
            self,
            *args,
            title=title,
            initialdir=initialdir,
            askoverwrite=askoverwrite,
            confirmexsists=confirmexsists,
            showhidden=showhidden,
            **kwargs
        )

class Save(_FileDialog):
    """Save a file."""

    def __init__(self, *args, title="Save", initialdir=os.environ["HOME"] + "/", askoverwrite=True, confirmexsists=False, showhidden=True, **kwargs):
        _FileDialog.__init__(
            self,
            *args,
            title=title,
            initialdir=initialdir,
            askoverwrite=askoverwrite,
            confirmexsists=confirmexsists,
            showhidden=showhidden,
            **kwargs
        )

class SaveAs(_FileDialog):
    """Save a file under a different name."""

    def __init__(self, *args, title="Save As", initialdir=os.environ["HOME"] + "/", askoverwrite=True, confirmexsists=True, showhidden=True, **kwargs):
        _FileDialog.__init__(
            self,
            *args,
            title=title,
            initialdir=initialdir,
            askoverwrite=askoverwrite,
            confirmexsists=confirmexsists,
            showhidden=showhidden,
            **kwargs
        )

if __name__ == "__main__":
    dialog = Open()
    print(dialog.show())