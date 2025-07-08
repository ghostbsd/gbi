#!/usr/bin/env python

import os
import pickle

# Directory use from the installer.
tmp = "/tmp/.gbi"
installer = "/usr/local/lib/gbi/"
# Installer data file.
disk = f'{tmp}/disk'
pcinstallcfg = f'{tmp}/pcinstall.cfg'
user_passwd = f'{tmp}/user_admin'
language = f'{tmp}/language'
dslice = f'{tmp}/slice'
left = f'{tmp}/left'
partlabel = f'{tmp}/partlabel'
timezone = f'{tmp}/timezone'
KBFile = f'{tmp}/keyboard'
boot_file = f'{tmp}/boot'
disk_scheme = f'{tmp}/scheme'
zfs_config = f'{tmp}/zfs_config'
ufs_config = f'{tmp}/ufs_config'


class GhostBSDCfg:
    def __init__(self):
        f = open(f'{tmp}/pcinstall.cfg', 'w')
        # Installation Mode
        f.write('# Installation Mode\n')
        f.write('installMode=fresh\n')
        f.write('installInteractive=no\n')
        f.write('installType=GhostBSD\n')
        f.write('installMedium=livezfs\n')
        f.write('packageType=livezfs\n')
        # System Language
        if os.path.exists(language):
            langfile = open(language, 'r')
            lang = langfile.readlines()[0].rstrip()
            f.write('\n# System Language\n')
            f.write(f'localizeLang={lang}\n')
        # Keyboard Setting
        if os.path.exists(KBFile):
            f.write('\n# Keyboard Setting\n')
            rkb = open(KBFile, 'r')
            kb = rkb.readlines()
            kbl = kb[0].rstrip()
            f.write(f'localizeKeyLayout={kbl}\n')
            kbv = kb[1].rstrip()
            if kbv != 'None':
                f.write(f'localizeKeyVariant={kbv}\n')
            kbm = kb[2].rstrip()
            if kbm != 'None':
                f.write(f'localizeKeyModel={kbm}\n')
        # Timezone
        if os.path.exists(timezone):
            time = open(timezone, 'r')
            t_output = time.readlines()[0].strip()
            f.write('\n# Timezone\n')
            f.write(f'timeZone={t_output}\n')
            f.write('enableNTP=yes\n')
        if os.path.exists(zfs_config):
            zfs = True
            # Disk Setup
            r = open(zfs_config, 'r')
            zfsconf = r.readlines()
            for line in zfsconf:
                if 'partscheme' in line:
                    f.write(line)
                    read = open(boot_file, 'r')
                    boot = read.readlines()[0].strip()
                    if boot == 'refind':
                        f.write('bootManager=none\n')
                        f.write(f'efiLoader={boot}\n')
                    else:
                        f.write(f'bootManager={boot}\n')
                        f.write('efiLoader=none\n')
                else:
                    f.write(line)
        elif os.path.exists(ufs_config):
            zfs = False
            # Disk Setup
            r = open(ufs_config, 'r')
            ufsconf = r.readlines()
            for line in ufsconf:
                if 'partscheme' in line:
                    f.write(line)
                    read = open(boot_file, 'r')
                    boot = read.readlines()[0].strip()
                    if boot == 'refind':
                        f.write('bootManager=none\n')
                        f.write(f'efiLoader={boot}\n')
                    else:
                        f.write(f'bootManager={boot}\n')
                        f.write('efiLoader=none\n')
                else:
                    f.write(line)
        else:
            # Disk Setup
            r = open(disk, 'r')
            drive = r.readlines()
            d_output = drive[0].strip()
            f.write('\n# Disk Setup\n')
            f.write('ashift=12\n')
            f.write(f'disk0={d_output}\n')
            # Partition Slice.
            p = open(dslice, 'r')
            line = p.readlines()
            part = line[0].rstrip()
            f.write(f'partition={part}\n')
            # Boot Menu
            read = open(boot_file, 'r')
            line = read.readlines()
            boot = line[0].strip()
            if boot == 'refind':
                f.write('bootManager=none\n')
                f.write(f'efiLoader={boot}\n')
            else:
                f.write(f'bootManager={boot}\n')
                f.write('efiLoader=none\n')
            # Scheme
            read = open(disk_scheme, 'r')
            scheme = read.readlines()[0]
            f.write(f'{scheme}\n')
            f.write('commitDiskPart\n')
            # Partition Setup
            f.write('\n# Partition Setup\n')
            part = open(partlabel, 'r').read()
            zfs = True if 'ZFS' in part else False
            # If slice and auto file exist add first partition line.
            # But Swap need to be 0 it will take the rest of the freespace.
            for line in part.splitlines():
                if 'BOOT' in line or 'BIOS' in line or 'UEFI' in line:
                    pass
                else:
                    f.write(f'disk0-part={line.strip()}\n')
            f.write('commitDiskLabel\n')
        if os.path.exists(user_passwd):
            # Network Configuration
            f.write('\n# Network Configuration\n')
            readu = open(user_passwd, 'rb')
            uf = pickle.load(readu)
            hostname = uf[5]
            f.write(f'hostname={hostname}\n')
            # Set the root pass
            f.write('\n# Root Password\n')
            readr = open(f'{tmp}/root', 'rb')
            rf = pickle.load(readr)
            root = rf[0]
            f.write(f'rootPass={root}\n')
            # Setup our users
            user = uf[0]
            f.write('\n# Setup user\n')
            f.write(f'userName={user}\n')
            name = uf[1]
            f.write(f'userComment={name}\n')
            passwd = uf[2]
            f.write(f'userPass={passwd.rstrip()}\n')
            shell = uf[3]
            f.write(f'userShell={shell}\n')
            upath = uf[4]
            f.write(f'userHome={upath.rstrip()}\n')
            f.write('userGroups=wheel,operator\n')
            f.write('commitUser\n')
            f.write('\n# Run command and script\n')
            f.write("""runCommand=sed -i '' 's/lightdm_enable="NO"/"""
                    """lightdm_enable="YES"/g' /etc/rc.conf\n""")
            f.write('runCommand=sed -i "" "/ghostbsd/d" /etc/gettytab\n')
            f.write(
                'runCommand=sed -i "" "/ttyv0/s/ghostbsd/Pc/g" /etc/ttys\n')

            f.write("runCommand=mv /usr/local/etc/devd/automount_devd"
                    ".conf.skip /usr/local/etc/devd/automount_devd.conf\n")
            f.write("runCommand=mv /usr/local/etc/devd/automount_devd"
                    "_localdisks.conf.skip /usr/local/etc/devd/"
                    "automount_devd_localdisks.conf\n")
            if zfs is True:
                zfs_arc = "echo 'vfs.zfs.arc.sys_free=\"1G\"' >> /boot/loader.conf"
                f.write(f'runCommand={zfs_arc}\n')
        else:
            f.write('\n# Network Configuration\n')
            f.write('hostname=installed\n')
            f.write('\n# command to prepare first boot\n')
            f.write("runCommand=sysrc hostname='installed'\n")
            f.write("runCommand=pw userdel -n ghostbsd -r\n")
            f.write("runCommand=sed -i '' 's/ghostbsd/root/g' /etc/gettytab\n")
            f.write("runCommand=sed -i '' 's/ghostbsd/root/g' /etc/ttys\n")
            f.write("runCommand=mv /usr/local/etc/devd/automount_devd"
                    ".conf.skip /usr/local/etc/devd/automount_devd.conf\n")
            f.write("runCommand=mv /usr/local/etc/devd/automount_devd"
                    "_localdisks.conf.skip /usr/local/etc/devd/"
                    "automount_devd_localdisks.conf\n")
        f.write("runCommand=echo '# For XHCI Mouse Support' >> /boot/loader.conf\n")
        f.write("runCommand=echo 'hw.usb.usbhid.enable=\"1\"' >> /boot/loader.conf\n")
        f.write("runCommand=echo 'usbhid_load=\"YES\"' >> /boot/loader.conf\n")
        f.write("runCommand=echo '# For UTouch Support' >> /boot/loader.conf\n")
        f.write("runCommand=echo 'utouch_load=\"YES\"' >> /boot/loader.conf\n")
        f.close()
