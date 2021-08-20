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

"""Widgets for the application."""

import json
import os
import sys
import tkinter
import tkinter.ttk
from tkinter.constants import *

# Add the main app directory to sys.path so we can import constants.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from . import syntax_highlighting
from constants import *

class _NotebookTab(tkinter.LabelFrame):
    """The tab widget for the Notebook."""

    def __init__(self, master, child, **kwargs):
        tkinter.LabelFrame.__init__(self, master, relief=SUNKEN)
        self.config(relief=SUNKEN)

        # The tab label attributes
        try: self.label_text = kwargs["text"]
        except:
            self.label_text = ""
        try: self.close_command = kwargs["closecommand"]
        except:
            pass

        # Our window's child
        self.child = child

        self.bind("<Button-1>", self.select_command)

        # The label
        self.label = tkinter.Label(self, text=self.label_text)
        self.label.bind("<Button-1>", self.select_command)
        self.label.grid(row=0, column=0, sticky=W)

        # The close button
        self.close_button = tkinter.Button(
            self,
            text="X",
            relief=FLAT,
            command=self.close_command
        )
        self.close_button.grid(row=0, column=1, sticky=E)

        self.columnconfigure(0, weight=1)

    def bind_close(self, func):
        """Bind the tab's close to a call of FUNC."""
        self.bound_close_func = func

    def bind_select(self, func):
        """Bind the tab's selection to a call of FUNC."""
        self.bound_select_func = func

    def close_command(self):
        """Close us."""
        response = self.bound_close_func(self)
        if response:
            self.child.destroy()
            self.destroy()

    def select_command(self, event=None):
        """Select us."""
        self.child.focus_set()
        self.config(relief=SUNKEN)
        self.bound_select_func(self)

    def set_text(self, text):
        """Set the label to text."""
        self.label_text = text
        self.label.config(text=self.label_text)

    # Unbound method placeholders
    def bound_close_func(self, tab):
        return True

    def bound_select_func(self, tab):
        pass

