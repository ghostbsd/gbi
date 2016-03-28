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

    def __init__(self):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        self.box1.pack_start(box2, True, True, 0)

        box2.show()
        # auto partition or Customize Disk Partition.
        bbox = Gtk.VBox()
        label = Gtk.Label()
        box2.pack_start(label, False, False, 0)
        label = Gtk.Label(
            '<b><span size="xx-large">Installation Type</span></b>')
        label.set_use_markup(True)
        box2.pack_start(label, False, False, 10)
        # create a Hbox to center the radio button.
        hbox = Gtk.HBox()
        box2.pack_start(hbox, True, True, 10)
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
        hbox.pack_start(bbox, True, True, 100)
        # hbox.pack_start(bbox, True, True, 50)
        label = Gtk.Label()
        box2.pack_start(label, False, False, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        self.box1.pack_start(box2, False, False, 0)
        box2.show()
        return
