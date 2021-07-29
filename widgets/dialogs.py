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

"""Application-specific dialogs."""

import json
import tkinter
from tkinter.constants import *

from constants import *

class AboutDialog(tkinter.Toplevel):
    """A simple dialog showing simple info on TKEditor."""

    def __init__(self, *args, className=None, **kwargs):
        kwargs["class"] = className
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.wm_geometry("300x200")
        self.wm_title("About TKEditor")
        self.wm_resizable(False, False)

        # The app info
        self.appinfo = json.load(open(JSON_APPINFO))

        # The label for the icon
        self.icon = tkinter.PhotoImage(master=self, file=IMAGE_APPLICATION)
        self.icon = self.icon.subsample(2)
        self.icon_label = tkinter.Label(self, image=self.icon)
        self.icon_label.pack(expand=YES, fill=BOTH)

        # The other labels
        
        self.name_label = tkinter.Label(
            self,
            text="TKEditor",
            font="Default 20 bold",
            justify=CENTER
        )
        self.name_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.version_label = tkinter.Label(self, text=self.appinfo["version"])
        self.version_label.pack(side=TOP, expand=YES, fill=BOTH)

        self.copyright_label = tkinter.Label(self, text=self.appinfo["copyright"])
        self.copyright_label.pack(side=TOP, expand=YES, fill=BOTH)

    def show(self):
        """Show the dialog."""
        self.mainloop()

if __name__ == "__main__":
    __name__ = 2
    w = tkinter.Tk()
    dialog = AboutDialog(tk, transientfor=w)
    dialog.show()
    exit()