class Notebook(tkinter.Frame):
    """A custom notebook widget with close buttons, tab scrolling, etc."""

    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        # The list of tabs. These have their children as built-in variables
        self.tabs = []

        # The current tab
        self.current_tab = 0

        # The tabs' text's scrollbar
        self.scrollbar = tkinter.Scrollbar(self, orient=HORIZONTAL)
        self.scrollbar.grid(row=1, column=0, sticky=EW)

        # Functions to call at tab closing and <Control-o>
        self.bound_close_func = self.close_func
        self.bound_control_o_func = self.control_o_func

        # The tabs' text
        self.tabs_text = tkinter.Text(
            self,
            bg="#d9d9d9",
            height=2,
            relief=FLAT,
            cursor="left_ptr",
            state=DISABLED,
            wrap=NONE,
            xscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.tabs_text.xview)
        self.tabs_text.grid(row=0, column=0, sticky=N+EW)

        # The frame for the child
        self.frame = tkinter.Frame(self)
        self.frame.grid(row=2, column=0, sticky=NSEW)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

    def _close_command(self, tab):
        """Close TAB and remove it's everything."""

        # Get the OK from our bound_close_func before closing
        response = self.bound_close_func(tab)
        if response:

            # Remove TAB from the list of tabs
            self.tabs.pop(self.tabs.index(tab))

            # Remove all the tab's widgets, including itself
            tab.child.pack_forget()
            tab.child.destroy()
            tab.destroy()

            # Select the previous tab, if there is one
            if len(self.tabs) != 0:
                self._select_command(self.tabs[len(self.tabs) - 1])
        
        return True

    def _see_tabs_text_end(self):
        """Scroll the tabs text so that the user can see the last tab."""
        self.tabs_text.see(END)

    def _see_tabs_text_index(self, index=None):
        """Scroll the tabs text so that the user can see the tab at INDEX.
        INDEX is set to the current tab if omitted."""
        if index is None:
            index = self.current_tab
        self.tabs_text.see(float("1.%s" % index))

    def _select_command(self, tab):
        """Select TAB and show it's child."""

        # Deselect all the other tabs and hide their children
        for other_tab in self.tabs:
            other_tab.config(relief=FLAT)
            other_tab.child.pack_forget()

        # Select this tab
        tab.config(relief=SUNKEN)
        tab.child.pack(expand=True, fill=BOTH)
        self.current_tab = self.tabs.index(tab)

        # Set the focus to this tab's text widget
        tab.child.text.focus_set()

        # Scroll the tabs_text so that we can see the tab
        self.after(4, self._see_tabs_text_index())

    def add_page(self, child, **kwargs):
        """Create a new tab with child CHILD."""
        try: text = kwargs["text"]
        except:
            text = ""

        # Create a new tab widget
        tab = _NotebookTab(self.tabs_text, child, text=text)
        tab.bind_select(self._select_command)
        tab.bind_close(self._close_command)

        # Add the tab wiget to the text
        self.tabs_text.config(state=NORMAL)
        self.tabs_text.window_create(END, window=tab)
        self.tabs_text.config(state=DISABLED)

        # Add the tab's child to the window as the currently open page
        child.pack(expand=True, fill=BOTH)
        child.bind_control_o(self.bound_control_o_func)
        child.text.bind_control_shift_left(self.tab_previous)
        child.text.bind_control_shift_right(self.tab_next)

        # Add the tab to our list, configure it, and select it
        self.tabs.append(tab)
        tab.set_text(child.title)
        self.current_tab = self.tabs.index(tab)
        self._select_command(tab)
        self.after(2, self._see_tabs_text_end)

        # Focus the text widget so the user can instantly start typing
        child.text.focus_set()

    def bind_close(self, func):
        """Bind the close of a tab to a call of FUNC."""
        self.bound_close_func = func

    def bind_control_o(self, func):
        """Bind \<Control-o\> to a call of FUNC, and keep the Text instances from 
        creating newlines."""
        self.bound_control_o_func = func

        # We bind all the tabs
        for tab in self.tabs:
            tab.child.bind_control_o(func)

    def get_current_page(self):
        """Return the child of the currently selected tab."""
        return self.get_current_tab().child

    def get_current_tab(self):
        """Return the currently selected tab."""
        try: return self.tabs[self.current_tab]
        except IndexError:
            return None

    def remove_tab(self, tab):
        """Remove the tab TAB."""
        self._close_command(tab)

    def tab_next(self, event=None):
        """Switch to the next tab."""
        if len(self.tabs) > 1:
            try:
                self._select_command(self.tabs[self.current_tab + 1])
            except IndexError:
                self._select_command(self.tabs[0])

    def tab_previous(self, event=None):
        """Switch to the previous tab."""
        if len(self.tabs) > 1:
            try:
                self._select_command(self.tabs[self.current_tab - 1])
            except IndexError:
                self._select_command(len(self.tabs) - 1)

    # Placeholders for unbound methods
    def close_func(self, tab):
        return True

    def control_o_func(self):
        return "break"

class StatusBar(tkinter.Frame):
    """The status widget at the bottom of the window."""

    def __init__(self, *args, **kwargs):
        kwargs["relief"] = RAISED
        tkinter.Frame.__init__(self, *args, **kwargs)

        # The application info
        self.appinfo = json.load(open(JSON_APPINFO))

        # The version label
        self.version_label = tkinter.Label(self, text=self.appinfo["version"])
        self.version_label.pack(side=RIGHT)

        sep = tkinter.ttk.Separator(self, orient=VERTICAL)
        sep.pack(padx=3, side=RIGHT, fill=Y)

        # The line/column label
        self.index_label = tkinter.Label(self, text="Ln: 1 Col: 0")
        self.index_label.pack(side=RIGHT)

        sep = tkinter.ttk.Separator(self, orient=VERTICAL)
        sep.pack(padx=3, side=RIGHT, fill=Y)

        # The tab size label
        self.tab_size_label = tkinter.Label(
            self,
            text="Spaces: 4"
        )
        self.tab_size_label.bind("<Button-1>", self.set_tab_size)
        self.tab_size_label.pack(side=RIGHT)

    def bind_set_tab_size(self, func):
        """Bind a click on the tab size label to a call of FUNC."""
        self.set_tab_size_func = func

    def set_tab_size(self, event=None):
        """Set the tab size."""
        tabsize = self.set_tab_size_func()
        self.tab_size_label.config(text="Spaces: %s" % tabsize)

    def update_index_label(self, line, column):
        """Update the index label."""
        label = "Ln: %s Col: %s" % (line, column)
        self.index_label.config(text=label)

    # Placeholders for unbound methods

    def set_tab_size_func(self):
        pass

