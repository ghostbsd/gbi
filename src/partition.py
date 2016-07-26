#!/usr/local/bin/python
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
#
# partition.py v 1.3 Friday, January 17 2014 Eric Turgeon
#
# auto_partition.py create and delete partition slice for GhostBSD installer
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
import os
import shutil
from partition_handler import partition_repos, disk_query, Delete_partition
from partition_handler import partition_query, label_query, bios_or_uefi
from partition_handler import autoDiskPartition, autoFreeSpace
from partition_handler import createLabel, scheme_query, how_partition
from partition_handler import diskSchemeChanger, createSlice, createPartition

# Folder use pr the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

add_part = 'gpart add'
disk_part = '%sdisk-part.sh' % query
disk_label = '%sdisk-label.sh' % query
detect_sheme = '%sdetect-sheme.sh' % query

part = '%sdisk-part.sh' % query
memory = 'sysctl hw.physmem'
disk_list = '%sdisk-list.sh' % query
disk_info = '%sdisk-info.sh' % query
disk_label = '%sdisk-label.sh' % query
disk_schem = '%sscheme' % tmp
disk_file = '%sdisk' % tmp
psize = '%spart_size' % tmp
logo = "/usr/local/lib/gbi/logo.png"
Part_label = '%spartlabel' % tmp
part_schem = '%sscheme' % tmp
partitiondb = "%spartitiondb/" % tmp
boot_file = "%sboot" % tmp
ufs_Partiton_list = []

