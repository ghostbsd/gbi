#!/usr/bin/env python

from gi.repository import Gtk, Gdk
import os
from gbi_common import (
    zfs_datasets, be_name,
    lowerCase, upperCase, lowerandNunber, upperandNunber,
    lowerUpperCase, lowerUpperNumber, allCharacter
)
from partition_handler import (
    zfs_disk_query,
    zfs_disk_size_query,
    bios_or_uefi
)


# Folder use pr the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
logo = f"{installer}image/logo.png"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)

disk_info = f'{query}disk-info.sh'
disk_file = f'{tmp}disk'
dslice = f'{tmp}slice'
Part_label = f'{tmp}zfs_config'
part_schem = f'{tmp}scheme'
boot_file = f'{tmp}boot'

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class ZFS:
    zfs_disk_list = []

    def save_selection(self):
        size = int(self.zfs_disk_list[0].partition('-')[2].rstrip()) - 512
        swap_size = int(self.swap_entry.get_text())
        ZFS_NUM = size - swap_size
        dgeli = '.eli' if self.disk_encript is True else ''
        pfile = open(Part_label, 'w')
        pfile.writelines(f'zpoolName={self.pool.get_text()}\n')
        pfile.writelines(f"beName={be_name}\n")
        if self.zfs_four_k is True:
            pfile.writelines('ashift=12\n\n')
        else:
            pfile.writelines('ashift=9\n\n')
        disk = self.zfs_disk_list[0].partition('-')[0].rstrip()
        pfile.writelines(f'disk0={disk}\n')
        pfile.writelines('partition=ALL\n')
        pfile.writelines(f'partscheme={self.scheme}\n')
        pfile.writelines('commitDiskPart\n\n')
        if len(self.zfs_disk_list) <= 1:
            pool_disk = '\n'
        else:
            zfs_disk = self.zfs_disk_list
            mirror_dsk = ''
            for i in range(1, len(zfs_disk)):
                mirror_dsk += ' ' + zfs_disk[i].partition('-')[0].rstrip()
            pool_disk = f' ({self.poolType}:{mirror_dsk})\n'
        final_space = ZFS_NUM - 100 if bios_or_uefi() == "UEFI" else ZFS_NUM - 1
        # adding zero to use remaining space
        zfs_part = f'disk0-part=ZFS{dgeli} {final_space} {zfs_datasets}{pool_disk}'
        pfile.writelines(zfs_part)
        # encpass= must be on the line immediately after the .eli partition
        if self.disk_encript:
            pfile.writelines(f'encpass={self.password.get_text()}\n')
        else:
            pfile.writelines('#encpass=None\n')
        if swap_size != 0:
            if self.disk_encript:
                pfile.writelines('disk0-part=SWAP.eli 0 none\n')
            else:
                pfile.writelines('disk0-part=SWAP 0 none\n')
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
        smallest_msg = "(select the smallest disk first)"
        data = model[index][0]
        self.mirror = data
        if self.mirror == "stripe":
            self.poolType = 'stripe'
            self.mirrorTips.set_text(
                f"Select 1 or more drives, no redundancy {smallest_msg}")
            valid = len(self.zfs_disk_list) >= 1
        elif self.mirror == "mirror":
            self.poolType = 'mirror'
            self.mirrorTips.set_text(
                f"Select 2 or more drives for mirroring {smallest_msg}")
            valid = len(self.zfs_disk_list) >= 2
        elif self.mirror == "raidz1":
            self.poolType = 'raidz1'
            self.mirrorTips.set_text(
                f"Select 3 drives for raidz1 {smallest_msg}")
            valid = len(self.zfs_disk_list) == 3
        elif self.mirror == "raidz2":
            self.poolType = 'raidz2'
            self.mirrorTips.set_text(
                f"Select 4 drives for raidz2 {smallest_msg}")
            valid = len(self.zfs_disk_list) == 4
        elif self.mirror == "raidz3":
            self.poolType = 'raidz3'
            self.mirrorTips.set_text(
                f"Select 5 drives for raidz3 {smallest_msg}")
            valid = len(self.zfs_disk_list) == 5
        else:
            valid = False
        self.button3.set_sensitive(valid)

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
            self.button3.set_sensitive(False)
        else:
            self.password.set_sensitive(False)
            self.repassword.set_sensitive(False)
            self.disk_encript = False
            if self.mirror == "stripe":
                self.button3.set_sensitive(len(self.zfs_disk_list) >= 1)
            elif self.mirror == "mirror":
                self.button3.set_sensitive(len(self.zfs_disk_list) >= 2)
            elif self.mirror == "raidz1":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 3)
            elif self.mirror == "raidz2":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 4)
            elif self.mirror == "raidz3":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 5)

    def __init__(self, button3):
        self.button3 = button3
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        # Title
        Title = Gtk.Label(label="ZFS Configuration", name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        # Chose disk
        sw = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.store = Gtk.TreeStore(str, str, str, 'gboolean')
        for disk in zfs_disk_query():
            dsk = disk.partition(':')[0].rstrip()
            if dsk.startswith("da"):
                continue
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
        column_header = Gtk.Label(label='Disk')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        cell2 = Gtk.CellRendererText()
        column2 = Gtk.TreeViewColumn(None, cell2, text=0)
        column_header2 = Gtk.Label(label='Size(MB)')
        column_header2.set_use_markup(True)
        column_header2.show()
        column2.set_widget(column_header2)
        cell3 = Gtk.CellRendererText()
        column3 = Gtk.TreeViewColumn(None, cell3, text=0)
        column_header3 = Gtk.Label(label='Name')
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
        sw.add(treeView)
        sw.show()
        self.mirrorTips = Gtk.Label(label='Please select one drive')
        self.mirrorTips.set_justify(Gtk.Justification.LEFT)
        self.mirrorTips.set_alignment(0.01, 0.5)
        # Mirror, raidz and stripe
        self.mirror = 'none'
        mirror_label = Gtk.Label(label='Pool Layout')
        mirror_label.set_use_markup(True)
        mirror_box = Gtk.ComboBoxText()
        mirror_box.append_text("stripe")
        mirror_box.append_text("mirror")
        mirror_box.append_text("raidz1")
        mirror_box.append_text("raidz2")
        mirror_box.append_text("raidz3")
        mirror_box.connect('changed', self.mirror_selection)
        mirror_box.set_active(0)

        # Pool Name
        pool_label = Gtk.Label(label='Pool Name')
        pool_label.set_use_markup(True)
        self.pool = Gtk.Entry()
        self.pool.set_text('zroot')
        # Creating MBR or GPT drive
        scheme_label = Gtk.Label(label='Partition Scheme')
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
        self.zfs_four_k = True
        zfs4kcheck = Gtk.CheckButton(label="Force ZFS 4k block size")
        zfs4kcheck.connect("toggled", self.on_check)
        zfs4kcheck.set_active(True)
        # Swap Size
        swap = 2048
        swp_size_label = Gtk.Label(label='Swap Size(MB)')
        swp_size_label.set_use_markup(True)
        self.swap_entry = Gtk.Entry()
        self.swap_entry.set_text(str(swap))
        self.swap_entry.connect('changed', self.digit_only)
        # GELI Disk encryption
        self.disk_encript = False
        encrypt_check = Gtk.CheckButton(label="Encrypt Disk (GELI)")
        encrypt_check.connect("toggled", self.on_check_encrypt)
        encrypt_check.set_sensitive(True)
        # password
        self.passwd_label = Gtk.Label(label="Password")
        self.password = Gtk.Entry()
        self.password.set_sensitive(False)
        self.password.set_visibility(False)
        self.password.connect("changed", self.passwdstrength)
        self.strenght_label = Gtk.Label()
        self.strenght_label.set_alignment(0.1, 0.5)
        self.vpasswd_label = Gtk.Label(label="Confirm")
        self.repassword = Gtk.Entry()
        self.repassword.set_sensitive(False)
        self.repassword.set_visibility(False)
        self.repassword.connect("changed", self.passwdVerification)
        # set image for password matching
        self.img = Gtk.Image()
        self.img.set_size_request(20, 20)

        # Two-column layout: left settings grid, right disk list
        hbox_main = Gtk.HBox(False, 10)

        # Left panel: settings in a grid
        left_grid = Gtk.Grid()
        left_grid.set_row_spacing(4)
        left_grid.set_column_spacing(6)
        left_grid.set_size_request(200, -1)

        mirror_label.set_alignment(0, 0.5)
        pool_label.set_alignment(0, 0.5)
        swp_size_label.set_alignment(0, 0.5)
        self.passwd_label.set_alignment(0, 0.5)
        self.vpasswd_label.set_alignment(0, 0.5)
        self.strenght_label.set_size_request(-1, 20)

        # Row 0: Pool Layout
        left_grid.attach(mirror_label, 0, 0, 2, 1)
        left_grid.attach(mirror_box, 0, 1, 2, 1)
        # Row 2: Pool Name
        left_grid.attach(pool_label, 0, 2, 2, 1)
        left_grid.attach(self.pool, 0, 3, 2, 1)
        # Row 4: Swap Size
        left_grid.attach(swp_size_label, 0, 4, 2, 1)
        left_grid.attach(self.swap_entry, 0, 5, 2, 1)
        # Row 6: Force 4k
        left_grid.attach(zfs4kcheck, 0, 6, 2, 1)
        # Row 7: Separator
        sep = Gtk.HSeparator()
        left_grid.attach(sep, 0, 7, 2, 1)
        # Row 8: Encrypt Disk
        left_grid.attach(encrypt_check, 0, 8, 2, 1)
        # Row 9: Password label + strength
        left_grid.attach(self.passwd_label, 0, 9, 1, 1)
        left_grid.attach(self.strenght_label, 1, 9, 1, 1)
        # Row 10: Password input
        left_grid.attach(self.password, 0, 10, 2, 1)
        # Row 11: Verify label + icon
        left_grid.attach(self.vpasswd_label, 0, 11, 1, 1)
        left_grid.attach(self.img, 1, 11, 1, 1)
        # Row 12: Verify input
        left_grid.attach(self.repassword, 0, 12, 2, 1)

        hbox_main.pack_start(left_grid, False, False, 10)

        # Right panel: disk list
        right_panel = Gtk.VBox(False, 0)
        self.mirrorTips.set_alignment(0, 0.5)
        right_panel.pack_start(self.mirrorTips, False, False, 0)
        right_panel.pack_start(sw, True, True, 0)

        hbox_main.pack_start(right_panel, True, True, 10)

        self.vbox1.pack_start(hbox_main, True, True, 10)
        return

    def get_model(self):
        return self.vbox1

    def digit_only(self, *args):
        text = self.swap_entry.get_text().strip()
        digit = ''.join([i for i in text if i in '0123456789'])
        self.swap_entry.set_text(digit)

    def check_if_small_disk(self, size):
        if len(self.zfs_disk_list) != 0:
            for line in self.zfs_disk_list:
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
            self.zfs_disk_list.remove(model[path][0] + "-" + model[path][1])
            if self.mirror == "stripe":
                self.button3.set_sensitive(len(self.zfs_disk_list) >= 1)
            elif self.mirror == "mirror":
                self.button3.set_sensitive(len(self.zfs_disk_list) >= 2)
            elif self.mirror == "raidz1":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 3)
            elif self.mirror == "raidz2":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 4)
            elif self.mirror == "raidz3":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 5)
        else:
            if self.check_if_small_disk(model[path][1]) is False:
                self.zfs_disk_list.extend([model[path][0] + "-" + model[path][1]])
                if self.mirror == "stripe":
                    self.button3.set_sensitive(len(self.zfs_disk_list) >= 1)
                elif self.mirror == "mirror":
                    self.button3.set_sensitive(len(self.zfs_disk_list) >= 2)
                elif self.mirror == "raidz1":
                    self.button3.set_sensitive(len(self.zfs_disk_list) == 3)
                elif self.mirror == "raidz2":
                    self.button3.set_sensitive(len(self.zfs_disk_list) == 4)
                elif self.mirror == "raidz3":
                    self.button3.set_sensitive(len(self.zfs_disk_list) == 5)
            else:
                self.check_cell.set_sensitive(False)
                self.small_disk_warning()

        print(self.zfs_disk_list)
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
        label = Gtk.Label(label=warning_text)
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

    def resset_selection(self, _widget, window):
        self.zfs_disk_list = []
        rows = len(self.store)
        for row in range(rows):
            self.store[row][3] = False
        self.check_cell.set_sensitive(True)
        window.hide()

    def passwdstrength(self, _widget):
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

    def passwdVerification(self, _widget):
        if self.password.get_text() == self.repassword.get_text():
            self.img.set_from_icon_name("gtk-yes", Gtk.IconSize.MENU)
            if self.mirror == "stripe":
                self.button3.set_sensitive(len(self.zfs_disk_list) >= 1)
            elif self.mirror == "mirror":
                self.button3.set_sensitive(len(self.zfs_disk_list) >= 2)
            elif self.mirror == "raidz1":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 3)
            elif self.mirror == "raidz2":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 4)
            elif self.mirror == "raidz3":
                self.button3.set_sensitive(len(self.zfs_disk_list) == 5)
        else:
            self.img.set_from_icon_name("gtk-no", Gtk.IconSize.MENU)
            self.button3.set_sensitive(False)
