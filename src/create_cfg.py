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
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
# Installer data file.
disk = '%sdisk' % tmp
layout = '%slayout' % tmp
model = '%smodel' % tmp
pcinstallcfg = '%spcinstall.cfg' % tmp
user_passwd = '%suser' % tmp
language = '%slanguage' % tmp
dslice = '%sslice' % tmp
left = '%sleft' % tmp
partlabel = '%spartlabel' % tmp
timezone = '%stimezone' % tmp
KBFile = '%skeyboard' % tmp
boot_file = '%sboot' % tmp
disk_schem = '%sscheme' % tmp
zfs_config = '%szfs_config' % tmp
ufs_config = tmp + 'ufs_config'


class gbsd_cfg():
    def __init__(self):
        f = open('%spcinstall.cfg' % tmp, 'w')
        # Installation Mode
        f.writelines('# Installation Mode\n')
        f.writelines('installMode=fresh\n')
        f.writelines('installInteractive=no\n')
        f.writelines('installType=GhostBSD\n')
        f.writelines('installMedium=livecd\n')
        f.writelines('packageType=livecd\n')
        # System Language
        langfile = open(language, 'r')
        lang = langfile.readlines()[0].rstrip()
        f.writelines('\n# System Language\n\n')
        f.writelines('localizeLang=%s\n' % lang)
        os.remove(language)
        # Keyboard Setting
        if os.path.exists(model):
            f.writelines('\n# Keyboard Setting\n')
            os.remove(model)
        if os.path.exists(KBFile):
            rkb = open(KBFile, 'r')
            kb = rkb.readlines()
            kbl = kb[0].rstrip()
            f.writelines('localizeKeyLayout=%s\n' % kbl)
            kbv = kb[1].rstrip()
            if kbv != 'None':
                f.writelines('localizeKeyVariant=%s\n' % kbv)
            kbm = kb[2].rstrip()
            if kbm != 'None':
                f.writelines('localizeKeyModel=%s\n' % kbm)
        # Timezone
        if os.path.exists(timezone):
            time = open(timezone, 'r')
            t_output = time.readlines()[0].strip()
            f.writelines('\n# Timezone\n')
            f.writelines('timeZone=%s\n' % t_output)
            f.writelines('enableNTP=yes\n')
            os.remove(timezone)
        if os.path.exists(zfs_config):
            # Disk Setup
            r = open(zfs_config, 'r')
            zfsconf = r.readlines()
            for line in zfsconf:
                if 'partscheme' in line:
                    f.writelines(line)
                    read = open(boot_file, 'r')
                    boot = read.readlines()[0].strip()
                    f.writelines('bootManager=%s\n' % boot)
                    os.remove(boot_file)
                else:
                    f.writelines(line)
            # os.remove(zfs_config)
        elif os.path.exists(ufs_config):
            # Disk Setup
            r = open(ufs_config, 'r')
            ufsconf = r.readlines()
            for line in ufsconf:
                if 'partscheme' in line:
                    f.writelines(line)
                    read = open(boot_file, 'r')
                    boot = read.readlines()[0].strip()
                    f.writelines('bootManager=%s\n' % boot)
                    os.remove(boot_file)
                else:
                    f.writelines(line)
        else:
            # Disk Setup
            r = open(disk, 'r')
            drive = r.readlines()
            d_output = drive[0].strip()
            f.writelines('\n# Disk Setup\n')
            f.writelines('disk0=%s\n' % d_output)
            os.remove(disk)
            # Partition Slice.
            p = open(dslice, 'r')
            line = p.readlines()
            part = line[0].rstrip()
            f.writelines('partition=%s\n' % part)
            os.remove(dslice)
            # Boot Menu
            read = open(boot_file, 'r')
            line = read.readlines()
            boot = line[0].strip()
            f.writelines('bootManager=%s\n' % boot)
            # os.remove(boot_file)
            # Sheme sheme
            read = open(disk_schem, 'r')
            shem = read.readlines()[0]
            f.writelines(shem + '\n')
            f.writelines('commitDiskPart\n')
            # os.remove(disk_schem)
            # Partition Setup
            f.writelines('\n# Partition Setup\n')
            part = open(partlabel, 'r')
            # If slice and auto file exist add first partition line.
            # But Swap need to be 0 it will take the rest of the freespace.
            for line in part:
                if 'BOOT' in line or 'BIOS' in line or 'UEFI' in line:
                    pass
                else:
                    f.writelines('disk0-part=%s\n' % line.strip())
            f.writelines('commitDiskLabel\n')
            os.remove(partlabel)
        # Network Configuration
        f.writelines('\n# Network Configuration\n')
        readu = open(user_passwd, 'rb')
        uf = pickle.load(readu)
        net = uf[5]
        f.writelines('hostname=%s\n' % net)
        # Set the root pass
        f.writelines('\n# Network Configuration\n')
        readr = open('%sroot' % tmp, 'rb')
        rf = pickle.load(readr)
        root = rf[0]
        f.writelines('\n# Set the root pass\n')
        f.writelines('rootPass=%s\n' % root)
        # Setup our users
        user = uf[0]
        f.writelines('\n# Setup user\n')
        f.writelines('userName=%s\n' % user)
        name = uf[1]
        f.writelines('userComment=%s\n' % name)
        passwd = uf[2]
        f.writelines('userPass=%s\n' % passwd.rstrip())
        shell = uf[3]
        f.writelines('userShell=%s\n' % shell)
        upath = uf[4]
        f.writelines('userHome=%s\n' % upath.rstrip())
        f.writelines('defaultGroup=wheel\n')
        f.writelines('userGroups=operator\n')
        f.writelines('commitUser\n')
        ifvbox = open('/tmp/.ifvbox', 'w')
        vbguest = Popen('pciconf -lv | grep "VirtualBox Graphics"', shell=True,
                        stdout=PIPE, close_fds=True, universal_newlines=True)
        if "VirtualBox Graphics" in vbguest.stdout.read():
            ifvbox.writelines('True\n')
        else:
            ifvbox.writelines('False\n')
        ifvbox.close()
        f.writelines('runScript=/root/iso_to_hd.sh\n')
        f.writelines('runCommand=rm -f /root/iso_to_hd.sh\n')
        if os.path.exists(zfs_config):
            zfsark = """echo 'vfs.zfs.arc_max="512M"' >> /boot/loader.conf"""
            f.writelines('runCommand=%s\n' % zfsark)
        if "af" == lang:
            f.writelines('runCommand=pkg install -y af-libreoffice\n')
        elif "ar" == lang:
            f.writelines('runCommand=pkg install -y ar-libreoffice\n')
        elif "bg" == lang:
            f.writelines('runCommand=pkg install -y bg-libreoffice\n')
        elif "bn" == lang:
            f.writelines('runCommand=pkg install -y bn-libreoffice\n')
        elif "br" == lang:
            f.writelines('runCommand=pkg install -y br-libreoffice\n')
        elif "bs" == lang:
            f.writelines('runCommand=pkg install -y bs-libreoffice\n')
        elif "ca" == lang:
            f.writelines('runCommand=pkg install -y ca-libreoffice\n')
        elif "cs" == lang:
            f.writelines('runCommand=pkg install -y cs-libreoffice\n')
        elif "cy" == lang:
            f.writelines('runCommand=pkg install -y cy-libreoffice\n')
        elif "da" == lang:
            f.writelines('runCommand=pkg install -y da-libreoffice\n')
        elif "de" == lang:
            f.writelines('runCommand=pkg install -y de-libreoffice\n')
        elif "el" == lang:
            f.writelines('runCommand=pkg install -y el-libreoffice\n')
        elif "en_GB" == lang:
            f.writelines('runCommand=pkg install -y en_GB-libreoffice\n')
        elif "en_ZA" == lang:
            f.writelines('runCommand=pkg install -y en_ZA-libreoffice\n')
        elif "es" == lang:
            f.writelines('runCommand=pkg install -y es-libreoffice\n')
        elif "et" == lang:
            f.writelines('runCommand=pkg install -y et-libreoffice\n')
        elif "eu" == lang:
            f.writelines('runCommand=pkg install -y eu-libreoffice\n')
        elif "fa" == lang:
            f.writelines('runCommand=pkg install -y fa-libreoffice\n')
        elif "fi" == lang:
            f.writelines('runCommand=pkg install -y fi-libreoffice\n')
        elif "fr" in lang:
            f.writelines('runCommand=pkg install -y fr-libreoffice\n')
        elif "ga" == lang:
            f.writelines('runCommand=pkg install -y ga-libreoffice\n')
        elif "gb" == lang:
            f.writelines('runCommand=pkg install -y gd-libreoffice\n')
        elif "gl" == lang:
            f.writelines('runCommand=pkg install -y gl-libreoffice\n')
        elif "he" == lang:
            f.writelines('runCommand=pkg install -y he-libreoffice\n')
        elif "hi" == lang:
            f.writelines('runCommand=pkg install -y hi-libreoffice\n')
        elif "hr" == lang:
            f.writelines('runCommand=pkg install -y hr-libreoffice\n')
        elif "hu" == lang:
            f.writelines('runCommand=pkg install -y hu-libreoffice\n')
        elif "id" == lang:
            f.writelines('runCommand=pkg install -y id-libreoffice\n')
        elif "is" == lang:
            f.writelines('runCommand=pkg install -y is-libreoffice\n')
        elif "it" == lang:
            f.writelines('runCommand=pkg install -y it-libreoffice\n')
        elif "ja" == lang:
            f.writelines('runCommand=pkg install -y ja-libreoffice\n')
        elif "ko" == lang:
            f.writelines('runCommand=pkg install -y ko-libreoffice\n')
        elif "lt" == lang:
            f.writelines('runCommand=pkg install -y lt-libreoffice\n')
        elif "lv" == lang:
            f.writelines('runCommand=pkg install -y lv-libreoffice\n')
        elif "mk" == lang:
            f.writelines('runCommand=pkg install -y mk-libreoffice\n')
        elif "mn" == lang:
            f.writelines('runCommand=pkg install -y mn-libreoffice\n')
        elif "nb" == lang:
            f.writelines('runCommand=pkg install -y nb-libreoffice\n')
        elif "ne" == lang:
            f.writelines('runCommand=pkg install -y ne-libreoffice\n')
        elif "nl" == lang:
            f.writelines('runCommand=pkg install -y nl-libreoffice\n')
        elif "pa_IN" == lang:
            f.writelines('runCommand=pkg install -y pa_IN-libreoffice\n')
        elif "pl" == lang:
            f.writelines('runCommand=pkg install -y pl-libreoffice\n')
        elif "pt" == lang:
            f.writelines('runCommand=pkg install -y pt-libreoffice\n')
        elif "pt_BR" == lang:
            f.writelines('runCommand=pkg install -y pt_BR-libreoffice\n')
        elif "ro" == lang:
            f.writelines('runCommand=pkg install -y ro-libreoffice\n')
        elif "ru" == lang:
            f.writelines('runCommand=pkg install -y ru-libreoffice\n')
        elif "sd" == lang:
            f.writelines('runCommand=pkg install -y sd-libreoffice\n')
        elif "sk" == lang:
            f.writelines('runCommand=pkg install -y sk-libreoffice\n')
        elif "sl" == lang:
            f.writelines('runCommand=pkg install -y sl-libreoffice\n')
        elif "sr" == lang:
            f.writelines('runCommand=pkg install -y sr-libreoffice\n')
        elif "sv" == lang:
            f.writelines('runCommand=pkg install -y sv-libreoffice\n')
        elif "ta" == lang:
            f.writelines('runCommand=pkg install -y ta-libreoffice\n')
        elif "tg" == lang:
            f.writelines('runCommand=pkg install -y tg-libreoffice\n')
        elif "tr" == lang:
            f.writelines('runCommand=pkg install -y tr-libreoffice\n')
        elif "uk" == lang:
            f.writelines('runCommand=pkg install -y uk-libreoffice\n')
        elif "vi" == lang:
            f.writelines('runCommand=pkg install -y vi-libreoffice\n')
        elif "zh_CN" == lang:
            f.writelines('runCommand=pkg install -y zh_CN-libreoffice\n')
        elif "zh_TW" == lang:
            f.writelines('runCommand=pkg install -y zh_TW-libreoffice\n')
        elif "zu" == lang:
            f.writelines('runCommand=pkg install -y zu-libreoffice\n')
        f.close()
        os.remove(user_passwd)
