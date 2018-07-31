#!/usr/bin/env python
#
#####################################################################
# Copyright (c) 2009-2012, GhostBSD. All rights reserved.
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
#####################################################################
# language.py show the language for the installer.


from gi.repository import Gtk
import os
import os.path
from sys_handler import language_dictionary
# Folder use for the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)
logo = "/usr/local/lib/gbi/logo.png"
langfile = '%slanguage' % tmp
lang_dictionary = language_dictionary()
# Text to be replace be multiple language file.
title = "Welcome To GhostBSD!"
welltext = """Select the language you want to use with GhostBSD."""


class Language:

    # On selection it overwrite the delfaut language file.
    def Language_Selection(self, tree_selection):
        model, treeiter = tree_selection.get_selected()
        if treeiter is not None:
            value = model[treeiter][0]
            self.language = lang_dictionary[value]
        return

    def Language_Columns(self, treeView):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('Language')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)
        return

    def save_selection(self):
        lang_file = open(langfile, 'w')
        lang_file.writelines(self.language)
        lang_file.close()
        return

    # Initial definition.
    def __init__(self):
        # Add a Default vertical box
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        # Add a second vertical box
        grid = Gtk.Grid()
        self.vbox1.pack_start(grid, True, True, 0)
        grid.set_row_spacing(10)
        grid.set_column_spacing(3)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_margin_left(10)
        grid.set_margin_right(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        # Adding a Scrolling Window
        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # Adding a treestore and store language in it.
        store = Gtk.TreeStore(str)
        for line in lang_dictionary:
            store.append(None, [line])
        treeView = Gtk.TreeView(store)
        treeView.set_model(store)
        treeView.set_rules_hint(True)
        self.Language_Columns(treeView)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        tree_selection.connect("changed", self.Language_Selection)
        sw.add(treeView)
        sw.show()
        grid.attach(sw, 1, 2, 1, 9)
        # add text in a label.
        vhbox = Gtk.VBox(False, 0)
        vhbox.set_border_width(10)
        vhbox.show()
        self.wellcome = Gtk.Label('<span size="xx-large"><b>' + title + '</b></span>')
        self.wellcome.set_use_markup(True)
        self.wellcometext = Gtk.Label(welltext)
        self.wellcometext.set_use_markup(True)
        table = Gtk.Table()
        # table.attach(self.wellcome, 0, 1, 1, 2)
        # wall = Gtk.Label()
        # table.attach(wall, 0, 1, 2, 3)
        table.attach(self.wellcometext, 0, 1, 3, 4)
        vhbox.pack_start(table, False, False, 5)
        image = Gtk.Image()
        image.set_from_file(logo)
        image.show()
        grid.attach(self.wellcome, 1, 1, 3, 1)
        vhbox.pack_start(image, True, True, 5)
        grid.attach(vhbox, 2, 2, 2, 9)
        grid.show()
        return

    def get_model(self):
        return self.vbox1