class Partitions():

    def on_fs(self, widget):
        self.fs = widget.get_active_text()

    def on_label(self, widget):
        self.label = widget.get_active_text()

    def save_selection(self):
        pass

    def on_add_label(self, widget, entry, inumb, path, data):
        if self.fs == '' or self.label == '':
            pass
        else:
            fs = self.fs
            lb = self.label
            cnumb = entry.get_value_as_int()
            lnumb = inumb - cnumb
            createLabel(path, lnumb, cnumb, lb, fs, data)
        self.window.hide()
        self.update()
        partlabel = '%spartlabel' % tmp

    def on_add_partition(self, widget, entry, inumb, path, data):
        if self.fs == '' or self.label == '':
            pass
        else:
            fs = self.fs
            lb = self.label
            cnumb = entry.get_value_as_int()
            lnumb = inumb - cnumb
            createPartition(path, lnumb, inumb, cnumb, lb, fs, data)
        self.window.hide()
        self.update()

    def cancel(self, widget):
        self.window.hide()

    def labelEditor(self, path, pslice, size, data1, data2):
        numb = int(size)
        self.window = Gtk.Window()
        self.window.set_title("Add Partition")
        self.window.set_border_width(0)
        self.window.set_size_request(480, 200)
        self.window.set_icon_from_file(logo)
        box1 = Gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # create label
        # label0 = Gtk.Label("Create Partition Label")
        table = Gtk.Table(1, 2, True)
        label1 = Gtk.Label("Type:")
        label2 = Gtk.Label("Size(MB):")
        label3 = Gtk.Label("Mount point:")
        self.fstype = Gtk.ComboBoxText()
        self.fstype.append_text('UFS')
        self.fstype.append_text('UFS+S')
        self.fstype.append_text('UFS+J')
        self.fstype.append_text('UFS+SUJ')
        self.fstype.append_text('SWAP')
        if data1 == 1:
            read = open(boot_file, 'r')
            line = read.readlines()
            boot = line[0].strip()
            if bios_or_uefi() == "UEFI":
                self.fstype.append_text("UEFI")
                self.fs = "UEFI"
            elif boot == "grub":
                self.fstype.append_text("BIOS")
                self.fs = "BIOS"
            else:
                self.fstype.append_text("BOOT")
                self.fs = "BOOT"
        if data1 == 1 and not os.path.exists(Part_label):
            self.fstype.set_active(5)
        elif data1 == 1 and len(self.partfile) == 0:
            self.fstype.set_active(5)
        elif self.lablebehind == "/":
            self.fstype.set_active(4)
            self.fs = "SWAP"
        else:
            self.fstype.set_active(3)
            self.fs = "UFS+SUJ"
        self.fstype.connect("changed", self.on_fs)
        adj = Gtk.Adjustment(numb, 0, numb, 1, 100, 0)
        self.entry = Gtk.SpinButton(adjustment=adj)
        if data2 == 0:
            self.entry.set_editable(False)
        else:
            self.entry.set_editable(True)
        self.mountpoint = Gtk.ComboBoxText()
        # self.mountpoint.append_text('select labels')
        self.label = "none"
        self.mountpoint.append_text('none')
        # The space for root '/ ' is to recognise / from the file.
        self.mountpoint.append_text('/')
        if os.path.exists(Part_label):
            if data1 == 1 and len(self.partfile) == 1:
                self.mountpoint.append_text('/boot')
            elif data1 == 0 and len(self.partfile) == 0:
                self.mountpoint.append_text('/boot')
        elif data1 == 0 and not os.path.exists(Part_label):
            self.mountpoint.append_text('/boot')
        self.mountpoint.append_text('/etc')
        self.mountpoint.append_text('/root')
        self.mountpoint.append_text('/tmp')
        self.mountpoint.append_text('/usr')
        self.mountpoint.append_text('/usr/home')
        self.mountpoint.append_text('/var')
        self.mountpoint.set_active(0)
        self.mountpoint.connect("changed", self.on_label)
        # table.attach(label0, 0, 2, 0, 1)
        table.attach(label1, 0, 1, 1, 2)
        table.attach(self.fstype, 1, 2, 1, 2)
        table.attach(label2, 0, 1, 2, 3)
        table.attach(self.entry, 1, 2, 2, 3)
        table.attach(label3, 0, 1, 3, 4)
        table.attach(self.mountpoint, 1, 2, 3, 4)
        box2.pack_start(table, False, False, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        # Add button
        bbox = Gtk.HButtonBox()
        bbox.set_border_width(5)
        bbox.set_spacing(10)
        button = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        button.connect("clicked", self.cancel)
        bbox.add(button)
        button = Gtk.Button(stock=Gtk.STOCK_ADD)
        if data2 == 1:
            if data1 == 0:
                button.connect("clicked", self.on_add_label, self.entry, numb, path, True)
            elif data1 == 1:
                button.connect("clicked", self.on_add_partition, self.entry, numb, path, True)
        else:
            if data1 == 0:
                button.connect("clicked", self.on_add_label, self.entry, numb, path, False)
            elif data1 == 1:
                button.connect("clicked", self.on_add_partition, self.entry, numb, path, False)
        bbox.add(button)
        box2.pack_end(bbox, True, True, 5)
        self.window.show_all()

    def sheme_selection(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        data = model[index][0]
        value = data.partition(':')[0]
        self.scheme = value

    def add_gpt_mbr(self, widget):
        diskSchemeChanger(self.scheme, self.path, self.slice, self.size)
        self.update()
        self.window.hide()

    def autoSchemePartition(self, widget):
        diskSchemeChanger(self.scheme, self.path, self.slice, self.size)
        self.update()
        autoDiskPartition(self.slice, self.size, self.scheme)
        self.update()
        self.window.hide()

    def schemeEditor(self, data):
        self.window = Gtk.Window()
        self.window.set_title("Partition Scheme")
        self.window.set_border_width(0)
        self.window.set_size_request(400, 150)
        self.window.set_icon_from_file("/usr/local/lib/gbi/logo.png")
        box1 = Gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # Creating MBR or GPT drive
        label = Gtk.Label('<b>Select a partition scheme for this drive:</b>')
        label.set_use_markup(True)
        # Adding a combo box to selecting MBR or GPT sheme.
        self.scheme = 'GPT'
        shemebox = Gtk.ComboBoxText()
        shemebox.append_text("GPT: GUID Partition Table")
        shemebox.append_text("MBR: DOS Partition")
        shemebox.connect('changed', self.sheme_selection)
        shemebox.set_active(0)
        table = Gtk.Table(1, 2, True)
        table.attach(label, 0, 2, 0, 1)
        table.attach(shemebox, 0, 2, 1, 2)
        box2.pack_start(table, False, False, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        # Add create_scheme button
        bbox = Gtk.HButtonBox()
        bbox.set_border_width(5)
        bbox.set_spacing(10)
        button = Gtk.Button(stock=Gtk.STOCK_ADD)
        if data is None:
            button.connect("clicked", self.autoSchemePartition)
        else:
            button.connect("clicked", self.add_gpt_mbr)
        bbox.add(button)
        box2.pack_end(bbox, True, True, 5)
        self.window.show_all()

    def get_value(self, widget, entry):
        psize = int(entry.get_value_as_int())
        rs = int(self.size) - psize
        createSlice(psize, rs, self.path)
        self.update()
        self.window.hide()

    def sliceEditor(self):
        numb = int(self.size)
        self.window = Gtk.Window()
        self.window.set_title("Add Partition")
        self.window.set_border_width(0)
        self.window.set_size_request(400, 150)
        self.window.set_icon_from_file("/usr/local/lib/gbi/logo.png")
        box1 = Gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # create Partition slice
        # label = Gtk.Label('<b>Create a New Partition Slice</b>')
        # label.set_use_markup(True)
        # label.set_alignment(0, .5)
        table = Gtk.Table(1, 2, True)
        label1 = Gtk.Label("Size(MB):")
        adj = Gtk.Adjustment(numb, 0, numb, 1, 100, 0)
        self.entry = Gtk.SpinButton(adjustment=adj)
        self.entry.set_numeric(True)
        # table.attach(label, 0, 2, 0, 1)
        table.attach(label1, 0, 1, 1, 2)
        table.attach(self.entry, 1, 2, 1, 2)
        box2.pack_start(table, False, False, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        # Add button
        bbox = Gtk.HButtonBox()
        bbox.set_border_width(5)
        bbox.set_spacing(10)
        button = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        button.connect("clicked", self.cancel)
        bbox.add(button)
        button = Gtk.Button(stock=Gtk.STOCK_ADD)
        button.connect("clicked", self.get_value, self.entry)
        bbox.add(button)
        box2.pack_end(bbox, True, True, 5)
        self.window.show_all()

    def update(self):
        oldpath = self.path
        self.Tree_Store()
        self.treeview.expand_all()
        self.treeview.row_activated(oldpath, self.treeview.get_columns()[0])
        self.treeview.set_cursor(oldpath)

    def delete_partition(self, widget):
        part = self.slice
        Delete_partition(part, self.path)
        self.update()

    def delete_create_button(self):
        bbox = Gtk.HButtonBox()
        bbox.set_border_width(5)
        bbox.set_spacing(10)
        self.create_bt = Gtk.Button("Create")
        self.create_bt.connect("clicked", self.create_partition)
        bbox.add(self.create_bt)
        self.delete_bt = Gtk.Button("Delete")
        self.delete_bt.connect("clicked", self.delete_partition)
        bbox.add(self.delete_bt)
        self.modifi_bt = Gtk.Button("Modify")
        self.modifi_bt.connect("clicked", self.modify_partition)
        # bbox.add(self.modifi_bt)
        self.revert_bt = Gtk.Button("Revert")
        self.revert_bt.connect("clicked", self.revertChange)
        bbox.add(self.revert_bt)
        self.auto_bt = Gtk.Button("Auto")
        self.auto_bt.connect("clicked", self.autoPartition)
        bbox.add(self.auto_bt)
        return bbox

    def modify_partition(self, widget):
        if len(self.path) == 3:
            if self.slice != 'freespace':
                self.labelEditor(self.path, self.slice, self.size, 0, 0)
        elif len(self.path) == 2 and self.slice != 'freespace':
            if scheme_query(self.path) == "GPT":
                self.labelEditor(self.path, self.slice, self.size, 1, 0)

    def autoPartition(self, widget):
        if len(self.path) == 3:
            pass
        elif len(self.path) == 1 and self.scheme is None:
            self.schemeEditor(None)
            self.update()
        elif len(self.path) == 1:
            autoDiskPartition(self.slice, self.size, self.scheme)
            self.Tree_Store()
            self.treeview.expand_all()
            self.treeview.set_cursor(self.path)
        elif self.slice == 'freespace':
            autoFreeSpace(self.path, self.size)
            self.Tree_Store()
            self.treeview.expand_all()
            self.treeview.set_cursor(self.path)
        elif len(self.path) == 2:
            pass
        else:
            pass
        self.update()

    def revertChange(self, widget):
        if os.path.exists(partitiondb):
            shutil.rmtree(partitiondb)
        if os.path.exists(tmp + 'create'):
            os.remove(tmp + 'create')
        if os.path.exists(tmp + 'delete'):
            os.remove(tmp + 'delete')
        if os.path.exists(tmp + 'destroy'):
            os.remove(tmp + 'destroy')
        if os.path.exists(Part_label):
            os.remove(Part_label)
        partition_repos()
        self.Tree_Store()
        self.treeview.expand_all()

    def create_partition(self, widget):
        if len(self.path) == 3:
            if self.slice == 'freespace':
                self.labelEditor(self.path, self.slice, self.size, 0, 1)
        elif len(self.path) == 2 and self.slice == 'freespace':
            if scheme_query(self.path) == "MBR" and self.path[1] < 4:
                self.sliceEditor()
            elif scheme_query(self.path) == "GPT":
                self.labelEditor(self.path, self.slice, self.size, 1, 1)
        else:
            if how_partition(self.path) == 1:
                self.schemeEditor(True)
            elif how_partition(self.path) == 0:
                self.schemeEditor(True)
            else:
                pass

    def partition_selection(self, widget):
        model, self.iter, = widget.get_selected()
        if self.iter != None:
            self.path = model.get_path(self.iter)
            tree_iter3 = model.get_iter(self.path[0])
            self.scheme = model.get_value(tree_iter3, 3)
            tree_iter = model.get_iter(self.path)
            self.slice = model.get_value(tree_iter, 0)
            self.size = model.get_value(tree_iter, 1)
            if len(self.path) == 2 and self.path[1] > 0 and self.scheme == "MBR":
                pathbehind = str(self.path[0]) + ":" + str(int(self.path[1] - 1))
                tree_iter2 = model.get_iter(pathbehind)
                self.slicebehind = model.get_value(tree_iter2, 0)
                sl = int(self.path[1]) + 1
                if 'freespace' in self.slicebehind:
                    slbehind = self.path[1]
                else:
                    slbehind = int(self.slicebehind.partition('s')[2])
            elif len(self.path) == 2 and  self.path[1] > 0 and self.scheme == "GPT":
                pathbehind = str(self.path[0]) + ":" + str(int(self.path[1] - 1))
                tree_iter2 = model.get_iter(pathbehind)
                self.slicebehind = model.get_value(tree_iter2, 0)
                self.lablebehind = model.get_value(tree_iter2, 2)
                sl = int(self.path[1]) + 1
                if 'freespace' in self.slicebehind:
                    slbehind = self.path[1]
                else:
                    slbehind = int(self.slicebehind.partition('p')[2])
            elif len(self.path) == 3 and  self.path[2] > 0 and self.scheme == "MBR":
                if self.path[1] > 0:
                    pathbehind1 = str(self.path[0]) + ":" + str(int(self.path[1] - 1))
                    tree_iter2 = model.get_iter(pathbehind1)
                    self.slicebehind = model.get_value(tree_iter2, 0)
                else:
                    self.slicebehind = None
                pathbehind2 = str(self.path[0]) + ":" + str(self.path[1]) + ":" + str(int(self.path[2] - 1))
                tree_iter3 = model.get_iter(pathbehind2)
                self.lablebehind = model.get_value(tree_iter3, 2)
                sl = int(self.path[1]) + 1
                if self.slicebehind is None:
                    slbehind = self.path[1]
                elif 'freespace' in self.slicebehind:
                    slbehind = self.path[1]
                else:
                    slbehind = int(self.slicebehind.partition('s')[2])
            else:
                self.slicebehind = None
                self.lablebehind = None
                sl = 1
                slbehind = 0

            if 'freespace' in self.slice:
                if self.path[1] > 3 and self.scheme == "MBR":
                    self.create_bt.set_sensitive(False)
                elif self.slicebehind == None:
                    self.create_bt.set_sensitive(True)
                elif sl == slbehind:
                    self.create_bt.set_sensitive(False)
                elif slbehind > 4:
                    self.create_bt.set_sensitive(False)
                else:
                    self.create_bt.set_sensitive(True)
                self.delete_bt.set_sensitive(False)
                self.modifi_bt.set_sensitive(False)
                self.auto_bt.set_sensitive(True)
            elif 's' in self.slice:
                self.create_bt.set_sensitive(False)
                self.delete_bt.set_sensitive(True)
                #self.modifi_bt.set_sensitive(True)
                self.auto_bt.set_sensitive(False)
            elif 'p' in self.slice:
                self.create_bt.set_sensitive(False)
                self.delete_bt.set_sensitive(True)
                #self.modifi_bt.set_sensitive(True)
                self.auto_bt.set_sensitive(False)
            else:
                self.delete_bt.set_sensitive(False)
                self.modifi_bt.set_sensitive(False)
                self.auto_bt.set_sensitive(True)
                if how_partition(self.path) == 1:
                    self.create_bt.set_sensitive(True)
                elif how_partition(self.path) == 0:
                    self.create_bt.set_sensitive(True)
                else:
                    self.create_bt.set_sensitive(False)
        if os.path.exists(Part_label):
            rd = open(Part_label, 'r')
            self.partfile = rd.readlines()
            # If Find GPT scheme.
            if os.path.exists(disk_schem):
                rschm = open(disk_schem, 'r')
                schm = rschm.readlines()[0]
                if 'GPT' in schm:
                    if len(self.partfile) >= 2:
                        if 'BOOT' in self.partfile[0] or 'BIOS' in self.partfile[0] or 'UEFI' in self.partfile[0]:
                                if "/boot\n" in self.partfile[1]:
                                    if len(self.partfile) >= 3:
                                        if '/\n' in self.partfile[1]:
                                            self.button3.set_sensitive(True)
                                        else:
                                            self.button3.set_sensitive(False)
                                    else:
                                        self.button3.set_sensitive(False)
                                elif '/\n' in self.partfile[1]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                        else:
                            self.button3.set_sensitive(False)
                    else:
                        self.button3.set_sensitive(False)
                else:
                    if len(self.partfile) >= 1:
                        if "/boot\n" in self.partfile[0]:
                            if len(self.partfile) >= 2:
                                if '/\n' in self.partfile[1]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                            else:
                                self.button3.set_sensitive(False)
                        elif '/\n' in self.partfile[0]:
                            self.button3.set_sensitive(True)
                        else:
                            self.button3.set_sensitive(False)
                    else:
                        self.button3.set_sensitive(False)
            else:
                self.button3.set_sensitive(False)
        else:
                self.button3.set_sensitive(False)

    def __init__(self, button3):
        self.button3 = button3
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(0)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()
        # Title
        Title = Gtk.Label("<b><span size='xx-large'>Partition Editor</span></b> ")
        Title.set_use_markup(True)
        box2.pack_start(Title, False, False, 20)
        # Choosing disk to Select Create or delete partition.
        label = Gtk.Label("<b>Select a drive:</b>")
        label.set_use_markup(True)
        sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.store = Gtk.TreeStore(str, str, str, str, 'gboolean')
        self.Tree_Store()
        self.treeview = Gtk.TreeView(self.store)
        self.treeview.set_model(self.store)
        self.treeview.set_rules_hint(True)
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('Partition')
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
        column_header3 = Gtk.Label('Mount Point')
        column_header3.set_use_markup(True)
        column_header3.show()
        column3.set_widget(column_header3)
        cell4 = Gtk.CellRendererText()
        column4 = Gtk.TreeViewColumn(None, cell4, text=0)
        column_header4 = Gtk.Label('System/Type')
        column_header4.set_use_markup(True)
        column_header4.show()
        column4.set_widget(column_header4)
        column.set_attributes(cell, text=0)
        column2.set_attributes(cell2, text=1)
        column3.set_attributes(cell3, text=2)
        column4.set_attributes(cell4, text=3)
        self.treeview.append_column(column)
        self.treeview.append_column(column2)
        self.treeview.append_column(column3)
        self.treeview.append_column(column4)
        self.treeview.set_reorderable(True)
        self.treeview.expand_all()
        self.tree_selection = self.treeview.get_selection()
        self.tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.tree_selection.connect("changed", self.partition_selection)
        sw.add(self.treeview)
        sw.show()
        box2.pack_start(sw, True, True, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(10)
        self.box1.pack_start(box2, False, False, 10)
        box2.show()
        self.scheme = 'GPT'
        box2.pack_start(self.delete_create_button(),
                        False, False, 10)
        return

    def Tree_Store(self):
        self.store.clear()
        for disk in disk_query():
            shem = disk[-1]
            piter = self.store.append(None, [disk[0],
                                            str(disk[1]), disk[2], disk[3], True])
            if shem == "GPT":
                for pi in partition_query(disk[0]):
                    self.store.append(piter, [pi[0], str(pi[1]), pi[2], pi[3], True])
            elif shem == "MBR":
                for pi in partition_query(disk[0]):
                    piter1 = self.store.append(piter, [pi[0], str(pi[1]), pi[2], pi[3], True])
                    if pi[0] == 'freespace':
                        pass
                    else:
                        for li in label_query(pi[0]):
                            self.store.append(piter1, [li[0], str(li[1]), li[2], li[3], True])
        return self.store

    def get_model(self):
        self.tree_selection.select_path(0)
        return self.box1

