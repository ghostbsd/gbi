#!/usr/bin/env python
#
# Copyright (c) 2015 GhostBSD
#
# See COPYING for licence terms.
#
# type.py v 0.5 Thursday, Mar 28 2013 19:31:53 Eric Turgeon
#
# type.py create and delete partition slice for GhostBSD system.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import os
import os.path

# Folder use pr the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/etc/lib/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

logo = "/usr/local/lib/gbi/logo.png"
disk_file = '%sdisk' % tmp
boot_file = '%sboot' % tmp
signal = '%ssignal' % tmp
disk_list = '%sdisk-list.sh' % query
disk_info = '%sdisk-info.sh' % query
part_query = '%sdisk-part.sh' % query

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class Types():

    def fstype(self, radiobutton, val):
        self.ne = val
        pass_file = open(signal, 'w')
        pass_file.writelines(self.ne)
        pass_file.close
        return

    def get_type(self):
        return self.ne

    def get_model(self):
        return self.vbox1

    def __init__(self):
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        Title = Gtk.Label('Installation Type', name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        vbox2 = Gtk.VBox()
        hbox1 = Gtk.HBox()
        self.ne = 'zfs'
        pass_file = open(signal, 'w')
        pass_file.writelines(self.ne)
        pass_file.close
        self.vbox1.pack_start(hbox1, False, False, 10)
        full_zfs = Gtk.RadioButton.new_with_label_from_widget(None, "Full disk configuration")
        vbox2.pack_start(full_zfs, False, True, 10)
        full_zfs.connect("toggled", self.fstype, "zfs")
        full_zfs.show()
#        full_ufs = Gtk.RadioButton.new_with_label_from_widget(full_zfs, "UFS full disk configuration")
#        vbox2.pack_start(full_ufs, False, True, 10)
#        full_ufs.connect("toggled", self.fstype, "ufs")
#        full_ufs.show()
        custom_ufs = Gtk.RadioButton.new_with_label_from_widget(full_zfs, "Custom (Advanced partitioning)")
        vbox2.pack_start(custom_ufs, False, True, 10)
        custom_ufs.connect("toggled", self.fstype, "custom")
        custom_ufs.show()
        hbox1.pack_start(vbox2, False, False, 50)
        full_zfs.set_active(True)
