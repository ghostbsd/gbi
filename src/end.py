#!/usr/bin/env python3.6

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from subprocess import Popen

lyrics = """Installation is complete. You need to restart the
computer in order to use the new installation.
You can continue to use this live media, although
any changes you make or documents you save will
not be preserved on reboot."""


class PyApp():

    def on_reboot(self, widget):
        Popen('shutdown -r now', shell=True)
        Gtk.main_quit()

    def on_close(self, widget):
        Gtk.main_quit()

    def __init__(self):
        window = Gtk.Window()
        window.set_border_width(8)
        window.connect("destroy", Gtk.main_quit)
        window.set_title("Installation Completed")
        window.set_icon_from_file("/usr/local/lib/gbi/logo.png")
        box1 = Gtk.VBox(False, 0)
        window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        label = Gtk.Label(lyrics)
        box2.pack_start(label, True, True, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        table = Gtk.Table(1, 2, True)
        restart = Gtk.Button("Restart")
        restart.connect("clicked", self.on_reboot)
        Continue = Gtk.Button("Continue")
        Continue.connect("clicked", self.on_close)
        table.attach(Continue, 0, 1, 0, 1)
        table.attach(restart, 1, 2, 0, 1)
        box2.pack_start(table, True, True, 0)
        window.show_all()


PyApp()
Gtk.main()
