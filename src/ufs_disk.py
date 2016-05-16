#!/usr/local/bin/python
#
#
# Copyright (c) 2009-2015, GhostBSD. All rights reserved.
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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
import os
import os.path
import re
from subprocess import Popen, PIPE, STDOUT
from partition_handler import disk_query

# Folder use pr the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

logo = "/usr/local/lib/gbi/logo.png"
memory = 'sysctl hw.physmem'
auto = '%sauto' % tmp
disk_info = '%sdisk-info.sh' % query
disk_file = '%sdisk' % tmp
dslice = '%sslice' % tmp
Part_label = '%sufs_fulldisk_config' % tmp
part_schem = '%sscheme' % tmp
disk_list = '%sdisk-list.sh' % query
ufs_dsk_list = []
to_root = 'python %sroot.py' % installer


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


class Entire():
    def Selection_Variant(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
            value2 = model.get_value(tree_iter, 1)
            value3 = model.get_value(tree_iter, 2)
        self.disk = value
        self.size = value2
        if value3 is None:
            self.schm = 'GPT'
        else:
            self.schm = value3
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=%s' % self.schm)
        sfile.close()
        file_disk = open(disk_file, 'w')
        file_disk.writelines('%s\n' % self.disk)
        file_disk.close()
        NUMBER = int(self.size)
        slice_file = open(dslice, 'w')
        slice_file.writelines('all\n')
        #slice_file.writelines('%s\n' % NUMBER)
        slice_file.close()
        ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
        close_fds=True)
        mem = ram.stdout.read()
        SWAP = int(mem.partition(':')[2].strip()) / (1024 * 1024)
        NUM1 = NUMBER - SWAP
        pfile = open(Part_label, 'w')
        pfile.writelines('UFS+SUJ %s /\n' % NUM1)
        pfile.writelines('SWAP 0 none\n')
        pfile.close()

    def __init__(self):
        window = Gtk.Window()

        window.set_size_request(700, 500)
        window.set_resizable(False)
        window.set_title("GhostBSD Installer")
        window.set_border_width(0)
        window.set_icon_from_file("/usr/local/lib/gbi/logo.png")
        box1 = Gtk.VBox(False, 0)
        window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # Title
        Title = Gtk.Label("<b><span size='xx-large'>Install GhostBSD entirely on disk</span></b> ")
        Title.set_use_markup(True)
        box2.pack_start(Title, False, False, 0)
        # chose Disk
        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        store = Gtk.TreeStore(str, str, str, 'gboolean')
        for disk in disk_query():
            store.append(None, [disk[0], disk[1], disk[3], False])
        treeView = Gtk.TreeView(store)
        treeView.set_model(store)
        treeView.set_rules_hint(True)
        self.checkcell = Gtk.CellRendererToggle()
        self.checkcell.set_property('activatable', True)
        self.checkcell.connect('toggled', self.col1_toggled_cb, store)
        column1 = Gtk.TreeViewColumn("Check", self.checkcell)
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('Disk')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        cell2 = Gtk.CellRendererText()
        column2 = Gtk.TreeViewColumn(None, cell2, text=0)
        column_header2 = Gtk.Label('Size(MB)')
        column_header2.set_use_markup(True)
        column_header2.show()
        column2.set_widget(column_header2)
        cell3 = Gtk.CellRendererText()
        column3 = Gtk.TreeViewColumn(None, cell3, text=0)
        column_header3 = Gtk.Label('Scheme')
        column_header3.set_use_markup(True)
        column_header3.show()
        column3.set_widget(column_header3)
        column1.add_attribute(self.checkcell, "active", 3)
        column.set_attributes(cell, text=0)
        column2.set_attributes(cell2, text=1)
        column3.set_attributes(cell3, text=2)
        treeView.append_column(column1)
        treeView.append_column(column)
        treeView.append_column(column2)
        treeView.append_column(column3)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        tree_selection.connect("changed", self.Selection_Variant)
        sw.add(treeView)
        sw.show()
        self.Gmirror = False
        gMirror_check = Gtk.CheckButton("Mirror Swap")
        gMirror_check.connect("toggled", self.on_check_Gmirror)
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.show()
        grid.attach(sw, 1, 4, 8, 3)
        box2.pack_start(grid, True, True, 10)
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=GPT')
        sfile.close()
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, False, 0)
        box2.show()
        # Add button
        #box2.pack_start(use_disk_bbox(True,
        #                10, Gtk.BUTTONBOX_END),
        #                True, True, 5)
        window.show_all()

    def col1_toggled_cb(self, cell, path, model):
        model[path][3] = not model[path][3]
        if model[path][3] is False:
            zfs_dsk_list.remove(model[path][0] + "-" + model[path][1])
            if self.mirror == "none":
                if len(zfs_dsk_list) != 1:
                    self.button3.set_sensitive(False)
                else:
                    self.button3.set_sensitive(True)
            elif self.mirror == "mirror":
                if len(zfs_dsk_list) > 1:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "raidz1":
                if len(zfs_dsk_list) == 4 or len(zfs_dsk_list) == 6 or len(zfs_dsk_list) == 10:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "raidz2":
                if len(zfs_dsk_list) == 3 or len(zfs_dsk_list) == 5:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "raidz3":
                if len(zfs_dsk_list) == 5 or len(zfs_dsk_list) == 7 or len(zfs_dsk_list) == 11:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "strip":
                if len(zfs_dsk_list) > 2:
                    self.button3.set_sensitive(True)
                else:
                    self.butt

Entire()
Gtk.main()
