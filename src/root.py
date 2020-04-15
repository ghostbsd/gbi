#!/usr/bin/env python3.7

# root.py set root password.

from gi.repository import Gtk
import os
import re
from subprocess import Popen
import pickle

# Directory use from the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
if not os.path.exists(tmp):
    os.makedirs(tmp)


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
def allCharacter(strg, search=re.compile(r'[^a-zA-Z0-9~\!@#\$%\^&\*_\+":;\'\-]').search):
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
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 0)
        box2.set_border_width(10)
        self.box1.pack_start(box2, False, False, 10)
        box2.show()
        # title.
        ttext = "Administrator(root) Password"
        Title = Gtk.Label("<b><span size='xx-large'>%s</span></b>" % ttext)
        Title.set_use_markup(True)
        box2.pack_start(Title, False, False, 10)
        # password for root.
        label = Gtk.Label('<b>Administrator (root) Password</b>')
        label.set_use_markup(True)
        label.set_alignment(.4, .2)
        table = Gtk.Table(1, 3, True)
        table.set_row_spacings(10)
        label1 = Gtk.Label("Password")
        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.password.connect("changed", self.passwdstrength)
        label2 = Gtk.Label("Verify Password")
        self.repassword = Gtk.Entry()
        self.repassword.set_visibility(False)
        self.repassword.connect("changed", self.passwdVerification, button3)
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
        return self.box1

    def passwdstrength(self, widget):
        passwd = self.password.get_text()
        if len(passwd) <= 4:
            self.label3.set_text("Super Weak")
        elif len(passwd) <= 8:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.label3.set_text("Super Weak")
            elif lowerandNunber(passwd):
                self.label3.set_text("Very Weak")
            elif upperandNunber(passwd):
                self.label3.set_text("Very Weak")
            elif lowerUpperCase(passwd):
                self.label3.set_text("Very Weak")
            elif lowerUpperNumber(passwd):
                self.label3.set_text("Fairly Weak")
            elif allCharacter(passwd):
                self.label3.set_text("Weak")
        elif len(passwd) <= 12:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.label3.set_text("Very Weak")
            elif lowerandNunber(passwd):
                self.label3.set_text("Fairly Weak")
            elif upperandNunber(passwd):
                self.label3.set_text("Fairly Weak")
            elif lowerUpperCase(passwd):
                self.label3.set_text("Fairly Weak")
            elif lowerUpperNumber(passwd):
                self.label3.set_text("Weak")
            elif allCharacter(passwd):
                self.label3.set_text("Strong")
        elif len(passwd) <= 16:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.label3.set_text("Fairly Weak")
            elif lowerandNunber(passwd):
                self.label3.set_text("Weak")
            elif upperandNunber(passwd):
                self.label3.set_text("Weak")
            elif lowerUpperCase(passwd):
                self.label3.set_text("Weak")
            elif lowerUpperNumber(passwd):
                self.label3.set_text("Strong")
            elif allCharacter(passwd):
                self.label3.set_text("Fairly Strong")
        elif len(passwd) <= 20:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.label3.set_text("Weak")
            elif lowerandNunber(passwd):
                self.label3.set_text("Strong")
            elif upperandNunber(passwd):
                self.label3.set_text("Strong")
            elif lowerUpperCase(passwd):
                self.label3.set_text("Strong")
            elif lowerUpperNumber(passwd):
                self.label3.set_text("Fairly Strong")
            elif allCharacter(passwd):
                self.label3.set_text("Very Strong")
        elif len(passwd) <= 24:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.label3.set_text("Strong")
            elif lowerandNunber(passwd):
                self.label3.set_text("Fairly Strong")
            elif upperandNunber(passwd):
                self.label3.set_text("Fairly Strong")
            elif lowerUpperCase(passwd):
                self.label3.set_text("Fairly Strong")
            elif lowerUpperNumber(passwd):
                self.label3.set_text("Very Strong")
            elif allCharacter(passwd):
                self.label3.set_text("Super Strong")
        elif len(passwd) > 24:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.label3.set_text("Fairly Strong")
            else:
                self.label3.set_text("Super Strong")

    def passwdVerification(self, widget, button3):
        if self.password.get_text() == self.repassword.get_text() and self.password.get_text() != "":
            self.img.set_from_stock(Gtk.STOCK_YES, 5)
            button3.set_sensitive(True)
        else:
            self.img.set_from_stock(Gtk.STOCK_NO, 5)
            button3.set_sensitive(False)
