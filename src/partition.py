#!/usr/local/bin/python

import os
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from partition_handler import create_disk_partition_db, disk_database, Delete_partition
from partition_handler import bios_or_uefi, how_partition, createSlice
from partition_handler import autoFreeSpace, createPartition
from partition_handler import createLabel, diskSchemeChanger

# Folder use pr the installer.
tmp = "/tmp/.gbi"
if not os.path.exists(tmp):
    os.makedirs(tmp)
disk_scheme = f'{tmp}/scheme'
disk_file = f'{tmp}/disk'
slice_file = f'{tmp}/slice'
logo = "/usr/local/lib/gbi/logo.png"
partition_label_file = f'{tmp}/partlabel'

disk_db_file = f'{tmp}/disk.db'
ufs_Partiton_list = []
bios_type = bios_or_uefi()

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class Partitions():

    def set_fs(self, widget):
        self.fs = widget.get_active_text()
        if 'UFS' in self.fs:
            self.mountpoint_box.set_sensitive(True)
        else:
            self.mountpoint_box.set_sensitive(False)

    def get_mountpoint(self, widget):
        self.mountpoint = widget.get_active_text()

    def save_selection(self):
        pass

    def on_add_label(self, widget, entry, free_space, path, create):
        create_size = entry.get_value_as_int()
        left_size = free_space - create_size
        createLabel(path, self.disk, self.slice, left_size, create_size, self.mountpoint, self.fs)
        self.window.hide()
        self.update()

    def on_add_partition(self, widget, entry, free_space, path, create):
        create_size = entry.get_value_as_int()
        left_size = int(free_space - create_size)
        createPartition(path, self.disk, left_size, create_size, self.mountpoint, self.fs)
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
        self.fs_type = Gtk.ComboBoxText()
        self.fs_type.append_text('ZFS')
        self.fs_type.append_text('UFS')
        self.fs_type.append_text('UFS+S')
        self.fs_type.append_text('UFS+J')
        self.fs_type.append_text('UFS+SUJ')
        self.fs_type.append_text('SWAP')
        if scheme == 'GPT':
            if bios_type == "UEFI":
                self.fs_type.append_text("UEFI")
                if self.efi_exist is False:
                    self.fs_type.set_active(6)
                    self.fs = "UEFI"
                elif self.mountpoint_behind == "/" or self.fs_behind == "ZFS":
                    self.fs_type.set_active(5)
                    self.fs = "SWAP"
                else:
                    self.fs_type.set_active(0)
                    self.fs = "ZFS"
            else:
                self.fs_type.append_text("BOOT")
                if not os.path.exists(partition_label_file):
                    self.fs_type.set_active(5)
                    self.fs = "BOOT"
                elif len(self.partitions) == 0:
                    self.fs_type.set_active(5)
                    self.fs = "BOOT"
                elif self.mountpoint_behind == "/" or self.fs_behind == "ZFS":
                    self.fs_type.set_active(4)
                    self.fs = "SWAP"
                else:
                    self.fs_type.set_active(0)
                    self.fs = "ZSF"
        elif self.mountpoint_behind == "/" or self.fs_behind == "ZFS":
            self.fs_type.set_active(4)
            self.fs = "SWAP"
        else:
            self.fs_type.set_active(0)
            self.fs = "ZFS"
        self.fs_type.connect("changed", self.set_fs)
        adj = Gtk.Adjustment(free_space, 0, free_space, 1, 100, 0)
        self.entry = Gtk.SpinButton(adjustment=adj, numeric=True)
        if modify is True:
            self.entry.set_editable(False)
        else:
            self.entry.set_editable(True)
        self.mountpoint_box = Gtk.ComboBoxText()
        # self.mountpoint_box.append_text('select labels')
        self.mountpoint = "none"
        self.mountpoint_box.append_text('none')
        # The space for root '/ ' is to recognize / from the file.
        self.mountpoint_box.append_text('/')
        if os.path.exists(partition_label_file):
            if scheme == 'GPT' and len(self.partitions) == 1:
                self.mountpoint_box.append_text('/boot')
            elif scheme == 'MBR' and len(self.partitions) == 0:
                self.mountpoint_box.append_text('/boot')
        elif scheme == 'MBR' and not os.path.exists(partition_label_file):
            self.mountpoint_box.append_text('/boot')
        self.mountpoint_box.append_text('/etc')
        self.mountpoint_box.append_text('/root')
        self.mountpoint_box.append_text('/tmp')
        self.mountpoint_box.append_text('/usr')
        self.mountpoint_box.append_text('/usr/home')
        self.mountpoint_box.append_text('/var')
        self.mountpoint_box.set_active(0)
        if 'UFS' in self.fs:
            self.mountpoint_box.set_sensitive(True)
        else:
            self.mountpoint_box.set_sensitive(False)
        self.mountpoint_box.connect("changed", self.get_mountpoint)
        # table.attach(label0, 0, 2, 0, 1)
        table.attach(label1, 0, 1, 1, 2)
        table.attach(self.fs_type, 1, 2, 1, 2)
        table.attach(label2, 0, 1, 2, 3)
        table.attach(self.entry, 1, 2, 2, 3)
        table.attach(label3, 0, 1, 3, 4)
        table.attach(self.mountpoint_box, 1, 2, 3, 4)
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

    def on_fs(self, widget):
        self.fs = widget.get_active_text()

    def choose_fs(self):
        self.window = Gtk.Window()
        self.window.set_title("Choose file system")
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
        table = Gtk.Table(1, 2, True)
        label1 = Gtk.Label("File System:")
        self.fs_type = Gtk.ComboBoxText()
        self.fs_type.append_text('ZFS')
        self.fs_type.append_text('UFS')
        self.fs_type.append_text('UFS+S')
        self.fs_type.append_text('UFS+J')
        self.fs_type.append_text('UFS+SUJ')
        self.fs_type.set_active(0)
        self.fs = "ZFS"
        self.fs_type.connect("changed", self.on_fs)
        table.attach(label1, 0, 1, 1, 2)
        table.attach(self.fs_type, 1, 2, 1, 2)
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
        button.connect("clicked", self.set_auto_partition)
        bbox.add(button)
        box2.pack_end(bbox, True, True, 5)
        self.window.show_all()

    def set_auto_partition(self, widget):
        autoFreeSpace(self.path, self.size, self.fs, self.efi_exist, self.disk, self.scheme)
        self.window.hide()
        self.update()

    def scheme_selection(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        data = model[index][0]
        value = data.partition(':')[0]
        self.scheme = value

    def add_gpt_mbr(self, widget):
        diskSchemeChanger(self.scheme, self.path, self.disk, self.size)
        self.update()
        self.window.hide()

    def schemeEditor(self):
        self.window = Gtk.Window()
        self.window.set_title("Partition Scheme")
        self.window.set_border_width(0)
        self.window.set_size_request(400, 150)
        self.window.set_icon_from_file(logo)
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
        button.connect("clicked", self.add_gpt_mbr)
        bbox.add(button)
        box2.pack_end(bbox, True, True, 5)
        self.window.show_all()

    def get_value(self, widget, entry):
        partition_size = int(entry.get_value_as_int())
        rs = int(self.size) - partition_size
        createSlice(partition_size, rs, self.path, self.disk)
        self.update()
        self.window.hide()

    def sliceEditor(self):
        free_space = int(self.size)
        self.window = Gtk.Window()
        self.window.set_title("Add Partition")
        self.window.set_border_width(0)
        self.window.set_size_request(400, 150)
        self.window.set_icon_from_file(logo)
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
        part = self.slice if self.label == "Not selected" else self.label
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
            if 'freespace' not in self.slice:
                self.labelEditor(self.path, self.slice, self.size, 'MBR', True)
        elif len(self.path) == 2 and 'freespace' not in self.slice:
            if self.scheme == "GPT":
                self.labelEditor(self.path, self.slice, self.size, 'GPT', True)

    def autoPartition(self, widget):
        self.create_bt.set_sensitive(False)
        self.delete_bt.set_sensitive(False)
        self.modify_bt.set_sensitive(False)
        self.auto_bt.set_sensitive(False)
        self.revert_bt.set_sensitive(False)
        if 'freespace' in self.slice:
            self.choose_fs()
        else:
            print('wrong utilization')

    def revertChange(self, widget):
        if os.path.exists(f'{tmp}/create'):
            os.remove(f'{tmp}/create')
        if os.path.exists(disk_scheme):
            os.remove(disk_scheme)
        if os.path.exists(disk_file):
            os.remove(disk_file)
        if os.path.exists(slice_file):
            os.remove(slice_file)
        if os.path.exists(f'{tmp}/delete'):
            os.remove(f'{tmp}/delete')
        if os.path.exists(f'{tmp}/destroy'):
            os.remove(f'{tmp}/destroy')
        if os.path.exists(partition_label_file):
            os.remove(partition_label_file)
        create_disk_partition_db()
        self.Tree_Store()
        self.treeview.expand_all()

    def create_partition(self, widget):
        self.create_bt.set_sensitive(False)
        self.delete_bt.set_sensitive(False)
        self.modify_bt.set_sensitive(False)
        self.auto_bt.set_sensitive(False)
        self.revert_bt.set_sensitive(False)
        if self.change_schemes is True:
            self.schemeEditor()
        elif 'freespace' in self.label:
            self.labelEditor(self.path, self.slice, self.size, 'MBR', False)
        elif 'freespace' in self.slice:
            if self.scheme == "MBR" and self.path[1] < 4:
                self.sliceEditor()
            elif self.scheme == "GPT":
                self.labelEditor(self.path, self.slice, self.size, 'GPT', False)

    def partition_selection(self, widget):
        model, self.iter, = widget.get_selected()
        if self.iter is not None:
            self.path = model.get_path(self.iter)
            main_tree_iter = model.get_iter(self.path)
            self.size = model.get_value(main_tree_iter, 1)
            tree_iter1 = model.get_iter(self.path[0])
            self.scheme = model.get_value(tree_iter1, 3)
            self.disk = model.get_value(tree_iter1, 0)
            if len(self.path) >= 2:
                tree_iter2 = model.get_iter(self.path[:2])
                self.slice = model.get_value(tree_iter2, 0)
                self.change_schemes = False
            else:
                if len(self.path) == 1:
                    if how_partition(self.disk) == 1:
                        slice_path = f'{self.path[0]}:0'
                        tree_iter2 = model.get_iter(slice_path)
                        if 'freespace' in model.get_value(tree_iter2, 0):
                            self.change_schemes = True
                        else:
                            self.change_schemes = False
                    else:
                        self.change_schemes = False
                    self.slice = 'Not selected'
                else:
                    self.slice = 'Not selected'
                    self.change_schemes = False
            if len(self.path) == 3:
                tree_iter3 = model.get_iter(self.path[:3])
                self.label = model.get_value(tree_iter3, 0)
            else:
                self.label = 'Not selected'
            if len(self.path) == 2 and self.path[1] > 0 and self.scheme == "GPT":
                pathbehind = f'{self.path[0]}:{str(int(self.path[1] - 1))}'
                tree_iter4 = model.get_iter(pathbehind)
                self.mountpoint_behind = model.get_value(tree_iter4, 2)
                self.fs_behind = model.get_value(tree_iter4, 3)
            elif len(self.path) == 3 and self.path[2] > 0 and self.scheme == "MBR":
                pathbehind2 = f'{self.path[0]}:{str(self.path[1])}:{str(int(self.path[2] - 1))}'
                tree_iter1 = model.get_iter(pathbehind2)
                self.mountpoint_behind = model.get_value(tree_iter1, 2)
                self.fs_behind = model.get_value(tree_iter1, 3)
            else:
                self.mountpoint_behind = None
                self.fs_behind = None
            if 'freespace' in self.slice:
                self.create_bt.set_sensitive(True)
                self.delete_bt.set_sensitive(False)
                self.modify_bt.set_sensitive(False)
                self.auto_bt.set_sensitive(True)
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
            elif 'freespace' in self.label:
                if self.path[1] > 3:
                    self.create_bt.set_sensitive(False)
                else:
                    self.create_bt.set_sensitive(True)
                    self.auto_bt.set_sensitive(True)
                self.delete_bt.set_sensitive(False)
                self.modify_bt.set_sensitive(False)
            elif 's' in self.slice and len(self.path) > 1:
                self.create_bt.set_sensitive(False)
                self.delete_bt.set_sensitive(True)
                # self.modify_bt.set_sensitive(True)
                self.auto_bt.set_sensitive(False)
            elif 'p' in self.slice and len(self.path) > 1:
                self.create_bt.set_sensitive(False)
                self.delete_bt.set_sensitive(True)
                # self.modify_bt.set_sensitive(True)
                self.auto_bt.set_sensitive(False)
            else:
                self.delete_bt.set_sensitive(False)
                self.modify_bt.set_sensitive(False)
                self.auto_bt.set_sensitive(False)
                if how_partition(self.disk) == 0:
                    self.create_bt.set_sensitive(True)
                elif self.change_schemes is True:
                    self.create_bt.set_sensitive(True)
                else:
                    self.create_bt.set_sensitive(False)
        if os.path.exists(partition_label_file):
            rd = open(partition_label_file, 'r')
            self.partitions = rd.readlines()
            # Find if GPT scheme.
            if os.path.exists(disk_scheme):
                rschm = open(disk_scheme, 'r')
                schm = rschm.read()
                if 'GPT' in schm:
                    if os.path.exists(disk_file):
                        diskfile = open(disk_file, 'r')
                        disk = diskfile.readlines()[0].strip()
                        diskfile.close()
                        disk_id = self.disk_index.index(disk)
                        num = 0
                        while True:
                            partition_path = f"{disk_id}:{num}"
                            try:
                                first_tree_iter = model.get_iter(partition_path)
                                first_fs = model.get_value(first_tree_iter, 3)
                                if 'efi' in first_fs:
                                    efi_already_exist = True
                                    break
                            except ValueError:
                                efi_already_exist = False
                                break
                            num += 1
                    if 'BOOT' in self.partitions[0] and bios_type == 'BIOS':
                        if "/boot\n" in self.partitions[1]:
                            if len(self.partitions) >= 3:
                                if '/\n' in self.partitions[2]:
                                    self.button3.set_sensitive(True)
                                elif 'ZFS' in self.partitions[2]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                            else:
                                self.button3.set_sensitive(False)
                        elif '/\n' in self.partitions[1]:
                            self.button3.set_sensitive(True)
                        elif 'ZFS' in self.partitions[1]:
                            self.button3.set_sensitive(True)
                    elif efi_already_exist is True and bios_type == 'UEFI':
                        if '/\n' in self.partitions[0]:
                            self.button3.set_sensitive(True)
                        elif 'ZFS' in self.partitions[0]:
                            self.button3.set_sensitive(True)
                        elif "/boot\n" in self.partitions[0]:
                            if len(self.partitions) >= 2:
                                if '/\n' in self.partitions[1]:
                                    self.button3.set_sensitive(True)
                                elif 'ZFS' in self.partitions[1]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                            else:
                                self.button3.set_sensitive(False)
                        else:
                            self.button3.set_sensitive(False)
                    elif 'UEFI' in self.partitions[0] and '/\n' in self.partitions[1]:
                        self.button3.set_sensitive(True)
                    elif 'UEFI' in self.partitions[0] and 'ZFS' in self.partitions[1]:
                        self.button3.set_sensitive(True)
                    elif 'UEFI' in self.partitions[0] and "/boot\n" in self.partitions[1]:
                        if len(self.partitions) >= 3:
                            if '/\n' in self.partitions[2]:
                                self.button3.set_sensitive(True)
                            elif 'ZFS' in self.partitions[2]:
                                self.button3.set_sensitive(True)
                            else:
                                self.button3.set_sensitive(False)
                        else:
                            self.button3.set_sensitive(False)
                    else:
                        self.button3.set_sensitive(False)
                else:
                    # to be changed when MBR UEFI will be supported by pc-sysinstall.
                    self.efi_exist = False
                    if len(self.partitions) >= 1:
                        if "/boot\n" in self.partitions[0]:
                            if len(self.partitions) >= 2:
                                if '/\n' in self.partitions[1]:
                                    self.button3.set_sensitive(True)
                                elif 'ZFS' in self.partitions[1]:
                                    self.button3.set_sensitive(True)
                                else:
                                    self.button3.set_sensitive(False)
                            else:
                                self.button3.set_sensitive(False)
                        elif '/\n' in self.partitions[0]:
                            self.button3.set_sensitive(True)
                        elif 'ZFS' in self.partitions[0]:
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
            os.path.exists(f'{tmp}/create'),
            os.path.exists(disk_scheme),
            os.path.exists(disk_file),
            os.path.exists(slice_file),
            os.path.exists(f'{tmp}/delete'),
            os.path.exists(f'{tmp}/destroy'),
            os.path.exists(partition_label_file)
        ]
        if any(path_exist):
            self.revert_bt.set_sensitive(True)
        else:
            self.revert_bt.set_sensitive(False)

    def __init__(self, button3):
        self.button3 = button3
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        # Title
        Title = Gtk.Label("Partition Editor", name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
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
        column.set_resizable(True)
        column.set_fixed_width(150)
        column.set_sort_column_id(0)
        cell2 = Gtk.CellRendererText()
        column2 = Gtk.TreeViewColumn(None, cell2, text=0)
        column_header2 = Gtk.Label('Size(MB)')
        column_header2.set_use_markup(True)
        column_header2.show()
        column2.set_widget(column_header2)
        column2.set_resizable(True)
        column2.set_fixed_width(150)
        cell3 = Gtk.CellRendererText()
        column3 = Gtk.TreeViewColumn(None, cell3, text=0)
        column_header3 = Gtk.Label('Mount Point')
        column_header3.set_use_markup(True)
        column_header3.show()
        column3.set_widget(column_header3)
        column3.set_resizable(True)
        column3.set_fixed_width(150)
        cell4 = Gtk.CellRendererText()
        column4 = Gtk.TreeViewColumn(None, cell4, text=0)
        column_header4 = Gtk.Label('System/Type')
        column_header4.set_use_markup(True)
        column_header4.show()
        column4.set_widget(column_header4)
        column4.set_resizable(True)
        column4.set_fixed_width(150)
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
        self.vbox1.pack_start(sw, True, True, 0)
        hbox1 = Gtk.HBox(False, 0)
        hbox1.set_border_width(10)
        self.vbox1.pack_start(hbox1, False, False, 0)
        hbox1.show()
        self.scheme = 'GPT'
        hbox1.pack_start(self.delete_create_button(), False, False, 10)
        return

    def Tree_Store(self):
        self.store.clear()
        disk_db = disk_database()
        self.disk_index = list(disk_db.keys())
        for disk in disk_db:
            disk_info = disk_db[disk]
            disk_schemee = disk_info['scheme']
            mount_point = ''
            disk_size = str(disk_info['size'])
            disk_partitions = disk_info['partitions']
            partition_list = disk_info['partition_list']
            pinter1 = self.store.append(None, [disk, disk_size, mount_point, disk_schemee, True])
            for partition in partition_list:
                partition_info = disk_partitions[partition]
                file_system = partition_info['file_system']
                mount_point = partition_info['mount_point']
                partition_size = str(partition_info['size'])
                partition_partitions = partition_info['partitions']
                partition_list = partition_info['partition_list']
                pinter2 = self.store.append(pinter1, [partition, partition_size, mount_point, file_system, True])
                for partition in partition_list:
                    partition_info = partition_partitions[partition]
                    file_system = partition_info['file_system']
                    mount_point = partition_info['mount_point']
                    partition_size = str(partition_info['size'])
                    self.store.append(pinter2, [partition, partition_size, mount_point, file_system, True])
        return self.store

    def get_model(self):
        self.tree_selection.select_path(0)
        return self.vbox1
