#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class errorWindow():

    def on_close(self, widget):
        Gtk.main_quit()

    def __init__(self):
        window = Gtk.Window()
        window.set_border_width(8)
        window.connect("destroy", Gtk.main_quit)
        window.set_title("Installation Error")
        # window.set_icon_from_file("/usr/local/lib/gbi/image/logo.png")
        box1 = Gtk.VBox(homogeneous=False, spacing=0)
        window.add(box1)
        box1.show()
        box2 = Gtk.VBox(homogeneous=False, spacing=10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        title = Gtk.Label()
        title.set_use_markup(True)
        title_text = 'Installation has failed!'
        title.set_markup(f'<b><span size="larger">{title_text}</span></b>')
        label = Gtk.Label()
        label.set_use_markup(True)
        url = 'https://github.com/ghostbsd/ghostbsd-src/issues/new/choose'
        anchor = f"<a href='{url}'>GhostBSD issue system</a>"
        message = f"Please report the issue to {anchor}, and \n" \
            "be sure to provide /tmp/.pc-sysinstall/pc-sysinstall.log."
        label.set_markup(message)
        box2.pack_start(title, True, True, 0)
        box2.pack_start(label, True, True, 0)
        box2 = Gtk.HBox(homogeneous=False, spacing=10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        table = Gtk.Table(n_rows=1, n_columns=2, homogeneous=True)
        ok = Gtk.Button(label="Ok")
        ok.connect("clicked", self.on_close)
        table.attach(ok, 0, 2, 0, 1)
        box2.pack_start(table, True, True, 0)
        window.show_all()


errorWindow()
Gtk.main()