class Page(tkinter.Frame):
    """The frame containing all the text field's widgets."""

    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        # The scrollbars
        self.xscrollbar = tkinter.Scrollbar(self, orient=HORIZONTAL)
        self.xscrollbar.grid(row=1, column=1, sticky=EW)
        
        self.yscrollbar = tkinter.Scrollbar(self, orient=VERTICAL)
        self.yscrollbar.grid(row=0, column=2, sticky=NS)

        # The line numbers widget
        self.line_numbers = TextLineNumbers(self, width=10, height=1000)
        self.line_numbers.grid(row=0, column=0, sticky=W)

        # The text widget
        self.text = Text(
            self,
            line_numbers=self.line_numbers,
            xscrollcommand=self.xscrollbar.set,
            yscrollcommand=self.yscrollbar.set
        )
        self.text.bind_update(self.update_accessories)
        self.text.grid(row=0, column=1, sticky=NSEW)

        self.xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)

        # The status bar
        self.status_bar = StatusBar(self)
        self.status_bar.bind_set_tab_size(self.set_tab_size)
        self.status_bar.grid(row=2, column=0, columnspan=3, sticky=EW)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Bind the events
        self.text.bind("<Control-z>", self.undo)
        self.text.bind("<Control-Z>", self.redo)
        self.yscrollbar.bind("<Button-1>", self.on_scroll_press)

        # The file we currently have open
        self.file = "Untitled"

        # Our title
        self.title = os.path.basename(self.file)

    def bind_control_o(self, func):
        self.text.bind_control_o(func)

    def load_string(self, string, file):
        """Load STRING into the text widget."""

        # Clear the old text and insert the new text
        self.text.delete(1.0, END)
        self.text.insert(1.0, string)

        # Reset the undo stack and redraw the line numbers
        self.text.edit_reset()
        self.line_numbers.redraw()

        # Set our file to be the currently open file, and set the title as such
        self.file = file
        self.title = os.path.basename(file)
        self.set_title(self.title)

    def on_scroll_press(self, *args):
        self.yscrollbar.bind("<B1-Motion>", self.line_numbers.redraw)

    def on_scroll_release(self, *args):
        self.yscrollbar.unbind("<B1-Motion>", self.line_numbers.redraw)

    def redo(self, event=None):
        """Redo the last undone action."""
        try:
            self.text.edit_redo()
        except tkinter.TclError:
            pass
        self.after(2, self.line_numbers.redraw())
        return "break"

    def set_tab_size(self):
        """Get the tab size and set it."""

        # Show the popover for the tab size
        tab_size = SetTabSizePopover(
            self.text,
            initialsize=self.text.tabwidth,
        ).show()
        self.text.focus_set()
        self.text.set_tab_width(tab_size)
        return tab_size

    def undo(self, event=None):
        """Undo the last action."""
        try:
            self.text.edit_undo()
        except tkinter.TclError:
            pass
        self.after(2, self.line_numbers.redraw())
        return "break"

    def update_accessories(self):
        """Update all our accessories, like the status bar."""
        line, col = self.text.index(INSERT).split(".")
        self.status_bar.update_index_label(line, col)

    # Placeholders for unbound methods
    def set_title(self, title):
        pass

class PanedWindow(tkinter.PanedWindow):
    """A custom PanedWindow widget with a list of Notebook instances."""

    def __init__(self, *args, **kwargs):
        tkinter.PanedWindow.__init__(self, *args, **kwargs)

        self.notebooks = []

    def add_notebook(self, notebook):
        """Add a notebook in a new pane."""
        self.add(notebook) 
        self.notebooks.append(notebook)

