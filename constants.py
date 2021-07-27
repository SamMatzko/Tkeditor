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
"""Application constants."""

import os

# The root path
ROOT_PATH = os.path.dirname(__file__) + "/"

# Json files
JSON_APPINFO = ROOT_PATH + "data/appinfo.json"

# Error messages for handling
ERROR_CLOSE = """can't invoke "update" command: \
application has been destroyed"""

# Images
IMAGE_BUTTON_PARENT_DIR = ROOT_PATH + "icons/application/parent_dir.png"
IMAGE_DIRECTORY = ROOT_PATH + "icons/application/16x16directory.png"
IMAGE_FILE = ROOT_PATH + "icons/application/16x16file.png"

# Other file paths
BOOKMARKS = os.environ["HOME"] + "/.config/gtk-3.0/bookmarks"
USER_DIRS = os.environ["HOME"] + "/.config/user-dirs.dirs"