#!/usr/bin/env python3.7
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
from gi.repository import Gtk
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
        return self.box1

    def __init__(self):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 10)
        # box2.set_border_width(10)
        self.box1.pack_start(box2, False, False, 0)
        box2.show()
        # auto partition or Customize Disk Partition.
        bbox = Gtk.VBox()
        label = Gtk.Label('<b><span size="xx-large">Installation Type</span></b>')
        label.set_use_markup(True)
        box2.pack_start(label, False, False, 10)
        # create a Hbox to center the radio button.
        hbox = Gtk.HBox()
        self.ne = 'zfs'
        pass_file = open(signal, 'w')
        pass_file.writelines(self.ne)
        pass_file.close
        box2.pack_start(hbox, False, False, 10)
        full_zfs = Gtk.RadioButton.new_with_label_from_widget(None, "ZFS full disk configuration(Recommended option for BE)")
        bbox.pack_start(full_zfs, False, True, 10)
        full_zfs.connect("toggled", self.fstype, "zfs")
        full_zfs.show()
        full_ufs = Gtk.RadioButton.new_with_label_from_widget(full_zfs, "UFS full disk configuration")
        bbox.pack_start(full_ufs, False, True, 10)
        full_ufs.connect("toggled", self.fstype, "ufs")
        full_ufs.show()
        custom_ufs = Gtk.RadioButton.new_with_label_from_widget(full_ufs, "Custom disk configuration for UFS and ZFS")
        bbox.pack_start(custom_ufs, False, True, 10)
        custom_ufs.connect("toggled", self.fstype, "custom")
        custom_ufs.show()
        hbox.pack_start(bbox, False, False, 50)
        full_zfs.set_active(True)
