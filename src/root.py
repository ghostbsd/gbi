#!/usr/bin/env python

# root.py set root password.

from gi.repository import Gtk, Gdk
import os
import re
import pickle

# Directory use from the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


# Find if pasword contain only lower case and number
def lowerCase(strg, search=re.compile(r'[^a-z]').search):
    return not bool(search(strg))


# Find if pasword contain only upper case
def upperCase(strg, search=re.compile(r'[^A-Z]').search):
    return not bool(search(strg))


# Find if pasword contain only lower case and number
def lowerandNunber(strg, search=re.compile(r'[^a-z0-9]').search):
    return not bool(search(strg))


# Find if pasword contain only upper case and number
def upperandNunber(strg, search=re.compile(r'[^A-Z0-9]').search):
    return not bool(search(strg))


# Find if pasword contain only lower and upper case and
def lowerUpperCase(strg, search=re.compile(r'[^a-zA-Z]').search):
    return not bool(search(strg))


# Find if pasword contain only lower and upper case and
def lowerUpperNumber(strg, search=re.compile(r'[^a-zA-Z0-9]').search):
    return not bool(search(strg))


# Find if pasword contain only lower and upper case and
def allCharacter(strg):
    search = re.compile(r'[^a-zA-Z0-9~\!@#\$%\^&\*_\+":;\'\-]').search
    return not bool(search(strg))


class RootUser:
    def save_selection(self):
        if self.password.get_text() == self.repassword.get_text():
            f = open('%sroot' % tmp, 'wb')
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

    def password_strength(self):
        password = self.password.get_text()
        same_character_type = any(
            [
                lowerCase(password),
                upperCase(password),
                password.isdigit()
            ]
        )
        mix_character = any(
            [
                lowerandNunber(password),
                upperandNunber(password),
                lowerUpperCase(password)
            ]
        )
        if ' ' in password or '\t' in password:
            self.label3.set_text("Space not allowed")
        elif len(password) <= 4:
            self.label3.set_text("Super Weak")
        elif len(password) <= 8 and same_character_type:
            self.label3.set_text("Super Weak")
        elif len(password) <= 8 and mix_character:
            self.label3.set_text("Very Weak")
        elif len(password) <= 8 and lowerUpperNumber(password):
            self.label3.set_text("Fairly Weak")
        elif len(password) <= 8 and allCharacter(password):
            self.label3.set_text("Weak")
        elif len(password) <= 12 and same_character_type:
            self.label3.set_text("Very Weak")
        elif len(password) <= 12 and mix_character:
            self.label3.set_text("Fairly Weak")
        elif len(password) <= 12 and lowerUpperNumber(password):
            self.label3.set_text("Weak")
        elif len(password) <= 12 and allCharacter(password):
            self.label3.set_text("Strong")
        elif len(password) <= 16 and same_character_type:
            self.label3.set_text("Fairly Weak")
        elif len(password) <= 16 and mix_character:
            self.label3.set_text("Weak")
        elif len(password) <= 16 and lowerUpperNumber(password):
            self.label3.set_text("Strong")
        elif len(password) <= 16 and allCharacter(password):
            self.label3.set_text("Fairly Strong")
        elif len(password) <= 20 and same_character_type:
            self.label3.set_text("Weak")
        elif len(password) <= 20 and mix_character:
            self.label3.set_text("Strong")
        elif len(password) <= 20 and lowerUpperNumber(password):
            self.label3.set_text("Fairly Strong")
        elif len(password) <= 20 and allCharacter(password):
            self.label3.set_text("Very Strong")
        elif len(password) <= 24 and same_character_type:
            self.label3.set_text("Strong")
        elif len(password) <= 24 and mix_character:
            self.label3.set_text("Fairly Strong")
        elif len(password) <= 24 and lowerUpperNumber(password):
            self.label3.set_text("Very Strong")
        elif len(password) <= 24 and allCharacter(password):
            self.label3.set_text("Super Strong")
        elif same_character_type:
            self.label3.set_text("Fairly Strong")
        else:
            self.label3.set_text("Super Strong")

    def password_verification(self, widget, button3):
        self.password_strength()
        password = self.password.get_text()
        repassword = self.repassword.get_text()
        if password == repassword and password != "" and " " not in password:
            self.img.set_from_stock(Gtk.STOCK_YES, 5)
            button3.set_sensitive(True)
        else:
            self.img.set_from_stock(Gtk.STOCK_NO, 5)
            button3.set_sensitive(False)
