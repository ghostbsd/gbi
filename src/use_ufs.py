#!/usr/bin/env python

from gi.repository import Gtk, Gdk
import os
import os.path
import re
from partition_handler import zfs_disk_query, zfs_disk_size_query, bios_or_uefi

# Folder use pr the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)


memory = 'sysctl hw.physmem'
auto = '%sauto' % tmp
disk_info = '%sdisk-info.sh' % query
disk_file = '%sdisk' % tmp
dslice = '%sslice' % tmp
Part_label = '%sufs_config' % tmp
part_schem = '%sscheme' % tmp
boot_file = '%sboot' % tmp
ufs_dsk_list = []

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


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


# Find if password contain only lowercase, uppercase numbers and some
# special character.
def allCharacter(strg):
    search = re.compile(r'[^a-zA-Z0-9~\!@#\$%\^&\*_\+":;\'\-]').search
    return not bool(search(strg))


class use_ufs():
    def save_selection(self):
        disk_size = int(ufs_dsk_list[0].partition('-')[2].rstrip()) - 512
        swap_size = int(self.swap_entry.get_text())
        root_size = disk_size - swap_size
        if self.disk_encript is True:
            dgeli = '.eli'
        else:
            dgeli = ''
        pfile = open(Part_label, 'w')
        disk = ufs_dsk_list[0].partition('-')[0].rstrip()
        pfile.writelines(f'disk0={disk}\n')
        if self.mirror is True:
            ufs_disk = ufs_dsk_list
            disk_len = len(ufs_disk) - 1
            num = 1
            mirror_dsk = ''
            while disk_len != 0:
                mirror_dsk += ufs_disk[num].partition('-')[0].rstrip() + " "
                print(mirror_dsk)
                num += 1
                disk_len -= 1
            pfile.writelines("mirror=%s\n" % mirror_dsk)
            pfile.writelines("mirrorlab=%s\n" % self.mirrorbl)
        else:
            pfile.writelines("#mirror=\n")
            pfile.writelines("#mirrorlab=\n")
        pfile.writelines('partition=ALL\n')
        pfile.writelines('partscheme=%s\n' % self.scheme)
        pfile.writelines('commitDiskPart\n\n')
        if bios_or_uefi() == "UEFI":
            root_size = root_size - 100
        else:
            root_size = root_size - 1
        # adding zero to use remaining space
        zfsPart = f'disk0-part={self.fs}{dgeli} {root_size} /\n'
        pfile.writelines(zfsPart)
        if swap_size != 0:
            pfile.writelines('disk0-part=SWAP 0 none\n')
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
        self.scheme = data

    def mirror_selection(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        data = model[index][0]
        self.mirrorbl = data

    def on_check_mirror(self, widget):
        if widget.get_active():
            self.mirrorbl_box.set_sensitive(True)
            self.mirror = True
        else:
            self.mirrorbl_box.set_sensitive(False)
            self.mirror = False
        if self.mirror is False:
            self.mirrorTips.set_text("Please select one drive")
            if len(ufs_dsk_list) != 1:
                self.button3.set_sensitive(False)
            else:
                self.button3.set_sensitive(True)
        elif self.mirror is True:
            self.mirrorTips.set_text("Please select 2 drive for mirroring")
            if len(ufs_dsk_list) > 1:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)

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
            # self.swap_encrypt_check.set_active(True)
            self.button3.set_sensitive(False)
        else:
            self.password.set_sensitive(False)
            self.repassword.set_sensitive(False)
            self.disk_encript = False
            # self.swap_encrypt_check.set_active(False)
            if self.mirror is False:
                if len(ufs_dsk_list) != 1:
                    self.button3.set_sensitive(False)
                else:
                    self.button3.set_sensitive(True)
            elif self.mirror is True:
                if len(ufs_dsk_list) > 1:
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

    def chosefs(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        data = model[index][0]
        self.fs = data

    def __init__(self, button3):
        self.button3 = button3
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        # Title
        Title = Gtk.Label("UFS Full Disk Configuration", name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        # Chose disk
        sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        store = Gtk.TreeStore(str, str, str, 'gboolean')
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
        self.mirror = False
        mirror_check = Gtk.CheckButton('Disk Mirror')
        mirror_check.connect("toggled", self.on_check_mirror)
        self.mirrorbl_box = Gtk.ComboBoxText()
        self.mirrorbl_box.append_text("load")
        self.mirrorbl_box.append_text("prefer")
        self.mirrorbl_box.append_text("round-robin")
        self.mirrorbl_box.append_text("split")
        self.mirrorbl_box.connect('changed', self.mirror_selection)
        self.mirrorbl_box.set_active(0)
        self.mirrorbl_box.set_sensitive(False)
        self.mirrorbl = 'load'
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
        if bios_or_uefi() == "UEFI":
            shemebox.set_sensitive(False)
        else:
            shemebox.set_sensitive(True)
        # Swap Size
        # ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
        #             stderr=STDOUT, universal_newlines=True, close_fds=True)
        # mem = ram.stdout.read()
        swap = 2048
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
        encrypt_check.set_sensitive(True)
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
        fslabel = Gtk.Label("File System:")
        self.fstype = Gtk.ComboBoxText()
        self.fstype.append_text('UFS')
        self.fstype.append_text('UFS+S')
        self.fstype.append_text('UFS+J')
        self.fstype.append_text('UFS+SUJ')
        self.fstype.set_active(3)
        self.fstype.connect("changed", self.chosefs)
        self.fs = "UFS+SUJ"
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        # grid.set_column_homogeneous(True)
        # grid.set_row_homogeneous(True)
        grid.attach(Title, 0, 0, 9, 2)
        grid.attach(mirror_check, 0, 2, 1, 1)
        grid.attach(self.mirrorbl_box, 1, 2, 1, 1)
        grid.attach(label, 0, 9, 2, 1)
        grid.attach(shemebox, 2, 9, 1, 1)
        grid.attach(self.mirrorTips, 1, 3, 8, 1)
        grid.attach(sw, 0, 4, 9, 4)
        grid.attach(fslabel, 5, 9, 2, 1)
        grid.attach(self.fstype, 7, 9, 1, 1)
        grid.attach(swp_size_label, 5, 2, 2, 1)
        grid.attach(self.swap_entry, 7, 2, 1, 1)
        # grid.attach(self.swap_encrypt_check, 9, 15, 11, 12)
        # grid.attach(swap_mirror_check, 9, 15, 11, 12)
        # grid.attach(encrypt_check, 1, 9, 2, 1)
        # grid.attach(self.passwd_label, 1, 10, 1, 1)
        # grid.attach(self.password, 2, 10, 2, 1)
        # grid.attach(self.strenght_label, 4, 10, 2, 1)
        # grid.attach(self.vpasswd_label, 1, 11, 1, 1)
        # grid.attach(self.repassword, 2, 11, 2, 1)
        # grid.attach(self.img, 4, 11, 2, 1)
        self.vbox1.pack_start(grid, True, True, 10)
        return

    def get_model(self):
        del ufs_dsk_list[:]
        return self.vbox1

    def digit_only(self, *args):
        text = self.swap_entry.get_text().strip()
        digit = ''.join([i for i in text if i in '0123456789'])
        self.swap_entry.set_text(digit)

    def col1_toggled_cb(self, cell, path, model):
        model[path][3] = not model[path][3]
        if model[path][3] is False:
            ufs_dsk_list.remove(model[path][0] + "-" + model[path][1])
            if self.mirror is False:
                if len(ufs_dsk_list) != 1:
                    self.button3.set_sensitive(False)
                else:
                    self.button3.set_sensitive(True)
            elif self.mirror is True:
                if len(ufs_dsk_list) > 1:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
        else:
            ufs_dsk_list.extend([model[path][0] + "-" + model[path][1]])
            if self.mirror is False:
                if len(ufs_dsk_list) != 1:
                    self.button3.set_sensitive(False)
                else:
                    self.button3.set_sensitive(True)
            elif self.mirror is True:
                if len(ufs_dsk_list) > 1:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
        print(ufs_dsk_list)
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
            self.img.set_from_stock(Gtk.STOCK_YES, 5)
            if self.mirror == "none":
                if len(ufs_dsk_list) != 1:
                    self.button3.set_sensitive(False)
                else:
                    self.button3.set_sensitive(True)
            elif self.mirror == "mirror":
                if len(ufs_dsk_list) > 1:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
        else:
            self.img.set_from_stock(Gtk.STOCK_NO, 5)
            self.button3.set_sensitive(False)
