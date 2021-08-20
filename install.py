#!/usr/bin/env python3
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

"""Install TKEditor."""

import json
import os
import shutil
import sys

# Install only if we are on a linux-based system
if "linux" in sys.platform.lower():

    # Check if we are installing or uninstalling
    try: uninstall = sys.argv[1]
    except:
        uninstall = False
    if not uninstall:

        # The directories
        APPLICATION = os.path.dirname(__file__)
        APPLICATION_DIR = APPLICATION + "/"
        CURRENT_DIR = os.path.dirname(APPLICATION_DIR)

        # Load our version info
        with open(APPLICATION_DIR + "data/appinfo.json") as f:
            current_appinfo = json.load(f)
            f.close()
        current_version = current_appinfo["version"]
        print("Starting install of TKEditor %s..." % current_version)

        # Create the desktop file from the template
        print("Creating desktop...", end="")
        with open(APPLICATION_DIR + "data/desktop.template") as f:
            template = f.read()
            f.close()
        template = template.replace("<ICON>", APPLICATION_DIR + "icons/application/appicon.svg")
        template = template.replace("<EXEC>", APPLICATION)
        with open(APPLICATION_DIR + "data/TKEditor-code.desktop", "w") as f:
            f.write(template)
            f.close()
        print("Done")
        
        # Install the desktop
        print("Installing desktop...", end="")
        os.system("xdg-desktop-menu install %s" % APPLICATION_DIR + "data/TKEditor-code.desktop")
        os.system("xdg-desktop-icon install %s" % APPLICATION_DIR + "data/TKEditor-code.desktop")
        print("Done")

        # Install the config directory
        config_dir = "%s/.tkeditor/" % os.environ["HOME"]
        print("Installing config directory in %s..." % config_dir, end="")
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)
        with open("%sdata/settings-default.json" % APPLICATION_DIR) as f:
            default_settings = f.read()
            f.close()
        with open("%ssettings.json" % config_dir, "w") as f:
            f.write(default_settings)
            f.close()
        print("Done")
        print("Successfully installed TKEditor %s" % current_version)

    else:

        # The directories
        APPLICATION = os.path.dirname(__file__)
        APPLICATION_DIR = APPLICATION + "/"
        CURRENT_DIR = os.path.dirname(APPLICATION_DIR)

        # Load our version info
        with open(APPLICATION_DIR + "data/appinfo.json") as f:
            current_appinfo = json.load(f)
            f.close()
        current_version = current_appinfo["version"]
        print("Starting uninstall of TKEditor %s..." % current_version)
        
        # Uninstall the desktop
        print("Uninstalling desktop...", end="")
        os.system("xdg-desktop-menu uninstall %s" % APPLICATION_DIR + "TKEditor-code.desktop")
        os.system("xdg-desktop-icon uninstall %s" % APPLICATION_DIR + "TKEditor-code.desktop")
        print("Done")

        # Uninstall the config dir
        print("Removing config dir...", end="")
        shutil.rmtree("%s.tkeditor/" % os.environ("$HOME"))
        print("Done")
        print("Successfully uninstalled TKEditor.")

else:
    print("FATAL ERROR: Your system is not a Linux. This install cannot run.")