class _Popover(tkinter.Frame):
    """The popover for the tab size."""

    def __init__(self, *args, **kwargs):
        kwargs["cursor"] = "arrow"
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.focus_force()

        self.bind("<FocusOut>", self.close)
        self.bind("<Key-Escape>", self.close)

        self.end = False

    def close(self, event=None):
        """Close the popover."""
        self.destroy()
        self.end = True

    def show(self):
        """Show the popover."""
        while True:
            if not self.end:
                self.update()
            else:
                break

class SetTabSizePopover(_Popover):
    """The popover for the tab size."""

    def __init__(self, *args, initialsize, **kwargs):
        _Popover.__init__(self, *args, **kwargs)
        self.focus_force()

        self.bind("<FocusOut>", self.close)
        self.bind("<Key-Escape>", self.close)

        self.end = False

        # The tab size
        self.tabsize = initialsize

        # Create the widgets
        self._create_window()

        self.grid(row=0, column=0, sticky=N)

    def _create_window(self):
        """Create the window."""
        
        # The label
        self.label = tkinter.Label(
            self,
            text="Select indentation size (in spaces)"
        )
        self.label.grid(row=0, column=0, sticky=NW)

        # The buttons
        self.size_two_button = tkinter.Button(
            self,
            text="2",
            relief=FLAT,
            command=lambda: self.set_size(size=2)
        )
        self.size_two_button.grid(row=1, column=0, sticky=EW)

        self.size_four_button = tkinter.Button(
            self,
            text="4",
            relief=FLAT,
            command=lambda: self.set_size(size=4)
        )
        self.size_four_button.grid(row=2, column=0, sticky=EW)

        self.size_eight_button = tkinter.Button(
            self,
            text="8",
            relief=FLAT,
            command=lambda: self.set_size(size=8)
        )
        self.size_eight_button.grid(row=3, column=0, sticky=EW)

        self.columnconfigure(0, weight=1)

    def set_size(self, *args, size):
        self.tabsize = size
        self.close()

    def show(self):
        """Show the popover."""
        while True:
            if not self.end:
                self.update()
            else:
                break
        return self.tabsize

