#!/usr/bin/env python
#
# Copyright (c) 2010-2013, GhostBSD. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistribution's of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistribution's in binary form must reproduce the above
#    copyright notice,this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# 3. Neither then name of GhostBSD Project nor the names of its
#    contributors maybe used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES(INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# user.py v 1.4 Friday, January 17 2014 Eric Turgeon
#
# user.py create users and set root password.

from gi.repository import Gtk
import os
import re
from subprocess import Popen
import pickle

# Directory use from the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)
to_cfg = 'python %screate_cfg.py' % installer


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


# Find if pasword contain only lowercase, uppercase numbers and some special character.
def allCharacter(strg, search=re.compile(r'[^a-zA-Z0-9~\!@#\$%\^&\*_\+":;\'\-]').search):
    return not bool(search(strg))


class AddUser:
    def save_selection(self):
        f = open('%suser' % tmp, 'wb')
        uname = self.user.get_text()
        name = self.name.get_text()
        if self.password.get_text() == self.repassword.get_text():
            up = self.password.get_text()
            shell = self.sh
            hf = '/home/%s' % self.user.get_text()
            hst = self.host.get_text()
            ul = [uname, name, up, shell, hf, hst]
            pickle.dump(ul, f)
            f.close()

    def on_shell(self, widget):
        SHELL = widget.get_active_text()
        if SHELL == 'sh':
            self.sh = '/bin/sh'
        elif SHELL == 'csh':
            self.sh = '/bin/csh'
        elif SHELL == 'tcsh':
            self.sh = '/bin/tcsh'
        elif SHELL == 'fish':
            self.sh = '/usr/local/bin/fish'
        elif SHELL == 'bash':
            self.sh = '/usr/local/bin/bash'
        elif SHELL == 'rbash':
            self.sh = '/usr/local/bin/rbash'
        elif SHELL == 'zsh':
            self.sh = '/usr/local/bin/zsh'
        elif SHELL == 'ksh':
            self.sh = '/usr/local/bin/ksh93'


    def userAndHost(self, widget):
        username = self.name.get_text().split()
        self.host.set_text("%s.ghostbsd-pc.home" % username[0].lower())
        self.user.set_text(username[0].lower())

    def __init__(self, button3):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 0)
        box2.set_border_width(10)
        self.box1.pack_start(box2, False, False, 0)
        box2.show()
        # title.
        ttext = "User Setup"
        Title = Gtk.Label("<b><span size='xx-large'>%s</span></b>" % ttext)
        Title.set_use_markup(True)
        box2.pack_start(Title, False, False, 0)
        # password for root.
        box2 = Gtk.VBox(False, 10)
        # box2.set_border_width(10)
        self.box1.pack_start(box2, False, False, 0)
        box2.show()
        label = Gtk.Label('<b>User Account</b>')
        label.set_use_markup(True)
        label.set_alignment(.2, .2)
        Username = Gtk.Label("User name")
        self.user = Gtk.Entry()
        self.label2 = Gtk.Label("Real name")
        self.name = Gtk.Entry()
        self.name.connect("changed", self.userAndHost)
        self.labelpass = Gtk.Label("Password")
        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.password.connect("changed", self.passwdstrength)
        self.label4 = Gtk.Label("Verify Password")
        self.repassword = Gtk.Entry()
        self.repassword.set_visibility(False)
        self.repassword.connect("changed", self.passwdVerification, button3)
        self.label5 = Gtk.Label("Shell")
        shell = Gtk.ComboBoxText()
        self.sh = '/usr/local/bin/fish'
        shell.append_text('sh')
        shell.append_text('csh')
        shell.append_text('tcsh')
        shell.append_text('fish')
        shell.append_text('bash')
        shell.append_text('rbash')
        shell.append_text('ksh')
        shell.append_text('zsh')
        shell.set_active(3)
        shell.connect("changed", self.on_shell)
        label = Gtk.Label('<b>Set Hostname</b>')
        label.set_use_markup(True)
        label.set_alignment(0, .5)
        table = Gtk.Table(1, 3, True)
        table.set_row_spacings(10)
        pcname = Gtk.Label("Hostname")
        self.host = Gtk.Entry()
        # table.attach(label, 0, 2, 0, 1)
        table.attach(self.label2, 0, 1, 1, 2)
        table.attach(self.name, 1, 2, 1, 2)
        table.attach(pcname, 0, 1, 2, 3)
        table.attach(self.host, 1, 2, 2, 3)
        table.attach(Username, 0, 1, 3, 4)
        table.attach(self.user, 1, 2, 3, 4)
        table.attach(self.labelpass, 0, 1, 4, 5)
        table.attach(self.password, 1, 2, 4, 5)
        self.label3 = Gtk.Label()
        table.attach(self.label3, 2, 3, 4, 5)
        table.attach(self.label4, 0, 1, 5, 6)
        table.attach(self.repassword, 1, 2, 5, 6)
        # set image for password matching
        self.img = Gtk.Image()
        table.attach(self.img, 2, 3, 5, 6)
        table.attach(self.label5, 0, 1, 6, 7)
        table.attach(shell, 1, 2, 6, 7)
        box2.pack_start(table, False, False, 0)
        self.box3 = Gtk.VBox(False, 10)
        self.box3.set_border_width(10)
        self.box1.pack_start(self.box3, True, True, 0)
        self.box3.show()
        # self.label3 = Gtk.Label()
        # self.box3.pack_start(self.label3, False, False, 0)

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
                button3.set_sensitive(True)
            else:
                self.label3.set_text("Super Strong")
                button3.set_sensitive(False)

    def passwdVerification(self, widget, button3):
        if self.password.get_text() == self.repassword.get_text():
            self.img.set_from_stock(Gtk.STOCK_YES, 10)
            button3.set_sensitive(True)

        else:
            self.img.set_from_stock(Gtk.STOCK_NO, 10)
            button3.set_sensitive(False)
