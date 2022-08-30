#!/usr/bin/env python

# root.py set root password.

from gi.repository import Gtk, Gdk
import pickle
from gbi_common import password_strength

# Directory use from the installer.
tmp = "/tmp/.gbi/"

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class RootUser:

    def save_selection(self):
        f = open(f'{tmp}root', 'wb')
        rp = self.password.get_text()
        ul = [rp]
        pickle.dump(ul, f)
        f.close()

    def __init__(self, button3):
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        Title = Gtk.Label("Administrator(root) Password", name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        box2 = Gtk.VBox(False, 0)
        box2.set_border_width(10)
        self.vbox1.pack_start(box2, False, False, 10)
        box2.show()
        # password for root.
        label = Gtk.Label('<b>Administrator (root) Password</b>')
        label.set_use_markup(True)
        label.set_alignment(.4, .2)
        table = Gtk.Table(1, 3, True)
        table.set_row_spacings(10)
        label1 = Gtk.Label("Password")
        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.password.connect("changed", self.password_verification, button3)
        label2 = Gtk.Label("Verify Password")
        self.repassword = Gtk.Entry()
        self.repassword.set_visibility(False)
        self.repassword.connect("changed", self.password_verification, button3)
        self.label3 = Gtk.Label()
        self.img = Gtk.Image()
        table.attach(label1, 0, 1, 1, 2)
        table.attach(self.password, 1, 2, 1, 2)
        table.attach(self.label3, 2, 3, 1, 2)
        table.attach(label2, 0, 1, 2, 3)
        table.attach(self.repassword, 1, 2, 2, 3)
        table.attach(self.img, 2, 3, 2, 3)
        box2.pack_start(table, False, False, 10)

    def get_model(self):
        return self.vbox1

    def password_verification(self, widget, button3):
        password = self.password.get_text()
        password_strength(password, self.label3)
        repassword = self.repassword.get_text()
        if password == repassword and password != "" and " " not in password:
            self.img.set_from_stock(Gtk.STOCK_YES, 5)
            button3.set_sensitive(True)
        else:
            self.img.set_from_stock(Gtk.STOCK_NO, 5)
            button3.set_sensitive(False)
