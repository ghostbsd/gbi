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
from gi.repository import Gtk, GObject
import os
import os.path
import re
from subprocess import Popen, PIPE, STDOUT
from partition_handler import zfs_disk_query, zfs_disk_size_query, bios_or_uefi

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
Part_label = '%szfs_config' % tmp
part_schem = '%sscheme' % tmp
boot_file = '%sboot' % tmp

zfs_dsk_list = []


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
    def save_selection(self):
        SIZE = int(zfs_dsk_list[0].partition('-')[2].rstrip()) - 2
        SWAP = int(self.swap_entry.get_text())
        ZFS_NUM = SIZE - SWAP
        if self.disk_encript is True:
            dgeli = '.eli '
        else:
            dgeli = ' '
        if self.swap_encrypt is True:
            sgeli = '.eli '
        else:
            sgeli = ' '
        pfile = open(Part_label, 'w')
        if self.zpool is True:
            pfile.writelines("zpoolName=%s\n" % self.pool.get_text())
        else:
            pfile.writelines("#zpoolName=None\n")
        if self.zfs_four_k is True:
            pfile.writelines('zfsForce4k=YES\n\n')
        else:
            pfile.writelines('#zfsForce4k=No\n\n')
        pfile.writelines('disk0=%s\n' % zfs_dsk_list[0].partition('-')[0].rstrip())
        pfile.writelines('partition=ALL\n')
        pfile.writelines('partscheme=%s\n' % self.scheme)
        pfile.writelines('commitDiskPart\n\n')
        if self.mirror == 'none':
            pool_type = '\n'
        else:
            ZFS_disk = zfs_dsk_list
            disk_len = len(ZFS_disk) - 1
            num = 1
            while disk_len != 0:
                mirror_dsk = ' ' + ZFS_disk[num].partition('-')[0].rstrip()
                num += 1
                disk_len -= 1
            pool_type = ' (%s:%s)\n' % (self.mirror, mirror_dsk)
        read = open(boot_file, 'r')
        line = read.readlines()
        boot = line[0].strip()
        if bios_or_uefi() == "UEFI":
            ZFS_NUM = ZFS_NUM - 100
        elif boot == 'GRUB':
            ZFS_NUM = ZFS_NUM - 1
        else:
            ZFS_NUM = ZFS_NUM - 1
        pfile.writelines('disk0-part=ZFS%s%s /, /usr, /var%s' % (dgeli, ZFS_NUM, pool_type))
        if SWAP != 0: 
            pfile.writelines('disk0-part=SWAP%s%s none\n' % (sgeli, SWAP))
        if self.disk_encript is True:
            pfile.writelines('encpass=%s\n' % self.password.get_text())
        else:
            pfile.writelines('#encpass=None\n')
        pfile.writelines('commitDiskLabel\n')
        pfile.close()

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
        if self.mirror == "none":
            self.mirrorTips.set_text("Please select one drive")
            if len(zfs_dsk_list) != 1:
                self.button3.set_sensitive(False)
            else:
                self.button3.set_sensitive(True)
        elif self.mirror == "mirror":
            self.mirrorTips.set_text("Please select at less 2 drive for mirroring")
            if len(zfs_dsk_list) > 1:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)
        elif self.mirror == "raidz1":
            self.mirrorTips.set_text("Please select 3 or 5 drive for raidz1")
            if len(zfs_dsk_list) == 3 or len(zfs_dsk_list) == 5:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)
        elif self.mirror == "raidz2":
            self.mirrorTips.set_text("Please select 4, 6, or 10 drive for raidz2")
            if len(zfs_dsk_list) == 4 or len(zfs_dsk_list) == 6 or len(zfs_dsk_list) == 10:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)
        elif self.mirror == "raidz3":
            self.mirrorTips.set_text("Please select 5, 7, or 11 drive for raidz3")
            if len(zfs_dsk_list) == 5 or len(zfs_dsk_list) == 7 or len(zfs_dsk_list) == 11:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)
        elif self.mirror == "strip":
            self.mirrorTips.set_text("Please select 3 drive to strip")
            if len(zfs_dsk_list) > 2:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)



    def on_check_poll(self, widget):
        if widget.get_active():
            self.pool.set_sensitive(True)
            self.zpool = True
        else:
            self.pool.set_sensitive(False)
            self.zpool = False

    def on_check(self, widget):
        if widget.get_active():
            self.zfs_four_k = True
        else:
            self.zfs_four_k = False

    def on_check_encrypt(self, widget):
        if widget.get_active():
            self.password.set_sensitive(True)
            self.repassword.set_sensitive(True)
            self.disk_encript = True
            #self.swap_encrypt_check.set_active(True)
            self.button3.set_sensitive(False)
        else:
            self.password.set_sensitive(False)
            self.repassword.set_sensitive(False)
            self.disk_encript = False
            #self.swap_encrypt_check.set_active(False)
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
                if len(zfs_dsk_list) == 3 or len(zfs_dsk_list) == 5:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "raidz2":
                if len(zfs_dsk_list) == 4 or len(zfs_dsk_list) == 6 or len(zfs_dsk_list) == 10:
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
                    self.button3.set_sensitive(False)

    def on_check_swap_encrypt(self, widget):
        if widget.get_active():
            self.swap_encrypt = True
        else:
            self.swap_encrypt = False

    def on_check_swap_mirror(self, widget):
        if widget.get_active():
            self.swap_mirror = True
        else:
            self.swap_mirror = False

    def __init__(self, button3):
        self.button3 = button3
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.HBox(False, 0)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()
        # Title
        Title = Gtk.Label("<b><span size='xx-large'>ZFS Configuration</span></b>")
        Title.set_use_markup(True)
        # Chose disk
        sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        store = Gtk.TreeStore(str, str, str,'gboolean')
        for disk in zfs_disk_query():
            dsk = disk.partition(':')[0].rstrip()
            dsk_name = disk.partition(':')[2].rstrip()
            dsk_size = zfs_disk_size_query(dsk).rstrip()
            store.append(None, [dsk, dsk_size, dsk_name, False])
        treeView = Gtk.TreeView(store)
        treeView.set_model(store)
        treeView.set_rules_hint(True)
        self.check_cell = Gtk.CellRendererToggle()
        self.check_cell.set_property('activatable', True)
        self.check_cell.connect('toggled', self.col1_toggled_cb, store)
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
        column_header3 = Gtk.Label('Name')
        column_header3.set_use_markup(True)
        column_header3.show()
        column3.set_widget(column_header3)
        column1 = Gtk.TreeViewColumn("Check", self.check_cell)
        column1.add_attribute(self.check_cell, "active", 3)
        column.set_attributes(cell, text=0)
        column2.set_attributes(cell2, text=1)
        column3.set_attributes(cell3, text=2)
        treeView.append_column(column1)
        treeView.append_column(column)
        treeView.append_column(column2)
        treeView.append_column(column3)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        sw.add(treeView)
        sw.show()
        self.mirrorTips = Gtk.Label('Please select one drive')
        self.mirrorTips.set_justify(Gtk.Justification.LEFT)
        self.mirrorTips.set_alignment(0.01, 0.5)
        # Mirro, raidz and strip
        self.mirror = 'none'
        mirror_label = Gtk.Label('<b>Pool Type</b>')
        mirror_label.set_use_markup(True)
        mirror_box = Gtk.ComboBoxText()
        mirror_box.append_text("none")
        mirror_box.append_text("mirror")
        mirror_box.append_text("raidz1")
        mirror_box.append_text("raidz2")
        mirror_box.append_text("raidz3")
        mirror_box.append_text("strip")
        mirror_box.connect('changed', self.mirror_selection)
        mirror_box.set_active(0)

        # Pool Name
        self.zpool = False
        pool_check = Gtk.CheckButton('Pool Name')
        pool_check.connect("toggled", self.on_check_poll)
        self.pool = Gtk.Entry()
        self.pool.set_text('zroot')
        self.pool.set_sensitive(False)
        # Creating MBR or GPT drive
        label = Gtk.Label('<b>Partition Scheme</b>')
        label.set_use_markup(True)
        # Adding a combo box to selecting MBR or GPT sheme.
        self.scheme = 'GPT'
        shemebox = Gtk.ComboBoxText()
        shemebox.append_text("GPT")
        shemebox.append_text("MBR")
        shemebox.connect('changed', self.sheme_selection)
        shemebox.set_active(0)
        # Force 4k Sectors
        self.zfs_four_k = "False"
        check = Gtk.CheckButton("Force ZFS 4k block size")
        check.connect("toggled", self.on_check)
        # Swap Size
        ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
        close_fds=True)
        mem = ram.stdout.read()
        swap = int(mem.partition(':')[2].strip()) / (1024 * 1024)
        swp_size_label = Gtk.Label('<b>Swap Size(MB)</b>')
        swp_size_label.set_use_markup(True)
        self.swap_entry = Gtk.Entry()
        self.swap_entry.set_text(str(swap))
        self.swap_entry.connect('changed', self.digit_only)
        # Swap encription
        self.swap_encrypt = False
        self.swap_encrypt_check = Gtk.CheckButton("Encrypt Swap")
        self.swap_encrypt_check.connect("toggled", self.on_check_swap_encrypt)
        # Swap mirror
        self.swap_mirror = False
        swap_mirror_check = Gtk.CheckButton("Mirror Swap")
        swap_mirror_check.connect("toggled", self.on_check_swap_mirror)
        # GELI Disk encription
        self.disk_encript = False
        encrypt_check = Gtk.CheckButton("Encrypt Disk")
        encrypt_check.connect("toggled", self.on_check_encrypt)
        # password
        self.passwd_label = Gtk.Label("Password")
        self.password = Gtk.Entry()
        self.password.set_sensitive(False)
        self.password.set_visibility(False)
        self.password.connect("changed", self.passwdstrength)
        self.strenght_label = Gtk.Label()
        self.strenght_label.set_alignment(0.1, 0.5)
        self.vpasswd_label = Gtk.Label("Verify it")
        self.repassword = Gtk.Entry()
        self.repassword.set_sensitive(False)
        self.repassword.set_visibility(False)
        self.repassword.connect("changed", self.passwdVerification)
        # set image for password matching
        self.img = Gtk.Image()
        self.img.set_alignment(0.2, 0.5)
        #table = Gtk.Table(12, 12, True)
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        # grid.set_column_homogeneous(True)
        # grid.set_row_homogeneous(True)
        grid.attach(Title, 1, 0, 8, 2)
        grid.attach(mirror_label, 1, 2, 1, 1)
        grid.attach(mirror_box, 2, 2, 1, 1)
        grid.attach(label, 6, 2, 2, 1)
        grid.attach(shemebox, 8, 2, 1, 1)
        grid.attach(self.mirrorTips, 1, 3, 8, 1)
        grid.attach(sw, 1, 4, 8, 3)
        grid.attach(pool_check, 5, 8, 2, 1)
        grid.attach(self.pool, 7, 8, 2, 1)
        grid.attach(check, 1, 8, 3, 1)
        grid.attach(swp_size_label, 5, 9, 2, 1)
        grid.attach(self.swap_entry, 7, 9, 2, 1)
        #grid.attach(self.swap_encrypt_check, 9, 15, 11, 12)
        #grid.attach(swap_mirror_check, 9, 15, 11, 12)
        grid.attach(encrypt_check, 1, 9, 2, 1)
        grid.attach(self.passwd_label, 1, 10, 1, 1)
        grid.attach(self.password, 2, 10, 2, 1)
        grid.attach(self.strenght_label, 4, 10, 2, 1)
        grid.attach(self.vpasswd_label, 1, 11, 1, 1)
        grid.attach(self.repassword, 2, 11, 2, 1)
        grid.attach(self.img, 4, 11, 2, 1)
        box2.pack_start(grid, True, True, 10)
        return

    def get_model(self):
        return self.box1

    def digit_only(self, *args):
        text = self.swap_entry.get_text().strip()
        self.swap_entry.set_text(''.join([i for i in text if i in '0123456789']))

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
                    self.button3.set_sensitive(False)
        else:
            zfs_dsk_list.extend([model[path][0] + "-" + model[path][1]])
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
                if len(zfs_dsk_list) == 3 or len(zfs_dsk_list) == 5:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "raidz2":
                if len(zfs_dsk_list) == 4 or len(zfs_dsk_list) == 6 or len(zfs_dsk_list) == 10:
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
                    self.button3.set_sensitive(False)
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
            self.img.set_from_stock(Gtk.STOCK_YES, 10)
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
                if len(zfs_dsk_list) == 3 or len(zfs_dsk_list) == 5:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "raidz2":
                if len(zfs_dsk_list) == 4 or len(zfs_dsk_list) == 6 or len(zfs_dsk_list) == 10:
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
                    self.button3.set_sensitive(False)
        else:
            self.img.set_from_stock(Gtk.STOCK_NO, 10)
            self.button3.set_sensitive(False)
