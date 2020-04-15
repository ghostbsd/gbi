#!/usr/bin/env python
"""
Copyright (c) 2010-2013, GhostBSD. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistribution's of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistribution's in binary form must reproduce the above
   copyright notice,this list of conditions and the following
   disclaimer in the documentation and/or other materials provided
   with the distribution.

3. Neither then name of GhostBSD Project nor the names of its
   contributors maybe used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES(INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import sys
import os
import shutil
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
installer = "/usr/local/lib/gbi/"
sys.path.append(installer)
from language import Language
from installType import Types
from keyboard import Keyboard
from timezone import TimeZone
from use_ufs import use_ufs
from partition import Partitions
from use_zfs import ZFS
from boot_manager import bootManager
from root import RootUser
from addUser import AddUser
from partition_handler import partition_repos
from install import installProgress, installSlide
logo = "/usr/local/lib/gbi/logo.png"
tmp = "/tmp/.gbi/"
if not os.path.exists(tmp):
    os.makedirs(tmp)
disk = '%sdisk' % tmp
dslice = '%sslice' % tmp
disk_schem = '%sscheme' % tmp
zfs_config = '%szfs_config' % tmp
ufs_config = '%sufs_config' % tmp
partitiondb = "%spartitiondb/" % tmp


class MainWindow():
    """Main window class."""

    def delete(self, widget, event=None):
        """Close the main window."""
        if os.path.exists('/tmp/.gbi'):
            shutil.rmtree('/tmp/.gbi')
        Gtk.main_quit()
        return False

    def next_page(self, widget, notebook):
        """Go to the next window."""
        page = self.notebook.get_current_page()
        if page == 0:
            self.lang.save_selection()
            kbbox = Gtk.VBox(False, 0)
            kbbox.show()
            self.kb = Keyboard(self.button3)
            get_kb = self.kb.get_model()
            kbbox.pack_start(get_kb, True, True, 0)
            label = Gtk.Label("Keyboard")
            self.notebook.insert_page(kbbox, label, 1)
            self.window.show_all()
            self.notebook.next_page()
            self.button1.set_sensitive(True)
            self.button3.set_sensitive(True)
        elif page == 1:
            self.kb.save_selection()
            tbbox = Gtk.VBox(False, 0)
            tbbox.show()
            self.tz = TimeZone(self.button3)
            get_tz = self.tz.get_model()
            tbbox.pack_start(get_tz, True, True, 0)
            label = Gtk.Label("TimeZone")
            self.notebook.insert_page(tbbox, label, 2)
            self.window.show_all()
            self.notebook.next_page()
            self.button3.set_sensitive(True)
        elif page == 2:
            self.tz.save_selection()
            typebox = Gtk.VBox(False, 0)
            typebox.show()
            self.types = Types()
            get_types = self.types.get_model()
            typebox.pack_start(get_types, True, True, 0)
            label = Gtk.Label("Types")
            self.notebook.insert_page(typebox, label, 3)
            self.window.show_all()
            self.notebook.next_page()
        elif page == 3:
            if self.types.get_type() == "ufs":
                partition_repos()
                udbox = Gtk.VBox(False, 0)
                udbox.show()
                self.partition = use_ufs(self.button3)
                get_ud = self.partition.get_model()
                udbox.pack_start(get_ud, True, True, 0)
                label = Gtk.Label("UFS Disk Configuration")
                self.notebook.insert_page(udbox, label, 4)
                self.window.show_all()
                self.notebook.next_page()
                self.button3.set_sensitive(False)
            elif self.types.get_type() == "custom":
                partition_repos()
                Pbox = Gtk.VBox(False, 0)
                Pbox.show()
                self.partition = Partitions(self.button3)
                get_part = self.partition.get_model()
                Pbox.pack_start(get_part, True, True, 0)
                label = Gtk.Label("UFS Custom Configuration")
                self.notebook.insert_page(Pbox, label, 4)
                self.window.show_all()
                self.notebook.next_page()
                self.button3.set_sensitive(False)
            elif self.types.get_type() == "zfs":
                Zbox = Gtk.VBox(False, 0)
                Zbox.show()
                self.partition = ZFS(self.button3)
                get_ZFS = self.partition.get_model()
                Zbox.pack_start(get_ZFS, True, True, 0)
                label = Gtk.Label("ZFS Configuration")
                self.notebook.insert_page(Zbox, label, 4)
                self.window.show_all()
                self.notebook.next_page()
                self.button3.set_sensitive(False)
        elif page == 4:
            self.partition.save_selection()
            Mbox = Gtk.VBox(False, 0)
            Mbox.show()
            self.bootmanager = bootManager()
            get_root = self.bootmanager.get_model()
            Mbox.pack_start(get_root, True, True, 0)
            label = Gtk.Label("Boot Option")
            self.notebook.insert_page(Mbox, label, 5)
            self.window.show_all()
            self.notebook.next_page()
            self.button3.set_sensitive(True)
        elif page == 5:
            Rbox = Gtk.VBox(False, 0)
            Rbox.show()
            self.rootuser = RootUser(self.button3)
            get_root = self.rootuser.get_model()
            Rbox.pack_start(get_root, True, True, 0)
            label = Gtk.Label("Root Password")
            self.notebook.insert_page(Rbox, label, 6)
            self.window.show_all()
            self.notebook.next_page()
            self.button3.set_sensitive(False)
        elif page == 6:
            self.rootuser.save_selection()
            Abox = Gtk.VBox(False, 0)
            Abox.show()
            self.adduser = AddUser(self.button3)
            get_adduser = self.adduser.get_model()
            Abox.pack_start(get_adduser, True, True, 0)
            label = Gtk.Label("Adding User")
            self.notebook.insert_page(Abox, label, 7)
            self.button3.set_label("Install")
            self.window.show_all()
            self.notebook.next_page()
            self.button3.set_sensitive(False)
        elif page == 7:
            self.adduser.save_selection()
            Ibox = Gtk.VBox(False, 0)
            Ibox.show()
            install = installSlide()
            get_install = install.get_model()
            Ibox.pack_start(get_install, True, True, 0)
            label = Gtk.Label("Installation")
            self.notebook.insert_page(Ibox, label, 8)
            self.notebook.next_page()
            instpro = installProgress()
            progressBar = instpro.getProgressBar()
            box1 = Gtk.VBox(False, 0)
            box1.show()
            label = Gtk.Label("Progress Bar")
            box1.pack_end(progressBar, False, False, 0)
            self.nbButton.insert_page(box1, label, 1)
            self.nbButton.next_page()
            self.window.show_all()

    def back_page(self, widget):
        """Go back to the previous window."""
        current_page = self.notebook.get_current_page()
        if current_page == 1:
            self.button1.set_sensitive(False)
        elif current_page == 7:
            self.button3.set_label("Next")
        self.notebook.prev_page()
        new_page = self.notebook.get_current_page()
        if current_page == 4 and new_page == 3:
            if os.path.exists(partitiondb):
                shutil.rmtree(partitiondb)
            if os.path.exists(tmp + 'create'):
                os.remove(tmp + 'create')
            if os.path.exists(tmp + 'delete'):
                os.remove(tmp + 'delete')
            if os.path.exists(tmp + 'destroy'):
                os.remove(tmp + 'destroy')
            if os.path.exists(tmp + 'partlabel'):
                os.remove(tmp + 'partlabel')
            if os.path.exists(zfs_config):
                os.remove(zfs_config)
            if os.path.exists(ufs_config):
                os.remove(ufs_config)
            if os.path.exists(disk):
                os.remove(disk)
            if os.path.exists(dslice):
                os.remove(dslice)
            if os.path.exists(disk_schem):
                os.remove(disk_schem)
        self.button3.set_sensitive(True)

    def __init__(self):
        """Were the Main window start."""
        self.window = Gtk.Window()
        self.window.connect("delete_event", self.delete)
        self.window.set_border_width(0)
        self.window.set_default_size(800, 500)
        self.window.set_size_request(800, 500)
        self.window.set_title("GhostBSD Installer")
        self.window.set_border_width(0)
        self.window.set_icon_from_file(logo)
        mainHBox = Gtk.HBox(False, 0)
        mainHBox.show()
        mainVbox = Gtk.VBox(False, 0)
        mainVbox.show()
        self.window.add(mainHBox)
        mainHBox.pack_start(mainVbox, True, True, 0)
        # Create a new self.notebook
        self.notebook = Gtk.Notebook()
        mainVbox.pack_start(self.notebook, True, True, 0)
        self.notebook.show()
        self.notebook.set_show_tabs(False)
        self.notebook.set_show_border(False)
        vbox = Gtk.VBox(False, 0)
        vbox.show()
        self.lang = Language()
        get_lang = self.lang.get_model()
        # self.lang = Installs()
        # get_lang = self.lang.get_model()
        vbox.pack_start(get_lang, True, True, 0)
        label = Gtk.Label("Language")
        self.notebook.insert_page(vbox, label, 0)

        # Set what page to start at Language
        self.notebook.set_current_page(0)

        # Create buttons
        self.table = Gtk.Table(1, 6, True)

        self.button1 = Gtk.Button(label='Back')
        self.button1.connect("clicked", self.back_page)
        self.table.attach(self.button1, 3, 4, 0, 1)
        self.button1.show()
        self.button1.set_sensitive(False)

        self.button2 = Gtk.Button(label='Cancel')
        self.button2.connect("clicked", self.delete)
        self.table.attach(self.button2, 4, 5, 0, 1)
        self.button2.show()

        self.button3 = Gtk.Button(label='Next')
        self.button3.connect("clicked", self.next_page, self.notebook)
        self.table.attach(self.button3, 5, 6, 0, 1)
        self.button3.show()

        self.table.set_col_spacings(5)
        self.table.show()
        # Create a new notebook
        self.nbButton = Gtk.Notebook()
        mainVbox.pack_end(self.nbButton, False, False, 5)
        self.nbButton.show()
        self.nbButton.set_show_tabs(False)
        self.nbButton.set_show_border(False)
        label = Gtk.Label("Button")
        self.nbButton.insert_page(self.table, label, 0)
        self.window.show_all()
