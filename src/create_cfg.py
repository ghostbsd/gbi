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
from subprocess import Popen

# Directory use from the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
start_Install = 'python %sinstall.py' % installer
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


class gbsd_cfg():
    def __init__(self):
        f = open('%spcinstall.cfg' % tmp, 'w')
        # Installation Mode
        f.writelines('# Installation Mode\n')
        f.writelines('installMode=fresh\n')
        f.writelines('installInteractive=no\n')
        f.writelines('installType=GhostBSD\n')
        f.writelines('installMedium=dvd\n')
        f.writelines('packageType=livecd\n')
        # System Language
        lang = open(language, 'r')
        lang_output = lang.readlines()[0].strip().split()[0].strip()
        f.writelines('\n# System Language\n\n')
        f.writelines('localizeLang=%s\n' % lang_output)
        os.remove(language)
        # Keyboard Setting
        if os.path.exists(model):
            f.writelines('\n# Keyboard Setting\n')
            os.remove(model)
        if os.path.exists(KBFile):
            rkb = open(KBFile, 'r')
            kb = rkb.readlines()
            if len(kb) == 2:
                l_output = kb[0].strip().partition('-')[2].strip()
                f.writelines('localizeKeyLayout=%s\n' % l_output)
                v_output = kb[1].strip().partition(':')[2].strip()
                f.writelines('localizeKeyVariant=%s\n' % v_output)
            else:
                l_output = kb[0].strip().partition('-')[2].strip()
                f.writelines('localizeKeyLayout=%s\n' % l_output)
            os.remove(KBFile)
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
            #os.remove(boot_file)
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
        f.writelines('runScript=/usr/local/bin/iso_to_hd\n')
        if "af" == lang_output:
            f.writelines('runCommand=pkg install -y af-libreoffice\n')
        elif "ar" == lang_output:
            f.writelines('runCommand=pkg install -y ar-libreoffice\n')
        elif "bg" == lang_output:
            f.writelines('runCommand=pkg install -y bg-libreoffice\n')
        elif "bn" == lang_output:
            f.writelines('runCommand=pkg install -y bn-libreoffice\n')
        elif "br" == lang_output:
            f.writelines('runCommand=pkg install -y br-libreoffice\n')
        elif "bs" == lang_output:
            f.writelines('runCommand=pkg install -y bs-libreoffice\n')
        elif "ca" == lang_output:
            f.writelines('runCommand=pkg install -y ca-libreoffice\n')
        elif "cs" == lang_output:
            f.writelines('runCommand=pkg install -y cs-libreoffice\n')
        elif "cy" == lang_output:
            f.writelines('runCommand=pkg install -y cy-libreoffice\n')
        elif "da" == lang_output:
            f.writelines('runCommand=pkg install -y da-libreoffice\n')
        elif "de" == lang_output:
            f.writelines('runCommand=pkg install -y de-libreoffice\n')
        elif "el" == lang_output:
            f.writelines('runCommand=pkg install -y el-libreoffice\n')
        elif "en_GB" == lang_output:
            f.writelines('runCommand=pkg install -y en_GB-libreoffice\n')
        elif "en_ZA" == lang_output:
            f.writelines('runCommand=pkg install -y en_ZA-libreoffice\n')
        elif "es" == lang_output:
            f.writelines('runCommand=pkg install -y es-libreoffice\n')
        elif "et" == lang_output:
            f.writelines('runCommand=pkg install -y et-libreoffice\n')
        elif "eu" == lang_output:
            f.writelines('runCommand=pkg install -y eu-libreoffice\n')
        elif "fa" == lang_output:
            f.writelines('runCommand=pkg install -y fa-libreoffice\n')
        elif "fi" == lang_output:
            f.writelines('runCommand=pkg install -y fi-libreoffice\n')
        elif "fr" in lang_output:
            f.writelines('runCommand=pkg install -y fr-libreoffice\n')
        elif "ga" == lang_output:
            f.writelines('runCommand=pkg install -y ga-libreoffice\n')
        elif "gb" == lang_output:
            f.writelines('runCommand=pkg install -y gd-libreoffice\n')
        elif "gl" == lang_output:
            f.writelines('runCommand=pkg install -y gl-libreoffice\n')
        elif "he" == lang_output:
            f.writelines('runCommand=pkg install -y he-libreoffice\n')
        elif "hi" == lang_output:
            f.writelines('runCommand=pkg install -y hi-libreoffice\n')
        elif "hr" == lang_output:
            f.writelines('runCommand=pkg install -y hr-libreoffice\n')
        elif "hu" == lang_output:
            f.writelines('runCommand=pkg install -y hu-libreoffice\n')
        elif "id" == lang_output:
            f.writelines('runCommand=pkg install -y id-libreoffice\n')
        elif "is" == lang_output:
            f.writelines('runCommand=pkg install -y is-libreoffice\n')
        elif "it" == lang_output:
            f.writelines('runCommand=pkg install -y it-libreoffice\n')
        elif "ja" == lang_output:
            f.writelines('runCommand=pkg install -y ja-libreoffice\n')
        elif "ko" == lang_output:
            f.writelines('runCommand=pkg install -y ko-libreoffice\n')
        elif "lt" == lang_output:
            f.writelines('runCommand=pkg install -y lt-libreoffice\n')
        elif "lv" == lang_output:
            f.writelines('runCommand=pkg install -y lv-libreoffice\n')
        elif "mk" == lang_output:
            f.writelines('runCommand=pkg install -y mk-libreoffice\n')
        elif "mn" == lang_output:
            f.writelines('runCommand=pkg install -y mn-libreoffice\n')
        elif "nb" == lang_output:
            f.writelines('runCommand=pkg install -y nb-libreoffice\n')
        elif "ne" == lang_output:
            f.writelines('runCommand=pkg install -y ne-libreoffice\n')
        elif "nl" == lang_output:
            f.writelines('runCommand=pkg install -y nl-libreoffice\n')
        elif "pa_IN" == lang_output:
            f.writelines('runCommand=pkg install -y pa_IN-libreoffice\n')
        elif "pl" == lang_output:
            f.writelines('runCommand=pkg install -y pl-libreoffice\n')
        elif "pt" == lang_output:
            f.writelines('runCommand=pkg install -y pt-libreoffice\n')
        elif "pt_BR" == lang_output:
            f.writelines('runCommand=pkg install -y pt_BR-libreoffice\n')
        elif "ro" == lang_output:
            f.writelines('runCommand=pkg install -y ro-libreoffice\n')
        elif "ru" == lang_output:
            f.writelines('runCommand=pkg install -y ru-libreoffice\n')
        elif "sd" == lang_output:
            f.writelines('runCommand=pkg install -y sd-libreoffice\n')
        elif "sk" == lang_output:
            f.writelines('runCommand=pkg install -y sk-libreoffice\n')
        elif "sl" == lang_output:
            f.writelines('runCommand=pkg install -y sl-libreoffice\n')
        elif "sr" == lang_output:
            f.writelines('runCommand=pkg install -y sr-libreoffice\n')
        elif "sv" == lang_output:
            f.writelines('runCommand=pkg install -y sv-libreoffice\n')
        elif "ta" == lang_output:
            f.writelines('runCommand=pkg install -y ta-libreoffice\n')
        elif "tg" == lang_output:
            f.writelines('runCommand=pkg install -y tg-libreoffice\n')
        elif "tr" == lang_output:
            f.writelines('runCommand=pkg install -y tr-libreoffice\n')
        elif "uk" == lang_output:
            f.writelines('runCommand=pkg install -y uk-libreoffice\n')
        elif "vi" == lang_output:
            f.writelines('runCommand=pkg install -y vi-libreoffice\n')
        elif "zh_CN" == lang_output:
            f.writelines('runCommand=pkg install -y zh_CN-libreoffice\n')
        elif "zh_TW" == lang_output:
            f.writelines('runCommand=pkg install -y zh_TW-libreoffice\n')
        elif "zu" == lang_output:
            f.writelines('runCommand=pkg install -y zu-libreoffice\n')
        f.close()
        os.remove(user_passwd)
        Popen(start_Install, shell=True)

