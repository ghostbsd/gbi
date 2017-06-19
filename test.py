#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

css = """
#MyWindow {
    background-color: #F00;
    }
    """
style_provider = Gtk.CssProvider()
style_provider.load_from_data(css)
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
                                         style_provider,
                                         Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                                        )

win = Gtk.Window()
win.set_name('MyWindow')

# The Button
#button = Gtk.Button("Click Me")
#win.add(button)


win.connect("delete-event", Gtk.main_quit)

win.show_all()
Gtk.main()
