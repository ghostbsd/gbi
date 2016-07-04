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
# $Id: gbi_keyboard.py v 0.3 Wednesday, May 30 2012 21:49 Eric Turgeon $

from gi.repository import Gtk, GObject
import os
from subprocess import Popen, PIPE, call


# Folder use for the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
pc_sysinstall = "/usr/local/bin/pc-sysinstall"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

logo = "/usr/local/lib/gbi/logo.png"

xk_variant = "%s xkeyboard-variants" % pc_sysinstall
xk_layout = "%s xkeyboard-layouts" % pc_sysinstall

# xkeyboard_variant = Popen(xk_variant , shell=True, stdout=PIPE, close_fds=True)
# xkeyboard_layout = Popen(xk_layout , shell=True, stdout=PIPE, close_fds=True)

xkeyboard_variant = "/usr/local/lib/gbi/keyboard/variant"
xkeyboard_layout = "/usr/local/lib/gbi/keyboard/layout"

layout = '%slayout' % tmp
variant = '%svariant' % tmp
KBFile= '%skeyboard' % tmp

# This class is for placeholder for entry.

class PlaceholderEntry(Gtk.Entry):

    placeholder = 'Type here to test your keyboard'
    _default = True

    def __init__(self, *args, **kwds):
        Gtk.Entry.__init__(self, *args, **kwds)
        self.set_text(self.placeholder)
        # self.modify_text(Gtk.STATE_NORMAL, Gtk.gdk.color_parse("#4d4d4d"))
        self._default = True
        self.connect('focus-in-event', self._focus_in_event)
        self.connect('focus-out-event', self._focus_out_event)

    def _focus_in_event(self, widget, event):
        if self._default:
            self.set_text('')
            # self.modify_text(Gtk.STATE_NORMAL, Gtk.gdk.color_parse('black'))

    def _focus_out_event(self, widget, event):
        if Gtk.Entry.get_text(self) == '':
            self.set_text(self.placeholder)
            # self.modify_text(Gtk.STATE_NORMAL, Gtk.gdk.color_parse("#4d4d4d"))
            self._default = True
        else:
            self._default = False

    def get_text(self):
        if self._default:
            return ''
        return Gtk.Entry.get_text(self)


class Keyboard:
    def layout_columns(self, treeView):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('<b>Keyboard Layout</b>')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def variant_columns(self, treeView):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('<b>Keyboard Variant</b>')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def Selection_Layout(self, tree_selection, button3):
        (model, pathlist) = tree_selection.get_selected_rows()
        self.variant_store.clear()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
        self.layout_txt = value
        if os.path.exists("%s/%s" % (xkeyboard_variant, value.partition("-")[2].strip())):
            read = open("%s/%s" % (xkeyboard_variant, value.partition("-")[2].strip()), 'r')
            for line in read.readlines():
                self.variant_store.append(None, [line.rstrip()])
        call("setxkbmap %s" % self.layout_txt.partition("-")[2], shell=True)
        button3.set_sensitive(True)

    def Selection_Variant(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
            #print value
        self.variant_txt = value
        call("setxkbmap %s %s" % (self.layout_txt.partition("-")[2],
        self.variant_txt.partition(":")[2]), shell=True)

    def get_model(self):
        return self.box1

    def save_selection(self):
        File = open(KBFile, 'w')
        File.writelines("%s\n" % self.layout_txt)
        if self.variant_txt != None:
            File.writelines("%s\n" % self.variant_txt)
        File.close()
        return

    def __init__(self, button3):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()
        table = Gtk.Table(1, 2, True)
        label = Gtk.Label('<span size="xx-large"><b>Keyboard Setup</b></span>')
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
        read = open(xkeyboard_layout, 'r')
        for line in read.readlines():
            store.append(None, [line.rstrip()])
        self.treeView = Gtk.TreeView(store)
        self.treeView.set_model(store)
        self.treeView.set_rules_hint(True)
        self.layout_columns(self.treeView)
        self.tree_selection = self.treeView.get_selection()
        self.tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.tree_selection.connect("changed", self.Selection_Layout, button3)
        sw.add(self.treeView)
        sw.show()
        hbox.pack_start(sw, True, True, 5)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.variant_store = Gtk.TreeStore(str)
        treeView = Gtk.TreeView(self.variant_store)
        treeView.set_model(self.variant_store)
        treeView.set_rules_hint(True)
        self.variant_columns(treeView)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        tree_selection.connect("changed", self.Selection_Variant)
        sw.add(treeView)
        sw.show()
        self.variant_txt = None
        hbox.pack_start(sw, True, True, 5)

        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        self.box1.pack_start(box2, False, False, 0)
        box2.show()
        box2.pack_start(PlaceholderEntry(), True, True, 10)

