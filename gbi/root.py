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
# root.py v 1.4 Friday, January 17 2014 Eric Turgeon
#
# root.py set root password.

import gtk
import os
import re
from subprocess import Popen
from defutil import close_application, back_window
import pickle

# Directory use from the installer.
tmp = "/home/ghostbsd/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)
to_user = 'python %suser.py' % installer
boot_file = '%sboot' % tmp


class rootUsers:
    def next_window(self, widget):
        f = open('%sroot' % tmp, 'wb')
        if self.password.get_text() == self.repassword.get_text():
            rp = self.password.get_text()
            ul = [rp]
            pickle.dump(ul, f)
            f.close()
            Popen(to_user, shell=True)
            gtk.main_quit()
        else:
            self.label3.set_text("Password and password confirmation for root don't match. Try again!")

    def on_check(self, widget):
        if widget.get_active():
            self.boot = "bsd"
        else:
            self.boot = 'none'
        boot = open(boot_file, 'w')
        boot.writelines(self.boot)
        boot.close()

    def create_bbox(self, horizontal, spacing, layout):
        bbox = gtk.HButtonBox()
        bbox.set_border_width(5)
        # Set the appearance of the Button Box
        bbox.set_layout(layout)
        bbox.set_spacing(spacing)
        button = gtk.Button(stock=gtk.STOCK_GO_BACK)
        button.connect("clicked", back_window)
        bbox.add(button)
        button = gtk.Button(stock=gtk.STOCK_CANCEL)
        bbox.add(button)
        button.connect("clicked", close_application)
        button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        bbox.add(button)
        button.connect("clicked", self.next_window)
        return bbox

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("destroy", close_application)
        window.set_size_request(700, 500)
        window.set_title("GhostBSD Installer")
        window.set_border_width(10)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_icon_from_file("/usr/local/lib/gbi/logo.png")
        box1 = gtk.VBox(False, 0)
        window.add(box1)
        box1.show()
        box2 = gtk.VBox(False, 0)
        box2.set_border_width(10)
        box1.pack_start(box2, False, False, 10)
        box2.show()
        # title.
        ttext = "Administrator(root) Password"
        Title = gtk.Label("<b><span size='xx-large'>%s</span></b>" % ttext)
        Title.set_use_markup(True)
        box2.pack_start(Title, False, False, 10)
        # password for root.
        label = gtk.Label('<b>Administrator (root) Password</b>')
        label.set_use_markup(True)
        label.set_alignment(.4, .2)
        table = gtk.Table(1, 3, True)
        table.set_row_spacings(10)
        label1 = gtk.Label("Password")
        self.password = gtk.Entry()
        self.password.set_visibility(False)
        self.password.connect("changed", self.passwdstrength)
        label2 = gtk.Label("Verify Password")
        self.repassword = gtk.Entry()
        self.repassword.set_visibility(False)
        self.repassword.connect("changed", self.passwdVerification)
        self.label3 = gtk.Label()
        self.img = gtk.Image() 
        table.attach(label1, 0, 1, 1, 2)
        table.attach(self.password, 1, 2, 1, 2)
        table.attach(self.label3, 2, 3, 1, 2)
        table.attach(label2, 0, 1, 2, 3)
        table.attach(self.repassword, 1, 2, 2, 3)
        table.attach(self.img, 2, 3, 2, 3)
        box2.pack_start(table, False, False, 10)
        # Boot option.
        box3 = gtk.VBox(False, 10)                                         
        box3.set_border_width(10)                                          
        box1.pack_start(box3, True, True, 0)                               
        box3.show()                                                       
        label = gtk.Label()                                               
        label = gtk.Label('<b><span size="xx-large">Boot Option</span></b>')
        label.set_use_markup(True)
        box3.pack_start(label, False, False, 20)
        check = gtk.CheckButton("Install FreeBSD Boot Manager(MBR only)")
        check.connect("toggled", self.on_check)
        self.boot = 'none'
        boot = open(boot_file, 'w')
        boot.writelines(self.boot)
        boot.close()
        table = gtk.Table(1, 6, True)
        table.set_row_spacings(10)
        table.attach(check, 2, 5, 0, 1)
        box3.pack_start(table, False, False, 10)
        self.box3 = gtk.VBox(False, 10)
        self.box3.set_border_width(10)
        box1.pack_start(self.box3, True, True, 0)
        #self.box3.show()
        #self.label = gtk.Label()
        #self.box3.pack_start(self.label3, False, False, 0)
        box2 = gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        box2.pack_start(self.create_bbox(True,
            10, gtk.BUTTONBOX_END),
            True, True, 5)
        window.show_all()
    

    def passwdstrength(self, widget):
        passwd = self.password.get_text()
        print passwd
        if len(passwd) <= 5:
            self.label3.set_text("Super Weak")
            print "Super Weak"
        elif len(passwd) <= 10
            if re.match("[a-z]", passwd):
                print "Very Weak"
                if re.match("[A-Z]", passwd):

                    if re.match("[0-9]", passwd):
                        if re.match("[~!@#$%^&*_+-]", passwd):
            elif len(passwd) <= 10:
                self.label3.set_text("Weak")
                print "Weak"
            elif re.match("[a-z]", passwd) and re.match("[A-Z]", passwd) and re.match("[0-9]", passwd) and len(passwd) <= 6:
                self.label3.set_text("Fairly Weak")
                print "Fairly Weak"
            elif re.match("[a-z]", passwd) and re.match("[A-Z]", passwd) and len(passwd) <= 6:
                self.label3.set_text("Very Weak")
                print "Very Weak"
        elif re.match("[a-z]", passwd) and len(passwd) <= 6:          
            self.label3.set_text("Super Weak")
            print "Super Weak 6" 
        elif re.match("[a-z]", passwd) and re.match("[A-Z]", passwd) and re.match("[0-9]", passwd) and len(passwd) <= 10:
            self.label3.set_text("Weak")


    def passwdVerification(self, widget):
        if self.password.get_text() == self.repassword.get_text():
            self.img.set_from_stock(gtk.STOCK_YES, 10)
        else:
            self.img.set_from_stock(gtk.STOCK_NO, 10)

rootUsers()
gtk.main()
