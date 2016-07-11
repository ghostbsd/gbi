#!/usr/local/bin//python
#
# Copyright (c) 2015 GhostBSD
#
# See COPYING for licence terms.
#
# type.py v 0.5 Thursday, Mar 28 2013 19:31:53 Eric Turgeon
#
# type.py create and delete partition slice for GhostBSD system.

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

    def partition(self, radiobutton, val):
        self.ne = val
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
        radio = Gtk.RadioButton.new_with_label_from_widget(None, "UFS full disk Configuration")
        bbox.pack_start(radio, False, True, 10)
        radio.connect("toggled", self.partition, "disk")
        self.ne = 'disk'
        pass_file = open(signal, 'w')
        pass_file.writelines(self.ne)
        pass_file.close
        radio.show()
        # box2.pack_start(radio, True, True, 10)
        radio = Gtk.RadioButton.new_with_label_from_widget(radio, "UFS Custom Configuration")
        bbox.pack_start(radio, False, True, 10)
        radio.connect("toggled", self.partition, "custom")
        radio.show()
        # box2.pack_start(radio, True, True, 10)
        radio = Gtk.RadioButton.new_with_label_from_widget(radio, "ZFS Configuration")
        bbox.pack_start(radio, False, True, 10)
        radio.connect("toggled", self.partition, "zfs")
        radio.show()
        hbox.pack_start(bbox, False, False, 50)
        # hbox.pack_start(bbox, True, True, 50)
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
        none = Gtk.RadioButton.new_with_label_from_widget(None, "Install only FreeBSD loader")
        bbox1.pack_start(none, False, True, 10)
        none.connect("toggled", self.boot_manager, "none")
        none.show()
        bsd = Gtk.RadioButton.new_with_label_from_widget(none, "Install FreeBSD boot manager + loader(MBR only)")
        bbox1.pack_start(bsd, False, True, 10)
        bsd.connect("toggled", self.boot_manager, "bsd")
        bsd.show()
        grub = Gtk.RadioButton.new_with_label_from_widget(bsd, "Install Grub2")
        bbox1.pack_start(grub, False, True, 10)
        grub.connect("toggled", self.boot_manager, "grub")
        grub.show()
        hbox.pack_start(bbox1, False, False, 50)
        self.boot = "none"
        boot = open(boot_file, 'w')
        boot.writelines(self.boot)
        boot.close()
        self.box3 = Gtk.VBox(False, 0)
        self.box3.set_border_width(0)
        self.box1.pack_start(self.box3, True, True, 0)
        return
