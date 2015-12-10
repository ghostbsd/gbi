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
tmp = "/home/ghostbsd/.gbi/"
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
KBFile= '%skeyboard' % tmp
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
            # f.writelines('enableNTP=yes\n')
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
            #os.remove(zfs_config)
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
        f.writelines('runCommand=echo \'gdm_lang="%s.UTF-8"\' >> /etc/rc.conf\n' % lang_output)
        if "af" == lang_output:
            f.writelines('runCommand=pkg install af-libreoffice')
        elif "ar" == lang_output:
            f.writelines('runCommand=pkg install ar-libreoffice')
        elif "bg" == lang_output:
            f.writelines('runCommand=pkg install bg-libreoffice')
        elif "bn" == lang_output:
            f.writelines('runCommand=pkg install bn-libreoffice')
        elif "br" == lang_output:
            f.writelines('runCommand=pkg install br-libreoffice')
        elif "bs" == lang_output:
            f.writelines('runCommand=pkg install bs-libreoffice')
        elif "ca" == lang_output:
            f.writelines('runCommand=pkg install ca-libreoffice')
        elif "cs" == lang_output:
            f.writelines('runCommand=pkg install cs-libreoffice')
        elif "cy" == lang_output:
            f.writelines('runCommand=pkg install cy-libreoffice')
        elif "da" == lang_output:
            f.writelines('runCommand=pkg install da-libreoffice')
        elif "de" == lang_output:
            f.writelines('runCommand=pkg install de-libreoffice')
        elif "el" == lang_output:
            f.writelines('runCommand=pkg install el-libreoffice')
        elif "en_GB" == lang_output:
            f.writelines('runCommand=pkg install en_GB-libreoffice')
        elif "en_ZA" == lang_output:
            f.writelines('runCommand=pkg install en_ZA-libreoffice')
        elif "es" == lang_output:
            f.writelines('runCommand=pkg install es-libreoffice')
        elif "et" == lang_output:
            f.writelines('runCommand=pkg install et-libreoffice')
        elif "eu" == lang_output:
            f.writelines('runCommand=pkg install eu-libreoffice')
        elif "fa" == lang_output:
            f.writelines('runCommand=pkg install fa-libreoffice')
        elif "fi" == lang_output:
            f.writelines('runCommand=pkg install fi-libreoffice')
        elif "fr" in lang_output:
            f.writelines('runCommand=pkg install fr-libreoffice')
        elif "ga" == lang_output:
            f.writelines('runCommand=pkg install ga-libreoffice')
        elif "gb" == lang_output:
            f.writelines('runCommand=pkg install gd-libreoffice')
        elif "gl" == lang_output:
            f.writelines('runCommand=pkg install gl-libreoffice')
        elif "he" == lang_output:
            f.writelines('runCommand=pkg install he-libreoffice')
        elif "hi" == lang_output:
            f.writelines('runCommand=pkg install hi-libreoffice')
        elif "hr" == lang_output:
            f.writelines('runCommand=pkg install hr-libreoffice')
        elif "hu" == lang_output:
            f.writelines('runCommand=pkg install hu-libreoffice')
        elif "id" == lang_output:
            f.writelines('runCommand=pkg install id-libreoffice')
        elif "is" == lang_output:
            f.writelines('runCommand=pkg install is-libreoffice')
        elif "it" == lang_output:
            f.writelines('runCommand=pkg install it-libreoffice')
        elif "ja" == lang_output:
            f.writelines('runCommand=pkg install ja-libreoffice')
        elif "ko" == lang_output:
            f.writelines('runCommand=pkg install ko-libreoffice')
        elif "lt" == lang_output:
            f.writelines('runCommand=pkg install lt-libreoffice')
        elif "lv" == lang_output:
            f.writelines('runCommand=pkg install lv-libreoffice')
        elif "mk" == lang_output:
            f.writelines('runCommand=pkg install mk-libreoffice')
        elif "mn" == lang_output:
            f.writelines('runCommand=pkg install mn-libreoffice')
        elif "nb" == lang_output:
            f.writelines('runCommand=pkg install nb-libreoffice')
        elif "ne" == lang_output:
            f.writelines('runCommand=pkg install ne-libreoffice')
        elif "nl" == lang_output:
            f.writelines('runCommand=pkg install nl-libreoffice')
        elif "pa_IN" == lang_output:
            f.writelines('runCommand=pkg install pa_IN-libreoffice')
        elif "pl" == lang_output:
            f.writelines('runCommand=pkg install pl-libreoffice')
        elif "pt" == lang_output:
            f.writelines('runCommand=pkg install pt-libreoffice')
        elif "pt_BR" == lang_output:
            f.writelines('runCommand=pkg install pt_BR-libreoffice')
        elif "ro" == lang_output:
            f.writelines('runCommand=pkg install ro-libreoffice')
        elif "ru" == lang_output:
            f.writelines('runCommand=pkg install ru-libreoffice')
        elif "sd" == lang_output:
            f.writelines('runCommand=pkg install sd-libreoffice')
        elif "sk" == lang_output:
            f.writelines('runCommand=pkg install sk-libreoffice')
        elif "sl" == lang_output:
            f.writelines('runCommand=pkg install sl-libreoffice')
        elif "sr" == lang_output:
            f.writelines('runCommand=pkg install sr-libreoffice')
        elif "sv" == lang_output:
            f.writelines('runCommand=pkg install sv-libreoffice')
        elif "ta" == lang_output:
            f.writelines('runCommand=pkg install ta-libreoffice')
        elif "tg" == lang_output:
            f.writelines('runCommand=pkg install tg-libreoffice')
        elif "tr" == lang_output:
            f.writelines('runCommand=pkg install tr-libreoffice')
        elif "uk" == lang_output:
            f.writelines('runCommand=pkg install uk-libreoffice')
        elif "vi" == lang_output:
            f.writelines('runCommand=pkg install vi-libreoffice')
        elif "zh_CN" == lang_output:
            f.writelines('runCommand=pkg install zh_CN-libreoffice')
        elif "zh_TW" == lang_output:
            f.writelines('runCommand=pkg install zh_TW-libreoffice')
        elif "zu" == lang_output:
            f.writelines('runCommand=pkg install zu-libreoffice')
        f.close()
        os.remove(user_passwd)
        Popen(start_Install, shell=True)
