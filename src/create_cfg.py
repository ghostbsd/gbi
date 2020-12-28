#!/usr/bin/env python
#
# Copyright (c) 2013 GhostBSD
#
# See COPYING for licence terms.
#
# create_cfg.py v 1.4 Friday, January 17 2014 Eric Turgeon
#

import os
import pickle
from subprocess import Popen, PIPE

# Directory use from the installer.
tmp = "/tmp/.gbi"
installer = "/usr/local/lib/gbi/"
# Installer data file.
disk = f'{tmp}/disk'
pcinstallcfg = f'{tmp}/pcinstall.cfg'
user_passwd = f'{tmp}/user'
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


class gbsd_cfg():
    def __init__(self):
        f = open(f'{tmp}/pcinstall.cfg', 'w')
        # Installation Mode
        f.writelines('# Installation Mode\n')
        f.writelines('installMode=fresh\n')
        f.writelines('installInteractive=no\n')
        f.writelines('installType=GhostBSD\n')
        f.writelines('installMedium=livecd\n')
        f.writelines('packageType=livecd\n')
        # System Language
        if os.path.exists(language):
            langfile = open(language, 'r')
            lang = langfile.readlines()[0].rstrip()
            f.writelines('\n# System Language\n')
            f.writelines(f'localizeLang={lang}\n')
        # Keyboard Setting
        if os.path.exists(KBFile):
            f.writelines('\n# Keyboard Setting\n')
            rkb = open(KBFile, 'r')
            kb = rkb.readlines()
            kbl = kb[0].rstrip()
            f.writelines(f'localizeKeyLayout={kbl}\n')
            kbv = kb[1].rstrip()
            if kbv != 'None':
                f.writelines(f'localizeKeyVariant={kbv}\n')
            kbm = kb[2].rstrip()
            if kbm != 'None':
                f.writelines(f'localizeKeyModel={kbm}\n')
        # Timezone
        if os.path.exists(timezone):
            time = open(timezone, 'r')
            t_output = time.readlines()[0].strip()
            f.writelines('\n# Timezone\n')
            f.writelines(f'timeZone={t_output}\n')
            f.writelines('enableNTP=yes\n')
        if os.path.exists(zfs_config):
            # Disk Setup
            r = open(zfs_config, 'r')
            zfsconf = r.readlines()
            for line in zfsconf:
                if 'partscheme' in line:
                    f.writelines(line)
                    read = open(boot_file, 'r')
                    boot = read.readlines()[0].strip()
                    if boot == 'refind':
                        f.writelines('bootManager=none\n')
                        f.writelines(f'efiLoader={boot}\n')
                    else:
                        f.writelines(f'bootManager={boot}\n')
                        f.writelines('efiLoader=none\n')
                else:
                    f.writelines(line)
        elif os.path.exists(ufs_config):
            # Disk Setup
            r = open(ufs_config, 'r')
            ufsconf = r.readlines()
            for line in ufsconf:
                if 'partscheme' in line:
                    f.writelines(line)
                    read = open(boot_file, 'r')
                    boot = read.readlines()[0].strip()
                    if boot == 'refind':
                        f.writelines('bootManager=none\n')
                        f.writelines(f'efiLoader={boot}\n')
                    else:
                        f.writelines(f'bootManager={boot}\n')
                        f.writelines('efiLoader=none\n')
                else:
                    f.writelines(line)
        else:
            # Disk Setup
            r = open(disk, 'r')
            drive = r.readlines()
            d_output = drive[0].strip()
            f.writelines('\n# Disk Setup\n')
            f.writelines('ashift=12\n')
            f.writelines(f'disk0={d_output}\n')
            # Partition Slice.
            p = open(dslice, 'r')
            line = p.readlines()
            part = line[0].rstrip()
            f.writelines(f'partition={part}\n')
            # Boot Menu
            read = open(boot_file, 'r')
            line = read.readlines()
            boot = line[0].strip()
            if boot == 'refind':
                f.writelines('bootManager=none\n')
                f.writelines(f'efiLoader={boot}\n')
            else:
                f.writelines(f'bootManager={boot}\n')
                f.writelines('efiLoader=none\n')
            # Scheme
            read = open(disk_scheme, 'r')
            scheme = read.readlines()[0]
            f.writelines(f'{scheme}\n')
            f.writelines('commitDiskPart\n')
            # Partition Setup
            f.writelines('\n# Partition Setup\n')
            part = open(partlabel, 'r')
            # If slice and auto file exist add first partition line.
            # But Swap need to be 0 it will take the rest of the freespace.
            for line in part:
                if 'BOOT' in line or 'BIOS' in line or 'UEFI' in line:
                    pass
                else:
                    f.writelines(f'disk0-part={line.strip()}\n')
            f.writelines('commitDiskLabel\n')
        if os.path.exists(user_passwd):
            # Network Configuration
            f.writelines('\n# Network Configuration\n')
            readu = open(user_passwd, 'rb')
            uf = pickle.load(readu)
            hostname = uf[5]
            f.writelines(f'hostname={hostname}\n')
            # Set the root pass
            f.writelines('\n# Root Password\n')
            readr = open(f'{tmp}/root', 'rb')
            rf = pickle.load(readr)
            root = rf[0]
            f.writelines(f'rootPass={root}\n')
            # Setup our users
            user = uf[0]
            f.writelines('\n# Setup user\n')
            f.writelines(f'userName={user}\n')
            name = uf[1]
            f.writelines(f'userComment={name}\n')
            passwd = uf[2]
            f.writelines(f'userPass={passwd.rstrip()}\n')
            shell = uf[3]
            f.writelines(f'userShell={shell}\n')
            upath = uf[4]
            f.writelines(f'userHome={upath.rstrip()}\n')
            f.writelines('defaultGroup=wheel\n')
            f.writelines('userGroups=operator\n')
            f.writelines('commitUser\n')
            f.writelines('\n# Run command and script\n')
            nv = Popen('pciconf -lv | grep -B 4 VGA', shell=True,
                       stdout=PIPE, close_fds=True, universal_newlines=True)
            if "NVIDIA" not in nv.stdout.read():
                f.writelines('runCommand=pkg delete -fy nvidia-driver\n')
            vbguest = Popen('pciconf -lv | grep "VirtualBox"', shell=True,
                            stdout=PIPE, close_fds=True, universal_newlines=True)
            if "VirtualBox" in vbguest.stdout.read():
                f.writelines('runCommand=rc-update add vboxguest default\n')
                f.writelines('runCommand=rc-update add vboxservice default\n')
            else:
                f.writelines('runCommand=pkg delete -fy virtualbox-ose-additions\n')
            if os.path.exists("/etc/wpa_supplicant.conf"):
                f.writelines('runExtCommand=cp /etc/wpa_supplicant.conf $FSMNT/etc/wpa_supplicant.conf\n')
                f.writelines('runExtCommand=chmod 665 $FSMNT/etc/wpa_supplicant.conf\n')
            if os.path.exists("/etc/X11/xorg.conf"):
                f.writelines('runExtCommand=cp /etc/X11/xorg.conf $FSMNT/etc/X11/xorg.conf\n')
            f.writelines('runScript=/root/iso_to_hd.sh\n')
            f.writelines('runCommand=rm -f /root/iso_to_hd.sh\n')
            if os.path.exists(zfs_config):
                zfsark = """echo 'vfs.zfs.arc_max="512M"' >> /boot/loader.conf"""
                f.writelines(f'runCommand={zfsark}\n')
        else:
            # Network Configuration
            f.writelines('\n# Network Configuration\n')
            f.writelines('hostname=installed\n')
        f.close()
