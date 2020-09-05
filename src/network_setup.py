#!/usr/bin/env python
#
# Copyright (c) 2020 GhostBSD

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import sys
import os
networkmgr = "/usr/local/share/networkmgr"
sys.path.append(networkmgr)
from net_api import networkdictionary
logo = "/usr/local/lib/gbi/logo.png"

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class network_setup():

    def get_model(self):
        return self.vbox1

    def __init__(self):
        os.system("netcardmgr")
        print(networkdictionary())
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        Title = Gtk.Label('Network Setup', name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
