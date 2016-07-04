#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
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
#
# $Id: time.py v 0.3 Wednesday, May 30 2012 21:49 Eric Turgeon $
#

from gi.repository import Gtk
import os.path
import os

# Folder use for the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

logo = "/usr/local/lib/gbi/logo.png"
back = 'python %sgbi_keyboard.py' % installer
logo = "/usr/local/lib/gbi/logo.png"
continent = '%s/timezone/continent' % installer
city = '%s/timezone/city/' % installer
time = '%stimezone' % tmp


class TimeZone:

    def continent_columns(self, treeView):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('<b>Continent</b>')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def city_columns(self, treeView):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('<b>City</b>')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def Continent_Selection(self, widget):
        (model, pathlist) = widget.get_selected_rows()
        self.variant_store.clear()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
        self.continent = value
        read = open('%s%s' % (city, self.continent), 'r')
        for line in read.readlines():
                self.variant_store.append(None, [line.rstrip()])

    def City_Selection(self, tree_selection, button3):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
            #print value
        self.city = value
        button3.set_sensitive(True)

    def save_selection(self):
        timezone = '%s/%s' % (self.continent, self.city)
        time_file = open(time, 'w')
        time_file.writelines(timezone)
        time_file.close()
        return

    def __init__(self, button3):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()
        table = Gtk.Table(1, 2, True)
        label = Gtk.Label('<b><span size="xx-large">Time Zone Selection</span></b>')
        label.set_use_markup(True)
        table.attach(label, 0, 2, 0, 1)
        box2.pack_start(table, False, False, 0)
        hbox = Gtk.HBox(False, 10)
        hbox.set_border_width(5)
        box2.pack_start(hbox, True, True, 5)
        hbox.show()

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        store = Gtk.TreeStore(str)
        read = open(continent, 'r')
        line0 = read.readlines()[0].strip()
        self.continent = line0
        read = open(continent, 'r')
        for line in read.readlines():
            store.append(None, [line.rstrip()])
        self.continenttreeView = Gtk.TreeView(store)
        self.continenttreeView.set_model(store)
        self.continenttreeView.set_rules_hint(True)
        self.continent_columns(self.continenttreeView)
        self.continenttree_selection = self.continenttreeView.get_selection()
        self.continenttree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.continenttree_selection.connect("changed", self.Continent_Selection)
        sw.add(self.continenttreeView)
        sw.show()
        hbox.pack_start(sw, True, True, 5)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.variant_store = Gtk.TreeStore(str)
        treeView = Gtk.TreeView(self.variant_store)
        treeView.set_model(self.variant_store)
        treeView.set_rules_hint(True)
        self.city_columns(treeView)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        tree_selection.connect("changed", self.City_Selection, button3)
        sw.add(treeView)
        sw.show()
        hbox.pack_start(sw, True, True, 5)
        return

    def get_model(self):
        return self.box1
