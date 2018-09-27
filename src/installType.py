#!/usr/local/bin//python
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
        # if self.ne == "ufs":
        #    self.none.set_active(True)
        #    self.grub.set_sensitive(False)
        #    self.bsd.set_sensitive(False)
        #    self.none.set_sensitive(True)
        # elif self.ne == "custom":
        #    self.grub.set_active(True)
        #    self.grub.set_sensitive(True)
        #    self.bsd.set_sensitive(True)
        #    self.none.set_sensitive(True)
        # elif self.ne == "zfs":
        #    self.grub.set_active(True)
        #    self.grub.set_sensitive(True)
        #    self.bsd.set_sensitive(False)
        #    self.none.set_sensitive(False)
        pass_file = open(signal, 'w')
        pass_file.writelines(self.ne)
        pass_file.close
        return

    def get_type(self):
        return self.ne

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
        # auto partition or Customize Disk Partition.
        bbox = Gtk.VBox()
        label = Gtk.Label('<b><span size="xx-large">Installation Type And Boot Manager</span></b>')
        label.set_use_markup(True)
        box2.pack_start(label, False, False, 10)
        # create a Hbox to center the radio button.
        hbox = Gtk.HBox()
        box2.pack_start(hbox, False, False, 10)
        full_ufs = Gtk.RadioButton.new_with_label_from_widget(None, "UFS Full Disk Configuration")
        bbox.pack_start(full_ufs, False, True, 10)
        full_ufs.connect("toggled", self.fstype, "ufs")
        self.ne = 'zfs'
        pass_file = open(signal, 'w')
        pass_file.writelines(self.ne)
        pass_file.close
        full_ufs.show()
        custom_ufs = Gtk.RadioButton.new_with_label_from_widget(full_ufs, "UFS Custom Disk Configuration")
        bbox.pack_start(custom_ufs, False, True, 10)
        custom_ufs.connect("toggled", self.fstype, "custom")
        custom_ufs.show()
        full_zfs = Gtk.RadioButton.new_with_label_from_widget(custom_ufs, "ZFS Full Disk Configuration(Recommended option for BE)")
        bbox.pack_start(full_zfs, False, True, 10)
        full_zfs.connect("toggled", self.fstype, "zfs")
        full_ufs.show()
        hbox.pack_start(bbox, False, False, 50)
        full_zfs.set_active(True)
        # Boot option.
        box3 = Gtk.VBox(False, 0)
        box3.set_border_width(10)
        self.box1.pack_start(box3, False, False, 0)
        box3.show()
        label = Gtk.Label('<b><span size="x-large">Boot Manager Option</span></b>')
        label.set_use_markup(True)
        box3.pack_start(label, False, False, 10)
        hbox = Gtk.HBox()
        hbox.show()
        box3.pack_start(hbox, True, True, 0)
        bbox1 = Gtk.VBox()
        bbox1.show()
        self.grub = Gtk.RadioButton.new_with_label_from_widget(None, "Install Grub 2")
        # bbox1.pack_start(self.grub, False, True, 10)
        self.grub.connect("toggled", self.boot_manager, "grub")
        self.grub.show()
        self.grub.set_sensitive(False)
        self.bsd = Gtk.RadioButton.new_with_label_from_widget(None, "Install FreeBSD boot manager + loader(MBR only)")
        bbox1.pack_start(self.bsd, False, True, 10)
        self.bsd.connect("toggled", self.boot_manager, "bsd")
        self.bsd.show()
        # self.bsd.set_sensitive(False)
        self.none = Gtk.RadioButton.new_with_label_from_widget(self.bsd, "BIOS: loader only UEFI: install Refind")
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
