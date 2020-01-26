#!/usr/local/bin/python

import os
import shutil
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from partition_handler import partition_repos, disk_query, Delete_partition
from partition_handler import partition_query, label_query, bios_or_uefi
from partition_handler import autoDiskPartition, autoFreeSpace, first_is_free
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
partition_db = "%spartition_db/" % tmp
ufs_Partiton_list = []
bios_type = bios_or_uefi()


class Partitions():

    def on_fs(self, widget):
        self.fs = widget.get_active_text()

    def on_label(self, widget):
        self.label = widget.get_active_text()

    def save_selection(self):
        pass

    def on_add_label(self, widget, entry, free_space, path, create):
        if self.fs == '' or self.label == '':
            pass
        else:
            fs = self.fs
            lb = self.label
            create_size = entry.get_value_as_int()
            left_size = free_space - create_size
            createLabel(path, self.disk, self.slicebehind, left_size, create_size, lb, fs, create)
        self.window.hide()
        self.update()

    def on_add_partition(self, widget, entry, free_space, path, create):
        if self.fs == '' or self.label == '':
            pass
        else:
            fs = self.fs
            lb = self.label
            create_size = entry.get_value_as_int()
            left_size = int(free_space - create_size)
            createPartition(path, self.disk, self.slicebehind, left_size, create_size, lb, fs, create)
        self.window.hide()
        self.update()

    def cancel(self, widget):
        self.window.hide()
        self.update()

    def labelEditor(self, path, pslice, size, scheme, modify):
        free_space = int(size)
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
        if scheme == 'GPT':
            if bios_type == "UEFI":
                self.fstype.append_text("UEFI")
                if self.efi_exist is False:
                    self.fstype.set_active(5)
                    self.fs = "UEFI"
                elif self.lablebehind == "/":
                    self.fstype.set_active(4)
                    self.fs = "SWAP"
                else:
                    self.fstype.set_active(3)
                    self.fs = "UFS+SUJ"
            else:
                self.fstype.append_text("BOOT")
                if not os.path.exists(Part_label):
                    self.fstype.set_active(5)
                    self.fs = "BOOT"
                elif len(self.prttn) == 0:
                    self.fstype.set_active(5)
                    self.fs = "BOOT"
                elif self.lablebehind == "/":
                    self.fstype.set_active(4)
                    self.fs = "SWAP"
                else:
                    self.fstype.set_active(3)
                    self.fs = "UFS+SUJ"
        elif self.lablebehind == "/":
            self.fstype.set_active(4)
            self.fs = "SWAP"
        else:
            self.fstype.set_active(3)
            self.fs = "UFS+SUJ"
        self.fstype.connect("changed", self.on_fs)
        adj = Gtk.Adjustment(free_space, 0, free_space, 1, 100, 0)
        self.entry = Gtk.SpinButton(adjustment=adj, numeric=True)
        if modify is True:
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
            if scheme == 'GPT' and len(self.prttn) == 1:
                self.mountpoint.append_text('/boot')
            elif scheme == 'MBR' and len(self.prttn) == 0:
                self.mountpoint.append_text('/boot')
        elif scheme == 'MBR' and not os.path.exists(Part_label):
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
        if modify is False:
            if scheme == 'MBR':
                button.connect("clicked", self.on_add_label, self.entry,
                               free_space, path, True)
            elif scheme == 'GPT' and self.fs == 'BOOT':
                button.connect("clicked", self.on_add_partition, self.entry,
                               free_space, path, True)
            elif scheme == 'GPT' and self.fs == 'UEFI' and self.efi_exist is False:
                button.connect("clicked", self.on_add_partition, self.entry,
                               free_space, path, True)
            else:
                button.connect("clicked", self.on_add_partition, self.entry,
                               free_space, path, False)
        else:
            if scheme == 'MBR':
                button.connect("clicked", self.on_add_label, self.entry, free_space,
                               path, False)
            elif scheme == 'GPT':
                button.connect("clicked", self.on_add_partition, self.entry,
                               free_space, path, False)
        bbox.add(button)
        box2.pack_end(bbox, True, True, 5)
        self.window.show_all()

    def scheme_selection(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        data = model[index][0]
        value = data.partition(':')[0]
        self.scheme = value

    def add_gpt_mbr(self, widget, data):
        diskSchemeChanger(self.scheme, self.path, self.slice, self.size)
        self.update()
        self.window.hide()
        if data is False:
            if scheme_query(self.path) == "MBR" and self.path[1] < 4:
                self.sliceEditor()
            elif scheme_query(self.path) == "GPT":
                self.labelEditor(self.path, self.slice, self.size, 'GPT', False)

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
        # Adding a combo box to selecting MBR or GPT scheme.
        self.scheme = 'GPT'
        scheme_box = Gtk.ComboBoxText()
        scheme_box.append_text("GPT: GUID Partition Table")
        scheme_box.append_text("MBR: DOS Partition")
        scheme_box.connect('changed', self.scheme_selection)
        scheme_box.set_active(0)
        table = Gtk.Table(1, 2, True)
        table.attach(label, 0, 2, 0, 1)
        table.attach(scheme_box, 0, 2, 1, 2)
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
            button.connect("clicked", self.add_gpt_mbr, data)
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
        free_space = int(self.size)
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
        adj = Gtk.Adjustment(free_space, 0, free_space, 1, 100, 0)
        self.entry = Gtk.SpinButton(adjustment=adj, numeric=True)
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
        self.modify_bt = Gtk.Button("Modify")
        self.modify_bt.connect("clicked", self.modify_partition)
        # bbox.add(self.modify_bt)
        self.revert_bt = Gtk.Button("Revert")
        self.revert_bt.connect("clicked", self.revertChange)
        self.revert_bt.set_sensitive(False)
        bbox.add(self.revert_bt)
        self.auto_bt = Gtk.Button("Auto")
        self.auto_bt.connect("clicked", self.autoPartition)
        bbox.add(self.auto_bt)
        return bbox

    def modify_partition(self, widget):
        if len(self.path) == 3:
            if self.slice != 'freespace':
                self.labelEditor(self.path, self.slice, self.size, 'MBR', True)
        elif len(self.path) == 2 and self.slice != 'freespace':
            if scheme_query(self.path) == "GPT":
                self.labelEditor(self.path, self.slice, self.size, 'GPT', True)

    def autoPartition(self, widget):
        if len(self.path) == 3:
            pass
        # elif len(self.path) == 1 and self.scheme is None:
        #    self.schemeEditor(None)
        #    self.update()
        # elif len(self.path) == 1:
        #    autoDiskPartition(self.slice, self.size, self.scheme)
        #    self.Tree_Store()
        #    self.treeview.expand_all()
        #    self.treeview.set_cursor(self.path)
        elif self.slice == 'freespace':
            autoFreeSpace(self.path, self.size, self.efi_exist)
            self.Tree_Store()
            self.treeview.expand_all()
            self.treeview.set_cursor(self.path)
        elif len(self.path) == 2:
            pass
        else:
            pass
        self.update()

    def revertChange(self, widget):
        if os.path.exists(partition_db):
            shutil.rmtree(partition_db)
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
        self.create_bt.set_sensitive(False)
        self.delete_bt.set_sensitive(False)
        self.modify_bt.set_sensitive(False)
        self.auto_bt.set_sensitive(False)
        self.revert_bt.set_sensitive(False)
        if len(self.path) == 2 and how_partition(self.path) == 1 and self.slice == 'freespace':
            self.schemeEditor(False)
        elif len(self.path) == 3:
            if self.slice == 'freespace':
                self.labelEditor(self.path, self.slice, self.size, 'MBR', False)
        elif len(self.path) == 2 and self.slice == 'freespace':
            if scheme_query(self.path) == "MBR" and self.path[1] < 4:
                self.sliceEditor()
            elif scheme_query(self.path) == "GPT":
                self.labelEditor(self.path, self.slice, self.size, 'GPT', False)
        else:
            if how_partition(self.path) == 1:
                self.schemeEditor(True)
            elif how_partition(self.path) == 0:
                self.schemeEditor(True)
            else:
                pass

    def partition_selection(self, widget):
        model, self.iter, = widget.get_selected()
        if self.iter is not None:
            self.path = model.get_path(self.iter)
            tree_iter3 = model.get_iter(self.path[0])
            self.scheme = model.get_value(tree_iter3, 3)
            self.disk = model.get_value(tree_iter3, 0)
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
            elif len(self.path) == 2 and self.path[1] > 0 and self.scheme == "GPT":
                pathbehind = str(self.path[0]) + ":" + str(int(self.path[1] - 1))
                tree_iter2 = model.get_iter(pathbehind)
                self.slicebehind = model.get_value(tree_iter2, 0)
                self.lablebehind = model.get_value(tree_iter2, 2)
                sl = int(self.path[1]) + 1
                if 'freespace' in self.slicebehind:
                    slbehind = self.path[1]
                else:
                    slbehind = int(self.slicebehind.partition('p')[2])
            elif len(self.path) == 3 and self.path[2] > 0 and self.scheme == "MBR":
                if self.path[2] > 0:
                    pathbehind1 = str(self.path[0]) + ":" + str(self.path[1]) + ":" + str(int(self.path[2] - 1))
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
                elif self.slicebehind is None:
                    self.create_bt.set_sensitive(True)
                elif sl == slbehind:
                    self.create_bt.set_sensitive(False)
                # elif slbehind > 4:
                #     self.create_bt.set_sensitive(False)
                else:
                    self.create_bt.set_sensitive(True)
                self.delete_bt.set_sensitive(False)
                self.modify_bt.set_sensitive(False)
                # scan for efi partition
                for num in range(self.path[1]):
                    partition_path = f"{self.path[0]}:{num}"
                    first_tree_iter = model.get_iter(partition_path)
                    first_fs = model.get_value(first_tree_iter, 3)
                    if first_fs == "UEFI" or 'efi' in first_fs:
                        self.efi_exist = True
                        break
                else:
                    self.efi_exist = False
                self.auto_bt.set_sensitive(True)
            elif 's' in self.slice:
                self.create_bt.set_sensitive(False)
                self.delete_bt.set_sensitive(True)
                # self.modify_bt.set_sensitive(True)
                self.auto_bt.set_sensitive(False)
            elif 'p' in self.slice:
                self.create_bt.set_sensitive(False)
                self.delete_bt.set_sensitive(True)
                # self.modify_bt.set_sensitive(True)
                self.auto_bt.set_sensitive(False)
            else:
                self.delete_bt.set_sensitive(False)
                self.modify_bt.set_sensitive(False)
                self.auto_bt.set_sensitive(False)
                how_many_prt = how_partition(self.path)
                firstisfree = first_is_free(self.path)
                if how_many_prt == 1 and firstisfree == 'freespace':
                    self.create_bt.set_sensitive(False)
                elif how_partition(self.path) == 0:
                    self.create_bt.set_sensitive(True)
                else:
                    self.create_bt.set_sensitive(False)
        if os.path.exists(Part_label):
            rd = open(Part_label, 'r')
            self.prttn = rd.readlines()
            print(self.prttn)
            # Find if GPT scheme.
            if os.path.exists(disk_schem):
                rschm = open(disk_schem, 'r')
                schm = rschm.readlines()[0]
                if 'GPT' in schm:
                    if os.path.exists(disk_file):
                        diskfile = open(disk_file, 'r')
                        disk = diskfile.readlines()[0].strip()
                        diskfile.close()
                        disk_num = re.sub("[^0-9]", "", disk)
                        num = 0
                        while True:
                            partition_path = f"{disk_num}:{num}"
                            try:
                                first_tree_iter = model.get_iter(partition_path)
                                first_fs = model.get_value(first_tree_iter, 3)
                                if first_fs == "UEFI" or 'efi' in first_fs:
                                    self.efi_exist = True
                                    break
                            except ValueError:
                                self.efi_exist = False
                                break
                            num += 1
                    if 'BOOT' in self.prttn[0] and bios_type == 'BIOS':
                        if "/boot\n" in self.prttn[1]:
                            if len(self.prttn) >= 3:
                                if '/\n' in self.prttn[2]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                            else:
                                self.button3.set_sensitive(False)
                        elif '/\n' in self.prttn[1]:
                            self.button3.set_sensitive(True)
                        else:
                            self.button3.set_sensitive(False)
                    elif self.efi_exist is True and bios_type == 'UEFI':
                        if '/\n' in self.prttn[0]:
                            self.button3.set_sensitive(True)
                        elif "/boot\n" in self.prttn[0]:
                            if len(self.prttn) >= 2:
                                if '/\n' in self.prttn[1]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                            else:
                                self.button3.set_sensitive(False)
                        elif 'UEFI' in self.prttn[0] and '/\n' in self.prttn[1]:
                            self.button3.set_sensitive(True)
                        elif 'UEFI' in self.prttn[0] and "/boot\n" in self.prttn[0]:
                            if len(self.prttn) >= 3:
                                if '/\n' in self.prttn[2]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                            else:
                                self.button3.set_sensitive(False)
                        else:
                            self.button3.set_sensitive(False)
                    else:
                        self.button3.set_sensitive(False)
                else:
                    # to be changed when MBR UEFI will be supported in the backend.
                    self.efi_exist = False
                    if len(self.prttn) >= 1:
                        if "/boot\n" in self.prttn[0]:
                            if len(self.prttn) >= 2:
                                if '/\n' in self.prttn[1]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                            else:
                                self.button3.set_sensitive(False)
                        elif '/\n' in self.prttn[0]:
                            self.button3.set_sensitive(True)
                        else:
                            self.button3.set_sensitive(False)
                    else:
                        self.button3.set_sensitive(False)
            else:
                self.button3.set_sensitive(False)
        else:
            self.button3.set_sensitive(False)
        path_exist = [
            os.path.exists(Part_label),
            os.path.exists(disk_schem),
            os.path.exists(disk_file),
            os.path.exists(psize),
            os.path.exists(part_schem)
        ]
        if any(path_exist):
            self.revert_bt.set_sensitive(True)
        else:
            self.revert_bt.set_sensitive(False)

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
        # Choosing disk to Select Create, delete partition.
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
            schem = disk[-1]
            pinter = self.store.append(None, [disk[0], str(disk[1]),
                                       disk[2], disk[3], True])
            if schem == "GPT":
                for pi in partition_query(disk[0]):
                    self.store.append(pinter, [pi[0], str(pi[1]), pi[2],
                                      pi[3], True])
            elif schem == "MBR":
                for pi in partition_query(disk[0]):
                    pinter1 = self.store.append(pinter, [pi[0], str(pi[1]),
                                                pi[2], pi[3], True])
                    if pi[0] == 'freespace':
                        pass
                    else:
                        for li in label_query(pi[0]):
                            self.store.append(pinter1, [li[0], str(li[1]),
                                              li[2], li[3], True])
        return self.store

    def get_model(self):
        self.tree_selection.select_path(0)
        return self.box1
