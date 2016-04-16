#!/usr/bin/env python

import gi
from gi.repository import Gtk, WebKit



view = WebKit.WebView()

sw = Gtk.ScrolledWindow()
sw.add(view)
notebook = Gtk.Notebook()
notebook.set_show_tabs(False)
notebook.set_show_border(False)
label = Gtk.Label("WebKit")
vbox = Gtk.VBox()
vbox.add(sw)
notebook.insert_page(vbox, label, 0)
win = Gtk.Window()
win.set_size_request(800, 600)
win.connect("destroy", Gtk.main_quit)
win.set_title("Linux Voice browser")
win.add(notebook)
win.show_all()

view.open("/usr/local/lib/gbi/slides/welcome.html")
Gtk.main()