class dbsd_cfg():
    def __init__(self):
        f = open('%spcinstall.cfg' % tmp, 'w')
        # Installation Mode
        f.writelines('# Installation Mode\n')
        f.writelines('installMode=fresh\n')
        f.writelines('installInteractive=no\n')
        f.writelines('installType=DesktopBSD\n')
        f.writelines('installMedium=dvd\n')
        f.writelines('packageType=livecd\n')
        # System Language
        lang = open(language, 'r')
        lang_output = lang.readlines()[0].strip().split()[0].strip()
        f.writelines('\n# System Language\n\n')
        f.writelines('localizeLang=%s\n' % lang_output)
        os.remove(language)
        # Keyboard Setting
        if os.path.exists(model):
            f.writelines('\n# Keyboard Setting\n')
            os.remove(model)
        if os.path.exists(KBFile):
            rkb = open(KBFile, 'r')
            kb = rkb.readlines()
            if len(kb) == 2:
                l_output = kb[0].strip().partition('-')[2].strip()
                f.writelines('localizeKeyLayout=%s\n' % l_output)
                v_output = kb[1].strip().partition(':')[2].strip()
                f.writelines('localizeKeyVariant=%s\n' % v_output)
            else:
                l_output = kb[0].strip().partition('-')[2].strip()
                f.writelines('localizeKeyLayout=%s\n' % l_output)
            os.remove(KBFile)
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
            os.remove(boot_file)
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
                if 'BOOT' in line:
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
        f.writelines('runScript=/usr/local/bin/iso_to_hd\n')
        if "af" == lang_output:
            f.writelines('runCommand=pkg install -y af-libreoffice\n')
        elif "ar" == lang_output:
            f.writelines('runCommand=pkg install -y ar-libreoffice\n')
        elif "bg" == lang_output:
            f.writelines('runCommand=pkg install -y bg-libreoffice\n')
        elif "bn" == lang_output:
            f.writelines('runCommand=pkg install -y bn-libreoffice\n')
        elif "br" == lang_output:
            f.writelines('runCommand=pkg install -y br-libreoffice\n')
        elif "bs" == lang_output:
            f.writelines('runCommand=pkg install -y bs-libreoffice\n')
        elif "ca" == lang_output:
            f.writelines('runCommand=pkg install -y ca-libreoffice\n')
        elif "cs" == lang_output:
            f.writelines('runCommand=pkg install -y cs-libreoffice\n')
        elif "cy" == lang_output:
            f.writelines('runCommand=pkg install -y cy-libreoffice\n')
        elif "da" == lang_output:
            f.writelines('runCommand=pkg install -y da-libreoffice\n')
        elif "de" == lang_output:
            f.writelines('runCommand=pkg install -y de-libreoffice\n')
        elif "el" == lang_output:
            f.writelines('runCommand=pkg install -y el-libreoffice\n')
        elif "en_GB" == lang_output:
            f.writelines('runCommand=pkg install -y en_GB-libreoffice\n')
        elif "en_ZA" == lang_output:
            f.writelines('runCommand=pkg install -y en_ZA-libreoffice\n')
        elif "es" == lang_output:
            f.writelines('runCommand=pkg install -y es-libreoffice\n')
        elif "et" == lang_output:
            f.writelines('runCommand=pkg install -y et-libreoffice\n')
        elif "eu" == lang_output:
            f.writelines('runCommand=pkg install -y eu-libreoffice\n')
        elif "fa" == lang_output:
            f.writelines('runCommand=pkg install -y fa-libreoffice\n')
        elif "fi" == lang_output:
            f.writelines('runCommand=pkg install -y fi-libreoffice\n')
        elif "fr" in lang_output:
            f.writelines('runCommand=pkg install -y fr-libreoffice\n')
        elif "ga" == lang_output:
            f.writelines('runCommand=pkg install -y ga-libreoffice\n')
        elif "gb" == lang_output:
            f.writelines('runCommand=pkg install -y gd-libreoffice\n')
        elif "gl" == lang_output:
            f.writelines('runCommand=pkg install -y gl-libreoffice\n')
        elif "he" == lang_output:
            f.writelines('runCommand=pkg install -y he-libreoffice\n')
        elif "hi" == lang_output:
            f.writelines('runCommand=pkg install -y hi-libreoffice\n')
        elif "hr" == lang_output:
            f.writelines('runCommand=pkg install -y hr-libreoffice\n')
        elif "hu" == lang_output:
            f.writelines('runCommand=pkg install -y hu-libreoffice\n')
        elif "id" == lang_output:
            f.writelines('runCommand=pkg install -y id-libreoffice\n')
        elif "is" == lang_output:
            f.writelines('runCommand=pkg install -y is-libreoffice\n')
        elif "it" == lang_output:
            f.writelines('runCommand=pkg install -y it-libreoffice\n')
        elif "ja" == lang_output:
            f.writelines('runCommand=pkg install -y ja-libreoffice\n')
        elif "ko" == lang_output:
            f.writelines('runCommand=pkg install -y ko-libreoffice\n')
        elif "lt" == lang_output:
            f.writelines('runCommand=pkg install -y lt-libreoffice\n')
        elif "lv" == lang_output:
            f.writelines('runCommand=pkg install -y lv-libreoffice\n')
        elif "mk" == lang_output:
            f.writelines('runCommand=pkg install -y mk-libreoffice\n')
        elif "mn" == lang_output:
            f.writelines('runCommand=pkg install -y mn-libreoffice\n')
        elif "nb" == lang_output:
            f.writelines('runCommand=pkg install -y nb-libreoffice\n')
        elif "ne" == lang_output:
            f.writelines('runCommand=pkg install -y ne-libreoffice\n')
        elif "nl" == lang_output:
            f.writelines('runCommand=pkg install -y nl-libreoffice\n')
        elif "pa_IN" == lang_output:
            f.writelines('runCommand=pkg install -y pa_IN-libreoffice\n')
        elif "pl" == lang_output:
            f.writelines('runCommand=pkg install -y pl-libreoffice\n')
        elif "pt" == lang_output:
            f.writelines('runCommand=pkg install -y pt-libreoffice\n')
        elif "pt_BR" == lang_output:
            f.writelines('runCommand=pkg install -y pt_BR-libreoffice\n')
        elif "ro" == lang_output:
            f.writelines('runCommand=pkg install -y ro-libreoffice\n')
        elif "ru" == lang_output:
            f.writelines('runCommand=pkg install -y ru-libreoffice\n')
        elif "sd" == lang_output:
            f.writelines('runCommand=pkg install -y sd-libreoffice\n')
        elif "sk" == lang_output:
            f.writelines('runCommand=pkg install -y sk-libreoffice\n')
        elif "sl" == lang_output:
            f.writelines('runCommand=pkg install -y sl-libreoffice\n')
        elif "sr" == lang_output:
            f.writelines('runCommand=pkg install -y sr-libreoffice\n')
        elif "sv" == lang_output:
            f.writelines('runCommand=pkg install -y sv-libreoffice\n')
        elif "ta" == lang_output:
            f.writelines('runCommand=pkg install -y ta-libreoffice\n')
        elif "tg" == lang_output:
            f.writelines('runCommand=pkg install -y tg-libreoffice\n')
        elif "tr" == lang_output:
            f.writelines('runCommand=pkg install -y tr-libreoffice\n')
        elif "uk" == lang_output:
            f.writelines('runCommand=pkg install -y uk-libreoffice\n')
        elif "vi" == lang_output:
            f.writelines('runCommand=pkg install -y vi-libreoffice\n')
        elif "zh_CN" == lang_output:
            f.writelines('runCommand=pkg install -y zh_CN-libreoffice\n')
        elif "zh_TW" == lang_output:
            f.writelines('runCommand=pkg install -y zh_TW-libreoffice\n')
        elif "zu" == lang_output:
            f.writelines('runCommand=pkg install -y zu-libreoffice\n')
        f.close()
        os.remove(user_passwd)
        Popen(start_Install, shell=True)