class Text(tkinter.Text):
    """The text widget."""

    def __init__(self, *args, line_numbers, tabwidth=4, **kwargs):

        # Configure all the keyword arguments to customize the widget
        kwargs["wrap"] = "none"
        kwargs["background"] = "#000000"
        kwargs["foreground"] = "#ffffff"
        kwargs["insertbackground"] = "#ffffff"
        kwargs["selectbackground"] = "#ffffff"
        kwargs["selectforeground"] = "#000000"
        kwargs["font"] = "LiberationMono 10"
        kwargs["undo"] = True

        # Initialize the widget and bind it's events
        tkinter.Text.__init__(self, *args, **kwargs)
        self.tabwidth = tabwidth
        self.bind("<Alt-Down>", self._move_line_down)
        self.bind("<Alt-Up>", self._move_line_up)
        self.bind("<ButtonPress>", self._on_button_press)
        self.bind("<Control-a>", self._select_all)
        self.bind("<Control-K>", self._delete_current_line)
        self.bind("<Control-o>", self._event_handler)
        self.bind("<Control-Shift-Left>", self._ctrl_shift_left)
        self.bind("<Control-Shift-Right>", self._ctrl_shift_right)
        self.bind("<KeyPress>", self._on_key_press)
        self.bind("<Key-Tab>", self._on_tab)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Our syntax highlighting manager
        self.syntax = syntax_highlighting.Python(self)

        # Our line numbers widget
        self.line_numbers = line_numbers
        self.line_numbers.attach(self)
    
    def _ctrl_shift_left(self, event=None):
        self.control_shift_left_func()
        return "break"

    def _ctrl_shift_right(self, event=None):
        self.control_shift_right_func()
        return "break"

    def _delete_current_line(self, event=None):
        """Delete the line where the cursor is."""
        i = self.index(INSERT)
        ilist = i.split(".")
        line_start = ilist[0] + ".0"
        line_end = ilist[0] + ".end+1c"

        # Insert a separator in the undo stack, so that the user can undo the
        # line deletion all by itself
        self.edit_separator()
        self.delete(line_start, line_end)
        
    def _event_handler(self, event):
        """Prevent the widget from creating a new line when Ctrl+O is hit."""
        self.control_o_func()
        return "break"

    def _get_line_above(self, index):
        """Return a tuple of start and end indexes for the line above INDEX.
        Return False if the line is line 1."""
        index = str(index)
        ilist = index.split(".")
        if ilist[0] == "1":
            return False
        else:
            return self._get_line_start_end(str(int(ilist[0]) - 1) + ".0")

    def _get_line_below(self, index):
        """Return a tuple of start and end indexes for the line below INDEX."""
        index = str(index)
        ilist = index.split(".")
        return self._get_line_start_end(str(int(ilist[0]) + 1) + ".0")

    def _get_line_last(self):
        """Return the start index for the last line."""
        return self._get_line_start_end(
            float(self.index(END)) - 1.0
        )[0]
        
    def _get_line_start_end(self, index):
        """Return the start and end indexes for the line at INDEX."""
        index = str(index)
        ilist = index.split(".")
        return ilist[0] + ".0", ilist[0] + ".end"

    def _move_line_down(self, event=None):
        """Swap the places of the current line and the one below it."""
        i = self.index(INSERT)
        ilist = i.split(".")

        # Make sure we can actually move up (that is, the current line is not
        # the first)
        if int(ilist[0]) < float(self._get_line_last()):
            
            # Get the contents of this line and the line above it
            current_contents = self.get(*self._get_line_start_end(i))
            above_contents = self.get(*self._get_line_below(i))

            # Replace the lines
            self.replace(*self._get_line_start_end(i), above_contents)
            self.replace(*self._get_line_below(i), current_contents)

    def _move_line_up(self, event=None):
        """Swap the places of the current line and the one above it."""
        i = self.index(INSERT)
        ilist = i.split(".")

        # Make sure we can actually move up (that is, the current line is not
        # the first)
        if int(ilist[0]) > 1:
            
            # Get the contents of this line and the line above it
            current_contents = self.get(*self._get_line_start_end(i))
            above_contents = self.get(*self._get_line_above(i))

            # Replace the lines
            self.replace(*self._get_line_start_end(i), above_contents)
            self.replace(*self._get_line_above(i), current_contents)

    def _on_button_press(self, event=None):
        """Update the line numbers and syntax highlighting."""
        self.after(2, self.update_accessories)

    def _on_key_press(self, event=None):
        """Update the line numbers and syntax highlighting."""
        self.after(2, self.update_accessories)

    def _on_tab(self, event):
        self.insert(INSERT, " " * self.tabwidth)
        self.update_accessories()
        return "break"

    def _select_all(self, event=None):
        """Select all of the text."""
        self.tag_add("sel", 1.0, "end-1c")
        self.mark_set(INSERT, 1.0)
        self.see(INSERT)
        return "break"

    def bind_control_o(self, func):
        """Bind \<Control-o\> to a call of FUNC."""
        self.control_o_func = func

    def bind_control_shift_left(self, func):
        """Bind \<Control-Shift-Left\> to a call of FUNC."""
        self.control_shift_left_func = func

    def bind_control_shift_right(self, func):
        """Bind \<Control-Shift-Right\> to a call of FUNC."""
        self.control_shift_right_func = func

    def bind_update(self, func):
        """Bind a call of self.update_accessories to a call of FUNC."""
        self.update_accessories_func = func

    def get_all(self):
        """Return all our text."""
        return self.get(1.0, END)

    def set_tab_width(self, width):
        """Set the tab width to WIDTH."""
        self.tabwidth = width

    def update_accessories(self, event=None):
        """Update the syntax highlighting."""
        self.line_numbers.redraw()
        self.syntax.update()
        self.update_accessories_func()

    # Placeholders for unbound methods

    def control_o_func(self, event=None):
        pass

    def control_shift_left_func(self, event=None):
        pass
    
    def control_shift_right_func(self, event=None):
        pass

    def update_accessories_func(self):
        pass

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