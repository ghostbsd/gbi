#!/usr/local/bin//python
#
# Copyright (c) 2019 GhostBSD

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import os.path
from partition_handler import bios_or_uefi


# Folder use pr the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/etc/lib/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

logo = "/usr/local/lib/gbi/logo.png"
boot_file = '%sboot' % tmp
disk_schem = '%sscheme' % tmp
zfs_config = '%szfs_config' % tmp
ufs_config = tmp + 'ufs_config'


class bootManager():

    def get_model(self):
        return self.box1

    def boot_manager(self, radiobutton, val):
        self.boot = val
        boot = open(boot_file, 'w')
        boot.writelines(self.boot)
        boot.close()

    def __init__(self):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 10)
        # box2.set_border_width(10)
        self.box1.pack_start(box2, False, False, 0)
        box2.show()
        if bios_or_uefi() == "UEFI":
            loader = "UEFI"
        else:
            loader = "BIOS"
        if os.path.exists(zfs_config):
            # Disk Setup
            read = open(zfs_config, 'r')
            schem = read.read()
            # os.remove(zfs_config)
        elif os.path.exists(ufs_config):
            # Disk Setup
            read = open(ufs_config, 'r')
            schem = read.readlines()
        else:
            # Sheme sheme
            read = open(disk_schem, 'r')
            schem = read.read()
        if 'GPT' in schem:
            scheme = 'GPT'
        else:
            scheme = 'MBR'
        label = Gtk.Label('<b><span size="x-large">Boot Option</span></b>')
        label.set_use_markup(True)
        box2.pack_start(label, False, False, 10)
        hbox = Gtk.HBox()
        hbox.show()
        box2.pack_start(hbox, True, True, 0)
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
        hbox.pack_start(bbox1, False, False, 50)
        self.none.set_active(True)
        self.boot = "none"
        boot = open(boot_file, 'w')
        boot.writelines(self.boot)
        boot.close()
        self.box3 = Gtk.VBox(False, 0)
        self.box3.set_border_width(0)
        self.box1.pack_start(self.box3, True, True, 0)
        return
