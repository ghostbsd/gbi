#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PyApp():

    def on_close(self, widget):
        Gtk.main_quit()

    def __init__(self):
        window = Gtk.Window()
        window.set_border_width(8)
        window.connect("destroy", Gtk.main_quit)
        window.set_title("Installation Error")
        # window.set_icon_from_file("/usr/local/lib/gbi/logo.png")
        box1 = Gtk.VBox(False, 0)
        window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        title = Gtk.Label()
        title.set_use_markup(True)
        title.set_markup('<b><span size="larger">Installation has failed!</span></b>')
        label = Gtk.Label()
        label.set_use_markup(True)
        label.set_markup("Please report the issue to <a href='http://issues.ghostbsd.org/my_view_page.php'>GhostBSD issue system</a>,\nand be sure to provide /tmp/.pc-sysinstall/pc-sysinstall.log.")
        box2.pack_start(title, True, True, 0)
        box2.pack_start(label, True, True, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        table = Gtk.Table(1, 2, True)
        ok = Gtk.Button("Ok")
        ok.connect("clicked", self.on_close)
        table.attach(ok, 0, 2, 0, 1)
        box2.pack_start(table, True, True, 0)
        window.show_all()


PyApp()
Gtk.main()
