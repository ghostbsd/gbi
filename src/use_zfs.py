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

import gtk
import os
import os.path
import re
from subprocess import Popen, PIPE, STDOUT
from defutil import use_disk_bbox, close_application, root_window, type_window
from partition_handler import zfs_disk_query, zfs_disk_size_query

# Folder use pr the installer.
tmp = "/home/ghostbsd/.gbi/"
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
Part_label = '%szfs_partition' % tmp
part_schem = '%sscheme' % tmp
zfs_dsk_list = []
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


class ZFS():
    def zfs_bbox(self, horizontal, spacing, layout):
        bbox = gtk.HButtonBox()
        bbox.set_border_width(5)
        bbox.set_layout(layout)
        bbox.set_spacing(spacing)
        button = gtk.Button(stock=gtk.STOCK_GO_BACK)
        bbox.add(button)
        button.connect("clicked", type_window)
        button = gtk.Button(stock=gtk.STOCK_CANCEL)
        bbox.add(button)
        button.connect("clicked", close_application)
        self.forward_button = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
        bbox.add(self.forward_button)
        self.forward_button.connect("clicked", self.next_to_root)
        return bbox

    def next_to_root(self, widget):
        SIZE = int(zfs_dsk_list[0].partition('-')[2].rstrip())
        SWAP = int(self.swap_entry.get_text())
        ZFS_NUM = SIZE - SWAP
        pfile = open(Part_label, 'w')
        pfile.writelines('ZFS %s /\n' % ZFS_NUM)
        pfile.writelines('SWAP %s none\n' % SWAP)
        pfile.close()
        # Popen(to_root, shell=True)
        # gtk.main_quit()


    def sheme_selection(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        data = model[index][0]
        self.scheme = data.partition(':')[0]
        
    def mirror_selection(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        data = model[index][0]
        self.mirror = data

    def on_check_poll(self, widget):
        if widget.get_active():
            self.pool.set_sensitive(True)
            self.zpool = True
        else:
            self.pool.set_sensitive(False)
            self.zpool = False

    def on_check(self, widget):
        if widget.get_active():
            self.zfs_four_k = "True"
        else:
            self.zfs_four_k = "False"

    def on_check_encrypt(self, widget):
        if widget.get_active():
            self.password.set_sensitive(True)
            self.repassword.set_sensitive(True)
            self.disk_encript = True
            self.swap_encrypt_check.set_active(True)
        else:
            self.password.set_sensitive(False)
            self.repassword.set_sensitive(False)
            self.disk_encript = False
            self.swap_encrypt_check.set_active(False)

    def on_check_swap_encrypt(self, widget):
        if widget.get_active():
            self.swap_encrypt = "True"
        else:
            self.swap_encrypt = "False"
            
    def on_check_swap_mirror(self, widget):
        if widget.get_active():
            self.swap_mirror = "True"
        else:
            self.swap_mirror = "False"

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("destroy", close_application)
        window.set_size_request(700, 500)
        window.set_resizable(False)
        window.set_title("GhostBSD Installer")
        window.set_border_width(0)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_icon_from_file("/usr/local/lib/gbi/logo.png")
        box1 = gtk.VBox(False, 0)
        window.add(box1)
        box1.show()
        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # Title
        Title = gtk.Label("<b><span size='xx-large'>ZFS Configuration</span></b>")
        Title.set_use_markup(True)
        box2.pack_start(Title, False, False, 0)
        # Chose disk
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        store = gtk.TreeStore(str, str, str,'gboolean')
        for disk in zfs_disk_query():
            print disk
            dsk = disk.partition(':')[0].rstrip()
            print dsk
            dsk_name = disk.partition(':')[2].rstrip()
            dsk_size = zfs_disk_size_query(dsk).rstrip()
            store.append(None, [dsk, dsk_size, dsk_name, False])
        treeView = gtk.TreeView(store)
        treeView.set_model(store)
        treeView.set_rules_hint(True)
        self.check_cell = gtk.CellRendererToggle()
        self.check_cell.set_property('activatable', True)
        self.check_cell.connect('toggled', self.col1_toggled_cb, store)
        cell = gtk.CellRendererText()
        column = gtk.TreeViewColumn(None, cell, text=0)
        column_header = gtk.Label('Disk')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        cell2 = gtk.CellRendererText()
        column2 = gtk.TreeViewColumn(None, cell2, text=0)
        column_header2 = gtk.Label('Size(MB)')
        column_header2.set_use_markup(True)
        column_header2.show()
        column2.set_widget(column_header2)
        cell3 = gtk.CellRendererText()
        column3 = gtk.TreeViewColumn(None, cell3, text=0)
        column_header3 = gtk.Label('Name')
        column_header3.set_use_markup(True)
        column_header3.show()
        column3.set_widget(column_header3)
        column1 = gtk.TreeViewColumn("Check", self.check_cell)
        column1.add_attribute(self.check_cell, "active", 3)
        column.set_attributes(cell, text=0)
        column2.set_attributes(cell2, text=1)
        column3.set_attributes(cell3, text=2)
        treeView.append_column(column1)
        treeView.append_column(column)
        treeView.append_column(column2)
        treeView.append_column(column3)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(gtk.SELECTION_SINGLE)
        sw.add(treeView)
        sw.show()
        # Mirro, raidz and strip 
        self.mirror = 'None'
        mirror_label = gtk.Label('<b>Pool Type</b>')
        mirror_label.set_use_markup(True)
        mirror_box = gtk.combo_box_new_text()
        mirror_box.append_text("None")
        mirror_box.append_text("mirror")
        mirror_box.append_text("raidz1")
        mirror_box.append_text("raidz2")
        mirror_box.append_text("raidz3")
        mirror_box.append_text("striop")
        mirror_box.connect('changed', self.mirror_selection)
        mirror_box.set_active(0)
        # Pool Name
        self.zpool = False
        pool_check = gtk.CheckButton('Pool Name')
        pool_check.connect("toggled", self.on_check_poll)
        self.pool = gtk.Entry()
        self.pool.set_text('zroot')
        self.pool.set_sensitive(False)
        # Creating MBR or GPT drive
        label = gtk.Label('<b>Partition Scheme</b>')
        label.set_use_markup(True)
        # Adding a combo box to selecting MBR or GPT sheme.
        self.scheme = 'GPT'
        shemebox = gtk.combo_box_new_text()
        shemebox.append_text("GPT")
        shemebox.append_text("MBR")
        shemebox.connect('changed', self.sheme_selection)
        shemebox.set_active(0)
        # Force 4k Sectors
        self.zfs_four_k = "False"
        check = gtk.CheckButton("Force ZFS 4k block size")
        check.connect("toggled", self.on_check)
        # Swap Size
        ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
        close_fds=True)
        mem = ram.stdout.read()
        swap = int(mem.partition(':')[2].strip()) / (1024 * 1024)
        swp_size_label = gtk.Label('<b>Swap Size(MB)</b>')
        swp_size_label.set_use_markup(True)
        self.swap_entry = gtk.Entry()
        self.swap_entry.set_text(str(swap))
        self.swap_entry.connect('changed', self.digit_only)
        # Swap encription
        self.swap_encrypt = False
        self.swap_encrypt_check = gtk.CheckButton("Encrypt Swap")
        self.swap_encrypt_check.connect("toggled", self.on_check_swap_encrypt)
        # Swap mirror
        self.swap_mirror = False
        swap_mirror_check = gtk.CheckButton("Mirror Swap")
        swap_mirror_check.connect("toggled", self.on_check_swap_mirror)
        # GELI Disk encription
        self.disk_encript = False
        encrypt_check = gtk.CheckButton("Encrypt Disk")
        encrypt_check.connect("toggled", self.on_check_encrypt)
        # password
        self.passwd_label = gtk.Label("Password")
        self.password = gtk.Entry()
        self.password.set_sensitive(False)
        self.password.set_visibility(False)

        self.password.connect("changed", self.passwdstrength)
        self.strenght_label = gtk.Label()
        self.vpasswd_label = gtk.Label("Verify it")
        self.repassword = gtk.Entry()
        self.repassword.set_sensitive(False)
        self.repassword.set_visibility(False)
        self.repassword.connect("changed", self.passwdVerification)
        # set image for password matching
        self.img = gtk.Image()
        table = gtk.Table(1, 16, True)
        table.attach(mirror_label, 0, 4, 1, 2)
        table.attach(mirror_box, 4, 7, 1, 2)
        table.attach(label, 9, 12, 1, 2)
        table.attach(shemebox, 12, 15, 1, 2)
        table.attach(sw, 1, 15, 3, 6)
        table.attach(pool_check, 1, 4, 7, 8)
        table.attach(self.pool, 4, 7, 7, 8)
        table.attach(check, 9, 15, 7, 8)
        table.attach(swp_size_label, 9, 12, 9, 10)
        table.attach(self.swap_entry, 12, 15, 9, 10)
        table.attach(self.swap_encrypt_check, 9, 15, 10, 11)
        table.attach(swap_mirror_check, 9, 15, 11, 12)
        table.attach(encrypt_check, 1, 7, 9, 10)
        table.attach(self.passwd_label, 1, 3, 10, 11)
        table.attach(self.password, 3, 7, 10, 11)
        table.attach(self.strenght_label, 7, 9, 10, 11)
        table.attach(self.vpasswd_label, 1, 3, 11, 12)
        table.attach(self.repassword, 3, 7, 11, 12)
        table.attach(self.img, 7, 8, 11, 12)
        box2.pack_start(table, False, False, 0)
        box2 = gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, False, 0)
        box2.show()
        # Add button
        box2.pack_start(self.zfs_bbox(True,
                        10, gtk.BUTTONBOX_END),
                        True, True, 5)
        window.show_all()

    def digit_only(self, *args):
        text = self.swap_entry.get_text().strip()
        self.swap_entry.set_text(''.join([i for i in text if i in '0123456789']))

    def col1_toggled_cb(self, cell, path, model):
        model[path][3] = not model[path][3]
        if model[path][3] is False:
            zfs_dsk_list.remove(model[path][0] + "-" + model[path][1])
        else:
            zfs_dsk_list.extend([model[path][0] + "-" + model[path][1]])
        return

    def passwdstrength(self, widget):
        passwd = self.password.get_text()
        if len(passwd) <= 4:
            self.strenght_label.set_text("Super Weak")
        elif len(passwd) <= 8:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.strenght_label.set_text("Super Weak")
            elif lowerandNunber(passwd):
                self.strenght_label.set_text("Very Weak")
            elif upperandNunber(passwd):
                self.strenght_label.set_text("Very Weak")
            elif lowerUpperCase(passwd):
                self.strenght_label.set_text("Very Weak")
            elif lowerUpperNumber(passwd):
                self.strenght_label.set_text("Fairly Weak")
            elif allCharacter(passwd):
                self.strenght_label.set_text("Weak")
        elif len(passwd) <= 12:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.strenght_label.set_text("Very Weak")
            elif lowerandNunber(passwd):
                self.strenght_label.set_text("Fairly Weak")
            elif upperandNunber(passwd):
                self.strenght_label.set_text("Fairly Weak")
            elif lowerUpperCase(passwd):
                self.strenght_label.set_text("Fairly Weak")
            elif lowerUpperNumber(passwd):
                self.strenght_label.set_text("Weak")
            elif allCharacter(passwd):
                self.strenght_label.set_text("Strong")
        elif len(passwd) <= 16:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.strenght_label.set_text("Fairly Weak")
            elif lowerandNunber(passwd):
                self.strenght_label.set_text("Weak")
            elif upperandNunber(passwd):
                self.strenght_label.set_text("Weak")
            elif lowerUpperCase(passwd):
                self.strenght_label.set_text("Weak")
            elif lowerUpperNumber(passwd):
                self.strenght_label.set_text("Strong")
            elif allCharacter(passwd):
                self.strenght_label.set_text("Fairly Strong")
        elif len(passwd) <= 20:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.strenght_label.set_text("Weak")
            elif lowerandNunber(passwd):
                self.strenght_label.set_text("Strong")
            elif upperandNunber(passwd):
                self.strenght_label.set_text("Strong")
            elif lowerUpperCase(passwd):
                self.strenght_label.set_text("Strong")
            elif lowerUpperNumber(passwd):
                self.strenght_label.set_text("Fairly Strong")
            elif allCharacter(passwd):
                self.strenght_label.set_text("Very Strong")
        elif len(passwd) <= 24:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.strenght_label.set_text("Strong")
            elif lowerandNunber(passwd):
                self.strenght_label.set_text("Fairly Strong")
            elif upperandNunber(passwd):
                self.strenght_label.set_text("Fairly Strong")
            elif lowerUpperCase(passwd):
                self.strenght_label.set_text("Fairly Strong")
            elif lowerUpperNumber(passwd):
                self.strenght_label.set_text("Very Strong")
            elif allCharacter(passwd):
                self.strenght_label.set_text("Super Strong")
        elif len(passwd) > 24:
            if lowerCase(passwd) or upperCase(passwd) or passwd.isdigit():
                self.strenght_label.set_text("Fairly Strong")
            else:
                self.strenght_label.set_text("Super Strong")

    def passwdVerification(self, widget):
        if self.password.get_text() == self.repassword.get_text():
            self.img.set_from_stock(gtk.STOCK_YES, 10)
        else:
            self.img.set_from_stock(gtk.STOCK_NO, 10)

ZFS()
gtk.main()