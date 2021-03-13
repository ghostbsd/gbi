#!/usr/bin/env python
#
# Copyright (c) 2019 GhostBSD

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import os
import os.path
from partition_handler import bios_or_uefi


# Folder use pr the installer.
tmp = "/tmp/.gbi"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/etc/lib/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)


boot_file = f'{tmp}/boot'
disk_scheme = f'{tmp}/scheme'
zfs_config = f'{tmp}/zfs_config'
ufs_config = f'{tmp}/ufs_config'

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class bootManager():

    def get_model(self):
        return self.vbox1

    def boot_manager(self, radiobutton, val):
        self.boot = val
        boot = open(boot_file, 'w')
        boot.writelines(self.boot)
        boot.close()

    def __init__(self):
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        if bios_or_uefi() == "UEFI":
            loader = "UEFI"
        else:
            loader = "BIOS"
        if os.path.exists(zfs_config):
            # Disk Setup
            read = open(zfs_config, 'r')
            read_scheme = read.read()
        elif os.path.exists(ufs_config):
            # Disk Setup
            read = open(ufs_config, 'r')
            read_scheme = read.read()
        else:
            # Scheme file
            read = open(disk_scheme, 'r')
            read_scheme = read.read()
        scheme = 'GPT' if 'GPT' in read_scheme else 'MBR'
        Title = Gtk.Label('Boot Option', name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        hbox1 = Gtk.HBox()
        hbox1.show()
        self.vbox1.pack_start(hbox1, True, True, 10)
        bbox1 = Gtk.VBox()
        bbox1.show()
        self.refind = Gtk.RadioButton.new_with_label_from_widget(None, "Setup rEFInd boot manager")
        bbox1.pack_start(self.refind, False, True, 10)
        self.refind.connect("toggled", self.boot_manager, "refind")
        self.refind.show()
        if scheme == 'GPT' and loader == "UEFI":
            self.refind.set_sensitive(True)
        else:
            self.refind.set_sensitive(False)
        self.bsd = Gtk.RadioButton.new_with_label_from_widget(self.refind, "Setup FreeBSD boot manager")
        bbox1.pack_start(self.bsd, False, True, 10)
        self.bsd.connect("toggled", self.boot_manager, "bsd")
        self.bsd.show()
        if scheme == 'MBR':
            self.bsd.set_sensitive(True)
        else:
            self.bsd.set_sensitive(False)
        self.none = Gtk.RadioButton.new_with_label_from_widget(self.bsd, f"FreeBSD {loader} loader only")
        bbox1.pack_start(self.none, False, True, 10)
        self.none.connect("toggled", self.boot_manager, "none")
        self.none.show()
        hbox1.pack_start(bbox1, False, False, 50)
        self.none.set_active(True)
        self.boot = "none"
        boot = open(boot_file, 'w')
        boot.writelines(self.boot)
        boot.close()
        self.box3 = Gtk.VBox(False, 0)
        self.box3.set_border_width(0)
        self.vbox1.pack_start(self.box3, True, True, 0)
        return
