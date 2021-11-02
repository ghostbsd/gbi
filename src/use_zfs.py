#!/usr/bin/env python

from gi.repository import Gtk, Gdk
import os
import os.path
import re
from partition_handler import zfs_disk_query, zfs_disk_size_query, bios_or_uefi

# Folder use pr the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
logo = f"{installer}image/logo.png"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

memory = 'sysctl hw.physmem'
auto = '%sauto' % tmp
disk_info = '%sdisk-info.sh' % query
disk_file = '%sdisk' % tmp
dslice = '%sslice' % tmp
Part_label = '%szfs_config' % tmp
part_schem = '%sscheme' % tmp
boot_file = '%sboot' % tmp

global zfs_dsk_list
zfs_dsk_list = []

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


# Find if pasword contain only lowercase, uppercase numbers
# and some special character.
def allCharacter(strg):
    search = re.compile(r'[^a-zA-Z0-9~\!@#\$%\^&\*_\+":;\'\-]').search
    return not bool(search(strg))


class ZFS():
    def save_selection(self):
        SIZE = int(zfs_dsk_list[0].partition('-')[2].rstrip()) - 512
        SWAP = int(self.swap_entry.get_text())
        ZFS_NUM = SIZE - SWAP
        if self.disk_encript is True:
            dgeli = '.eli'
        else:
            dgeli = ''
        pfile = open(Part_label, 'w')
        if self.zpool is True:
            pfile.writelines("zpoolName=%s\n" % self.pool.get_text())
        else:
            pfile.writelines("#zpoolName=None\n")
        if self.zfs_four_k is True:
            pfile.writelines('ashift=12\n\n')
        else:
            pfile.writelines('ashift=9\n\n')
        disk = zfs_dsk_list[0].partition('-')[0].rstrip()
        pfile.writelines(f'disk0={disk}\n')
        pfile.writelines('partition=ALL\n')
        pfile.writelines('partscheme=%s\n' % self.scheme)
        pfile.writelines('commitDiskPart\n\n')
        if self.poolType == 'none':
            pool_disk = '\n'
        else:
            ZFS_disk = zfs_dsk_list
            disk_len = len(ZFS_disk) - 1
            num = 1
            mirror_dsk = ''
            while disk_len != 0:
                mirror_dsk += ' ' + ZFS_disk[num].partition('-')[0].rstrip()
                print(mirror_dsk)
                num += 1
                disk_len -= 1
            pool_disk = ' (%s:%s)\n' % (self.poolType, mirror_dsk)
        if bios_or_uefi() == "UEFI":
            ZFS_NUM = ZFS_NUM - 100
        else:
            ZFS_NUM = ZFS_NUM - 1
        zfslayout = "/," \
            "/tmp(mountpoint=/tmp|exec=on|setuid=off)," \
            "/usr(mountpoint=/usr|canmount=off)," \
            "/usr/home," \
            "/usr/ports(setuid=off)," \
            "/usr/src," \
            "/var(mountpoint=/var|canmount=off)," \
            "/var/audit(exec=off|setuid=off)," \
            "/var/crash(exec=off|setuid=off)" \
            "/var/log(exec=off|setuid=off)," \
            "/var/mail(atime=on)," \
            "/var/tmp(setuid=off)"
        # adding zero to use remaining space
        zfsPart = f'disk0-part=ZFS{dgeli} {ZFS_NUM} {zfslayout}{pool_disk}'
        pfile.writelines(zfsPart)
        if SWAP != 0:
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
        self.scheme = data.partition(':')[0]

    def mirror_selection(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        mirror_mesage = " (select the smallest disk first)"
        data = model[index][0]
        self.mirror = data
        if self.mirror == "single disk":
            self.poolType = 'none'
            self.mirrorTips.set_text("Please select one drive")
            if len(zfs_dsk_list) != 1:
                self.button3.set_sensitive(False)
            else:
                self.button3.set_sensitive(True)
        elif self.mirror == "2 disk mirror":
            self.poolType = 'mirror'
            mir_msg1 = f"Please select 2 drive for mirroring{mirror_mesage}"
            self.mirrorTips.set_text(mir_msg1)
            if len(zfs_dsk_list) == 2:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)
        elif self.mirror == "3 disk raidz1":
            self.poolType = 'raidz1'
            self.mirrorTips.set_text(f"Please select 3 drive for "
                                     f"raidz1{mirror_mesage}")
            if len(zfs_dsk_list) == 3:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)
        elif self.mirror == "4 disk raidz2":
            self.poolType = 'raidz2'
            self.mirrorTips.set_text(f"Please select 4 drive for "
                                     f"raidz2{mirror_mesage}")
            if len(zfs_dsk_list) == 4:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)
        elif self.mirror == "5 disk raidz3":
            self.poolType = 'raidz3'
            self.mirrorTips.set_text("Please select 5 drive for "
                                     f"raidz3{mirror_mesage}")
            if len(zfs_dsk_list) == 5:
                self.button3.set_sensitive(True)
            else:
                self.button3.set_sensitive(False)
        elif self.mirror == "2+ disk stripe":
            self.poolType = 'stripe'
            self.mirrorTips.set_text("Please select 2 or more drive for "
                                     f"stripe{mirror_mesage}")
            if len(zfs_dsk_list) >= 2:
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
            # self.swap_encrypt_check.set_active(True)
            self.button3.set_sensitive(False)
        else:
            self.password.set_sensitive(False)
            self.repassword.set_sensitive(False)
            self.disk_encript = False
            # self.swap_encrypt_check.set_active(False)
            if self.mirror == "single disk":
                if len(zfs_dsk_list) != 1:
                    self.button3.set_sensitive(False)
                else:
                    self.button3.set_sensitive(True)
            elif self.mirror == "2 disk mirror":
                if len(zfs_dsk_list) == 2:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "3 disk raidz1":
                if len(zfs_dsk_list) == 3:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "4 disk raidz2":
                if len(zfs_dsk_list) == 4:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "5 disk raidz3":
                if len(zfs_dsk_list) == 5:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "2+ disk  stripe":
                if len(zfs_dsk_list) >= 2:
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
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        # Title
        Title = Gtk.Label("ZFS Configuration", name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        # Chose disk
        sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.store = Gtk.TreeStore(str, str, str, 'gboolean')
        for disk in zfs_disk_query():
            dsk = disk.partition(':')[0].rstrip()
            dsk_name = disk.partition(':')[2].rstrip()
            dsk_size = zfs_disk_size_query(dsk).rstrip()
            self.store.append(None, [dsk, dsk_size, dsk_name, False])
        treeView = Gtk.TreeView(self.store)
        treeView.set_model(self.store)
        treeView.set_rules_hint(True)
        self.check_cell = Gtk.CellRendererToggle()
        self.check_cell.set_property('activatable', True)
        self.check_cell.connect('toggled', self.col1_toggled_cb, self.store)
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
        # Mirror, raidz and stripe
        self.mirror = 'none'
        mirror_label = Gtk.Label('<b>Pool Type</b>')
        mirror_label.set_use_markup(True)
        mirror_box = Gtk.ComboBoxText()
        mirror_box.append_text("single disk")
        mirror_box.append_text("2 disk mirror")
        mirror_box.append_text("3 disk raidz1")
        mirror_box.append_text("4 disk raidz2")
        mirror_box.append_text("5 disk raidz3")
        mirror_box.append_text("2+ disk stripe")
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
        scheme_label = Gtk.Label('<b>Partition Scheme</b>')
        scheme_label.set_use_markup(True)
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
        # Force 4k Sectors
        self.zfs_four_k = "True"
        zfs4kcheck = Gtk.CheckButton("Force ZFS 4k block size")
        zfs4kcheck.connect("toggled", self.on_check)
        zfs4kcheck.set_active(True)
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
        self.img = Gtk.Image()
        self.img.set_alignment(0.2, 0.5)
        # table = Gtk.Table(12, 12, True)
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        # grid.set_column_homogeneous(True)
        # grid.set_row_homogeneous(True)
        # grid.attach(Title, 1, 1, 10, 1)
        grid.attach(mirror_label, 1, 2, 1, 1)
        grid.attach(mirror_box, 2, 2, 1, 1)
        grid.attach(pool_check, 7, 2, 2, 1)
        grid.attach(self.pool, 9, 2, 2, 1)
        grid.attach(self.mirrorTips, 1, 3, 8, 1)
        grid.attach(zfs4kcheck, 9, 3, 2, 1)
        grid.attach(sw, 1, 4, 10, 3)
        # grid.attach(scheme_label, 1, 9, 1, 1)
        # grid.attach(shemebox, 2, 9, 1, 1)
        grid.attach(swp_size_label, 9, 9, 1, 1)
        grid.attach(self.swap_entry, 10, 9, 1, 1)
        # grid.attach(self.swap_encrypt_check, 9, 15, 11, 12)
        # grid.attach(swap_mirror_check, 9, 15, 11, 12)
        # grid.attach(encrypt_check, 2, 8, 2, 1)
        # grid.attach(self.passwd_label, 1, 9, 1, 1)
        # grid.attach(self.password, 2, 9, 2, 1)
        # grid.attach(self.strenght_label, 4, 9, 2, 1)
        # grid.attach(self.vpasswd_label, 1, 10, 1, 1)
        # grid.attach(self.repassword, 2, 10, 2, 1)
        # grid.attach(self.img, 4, 10, 2, 1)
        self.vbox1.pack_start(grid, True, True, 10)
        return

    def get_model(self):
        return self.vbox1

    def digit_only(self, *args):
        text = self.swap_entry.get_text().strip()
        digit = ''.join([i for i in text if i in '0123456789'])
        self.swap_entry.set_text(digit)

    def check_if_small_disk(self, size):
        if len(zfs_dsk_list) != 0:
            for line in zfs_dsk_list:
                if int(line.partition('-')[2]) > int(size):
                    returns = True
                    break
                else:
                    returns = False
        else:
            returns = False
        return returns

    def col1_toggled_cb(self, cell, path, model):
        model[path][3] = not model[path][3]
        if model[path][3] is False:
            zfs_dsk_list.remove(model[path][0] + "-" + model[path][1])
            if self.mirror == "single disk":
                if len(zfs_dsk_list) != 1:
                    self.button3.set_sensitive(False)
                else:
                    self.button3.set_sensitive(True)
            elif self.mirror == "2 disk mirror":
                if len(zfs_dsk_list) == 2:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "3 disk raidz1":
                if len(zfs_dsk_list) == 3:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "4 disk raidz2":
                if len(zfs_dsk_list) == 4:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "5 disk raidz3":
                if len(zfs_dsk_list) == 5:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "2+ disk stripe":
                if len(zfs_dsk_list) >= 2:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
        else:
            if self.check_if_small_disk(model[path][1]) is False:
                zfs_dsk_list.extend([model[path][0] + "-" + model[path][1]])
                if self.mirror == "single disk":
                    if len(zfs_dsk_list) != 1:
                        self.button3.set_sensitive(False)
                    else:
                        self.button3.set_sensitive(True)
                elif self.mirror == "2 disk mirror":
                    if len(zfs_dsk_list) == 2:
                        self.button3.set_sensitive(True)
                    else:
                        self.button3.set_sensitive(False)
                elif self.mirror == "3 disk raidz1":
                    if len(zfs_dsk_list) == 3:
                        self.button3.set_sensitive(True)
                    else:
                        self.button3.set_sensitive(False)
                elif self.mirror == "4 disk raidz2":
                    if len(zfs_dsk_list) == 4:
                        self.button3.set_sensitive(True)
                    else:
                        self.button3.set_sensitive(False)
                elif self.mirror == "5 disk raidz3":
                    if len(zfs_dsk_list) == 5:
                        self.button3.set_sensitive(True)
                    else:
                        self.button3.set_sensitive(False)
                elif self.mirror == "2+ disk stripe":
                    if len(zfs_dsk_list) >= 2:
                        self.button3.set_sensitive(True)
                    else:
                        self.button3.set_sensitive(False)
            else:
                self.check_cell.set_sensitive(False)
                self.small_disk_warning()

        print(zfs_dsk_list)
        return True

    def small_disk_warning(self):
        window = Gtk.Window()
        window.set_title("Warning")
        window.set_border_width(0)
        # window.set_size_request(480, 200)
        window.set_icon_from_file(logo)
        box1 = Gtk.VBox(False, 0)
        window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        warning_text = "Smallest disk need to be SELECTED first!\n"
        warning_text += "All the disk selected will reset."
        label = Gtk.Label(warning_text)
        # Add button
        box2.pack_start(label, True, True, 0)
        bbox = Gtk.HButtonBox()
        bbox.set_border_width(5)
        bbox.set_spacing(10)
        button = Gtk.Button(stock=Gtk.STOCK_OK)
        button.connect("clicked", self.resset_selection, window)
        bbox.add(button)
        box2.pack_end(bbox, True, True, 5)
        window.show_all()

    def resset_selection(self, widget, window):
        global zfs_dsk_list
        zfs_dsk_list = []
        rows = len(self.store)
        for row in range(0, rows):
            self.store[row][3] = False
            row += 1
        self.check_cell.set_sensitive(True)
        window.hide()

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
            if self.mirror == "single disk":
                if len(zfs_dsk_list) != 1:
                    self.button3.set_sensitive(False)
                else:
                    self.button3.set_sensitive(True)
            elif self.mirror == "2 disk mirror":
                if len(zfs_dsk_list) == 2:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "3 disk raidz1":
                if len(zfs_dsk_list) == 3:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "4 disk raidz2":
                if len(zfs_dsk_list) == 4:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "5 disk raidz3":
                if len(zfs_dsk_list) == 5:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
            elif self.mirror == "2+ disk stripe":
                if len(zfs_dsk_list) >= 2:
                    self.button3.set_sensitive(True)
                else:
                    self.button3.set_sensitive(False)
        else:
            self.img.set_from_stock(Gtk.STOCK_NO, 5)
            self.button3.set_sensitive(False)
