#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 by Mike Gabriel <mike.gabriel@das-netzwerkteam.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.

import os
import sys

from glob import glob

from setuptools import setup

# import DistUtilsExtra.command.build_extra
# import DistUtilsExtra.command.build_i18n
# import DistUtilsExtra.command.clean_i18n

# to update i18n .mo files (and merge .pot file into .po files) run on Linux:
# ,,python setup.py build_i18n -m''

# silence pyflakes, __VERSION__ is properly assigned below...
__VERSION__ = '3.0'
# for line in file('networkmgr').readlines():
#    if (line.startswith('__VERSION__')):
#        exec(line.strip())
PROGRAM_VERSION = __VERSION__

def datafilelist(installbase, sourcebase):
    datafileList = []
    for root, subFolders, files in os.walk(sourcebase):
        fileList = []
        for f in files:
            fileList.append(os.path.join(root, f))
        datafileList.append((root.replace(sourcebase, installbase), fileList))
    return datafileList
# '{prefix}/share/man/man1'.format(prefix=sys.prefix), glob('data/*.1')),
data_files = [
    ('{prefix}/share/applications'.format(prefix=sys.prefix), ['src/gbi.desktop',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/install.png',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/logo.png',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/create_cfg.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/end.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/error.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/gbiWindow.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/install.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/installType.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/keyboard.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/language.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/partition.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/partition_handler.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/root.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/timezone.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/use_disk.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/use_zfs.py',]),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/user.py',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-laptop.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-nics.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-sheme.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-vmware.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-wifi.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/disk-info.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/disk-label.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/disk-list.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/disk-part.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/enable-net.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/list-components.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/list-rsync-backups.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/list-tzones.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/query-langs.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/send-logs.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/setup-ssh-keys.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/sys-mem.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/test-live.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/test-netup.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/update-part-list.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/xkeyboard-layouts.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/xkeyboard-models.sh',]),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/xkeyboard-variants.sh',]),
    ('{prefix}/lib/gbi/keyboard'.format(prefix=sys.prefix), ['src/keyboard/layout',]),
    ('{prefix}/lib/gbi/keyboard'.format(prefix=sys.prefix), ['src/keyboard/model',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/af',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/am',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ara',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/at',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/az',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ba',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/bd',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/be',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/bg',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/br',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/brai',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/by',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ca',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ch',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/cn',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/cz',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/de',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/dk',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ee',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/epo',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/es',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/fi',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/fo',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/fr',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/gb',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ge',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/gh',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/gr',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/hr',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/hu',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ie',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/il',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/in',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/iq',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ir',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/is',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/it',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/jp',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ke',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/kg',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/kz',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/latam',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/lk',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/lt',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/lv',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ma',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/me',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/mk',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ml',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/mt',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ng',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/nl',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/no',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ph',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/pk',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/pl',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/pt',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ro',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/rs',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ru',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/se',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/si',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/sk',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/sy',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/th',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/tj',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/tm',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/tr',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/ua',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/us',]),
    ('{prefix}/lib/gbi/keyboard/variant'.format(prefix=sys.prefix), ['src/keyboard/variant/uz',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/accessibility.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/browse.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/chat.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/gethelp.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/index.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/music.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/office.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/photos.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/privacy.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/software.html',]),
    ('{prefix}/lib/gbi/slides'.format(prefix=sys.prefix), ['src/slides/welcome.html',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/access.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/chromium.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/empathy.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/evolution.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/facebook.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/firefox.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/flash.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/gimp.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/gwibber.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/identica.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/inkscape.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/languages.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/libreoffice-calc.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/libreoffice-impress.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/libreoffice-writer.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/media-player-banshee.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/movieplayer.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/pidgin.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/pitivi.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/rhythmbox.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/shotwell.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/skype.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/stellarium.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/themes.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/thunderbird.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/tomboy.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/twitter.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/ubuntuone.png',]),
    ('{prefix}/lib/gbi/slides/icons'.format(prefix=sys.prefix), ['src/slides/icons/xchat.png',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/Untitled.xcf',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/arrow-back.png',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/arrow-next.png',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/background.png',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/base.css',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/bullet-point.png',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/twitter-bird-16.png',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/twitter-logo-16.png',]),
    ('{prefix}/lib/gbi/slides/link'.format(prefix=sys.prefix), ['src/slides/link/twitter.js',]),
    ('{prefix}/lib/gbi/slides/link-core'.format(prefix=sys.prefix), ['src/slides/link-core/base.js',]),
    ('{prefix}/lib/gbi/slides/link-core'.format(prefix=sys.prefix), ['src/slides/link-core/jquery.cycle.all.js',]),
    ('{prefix}/lib/gbi/slides/link-core'.format(prefix=sys.prefix), ['src/slides/link-core/jquery.js',]),
    ('{prefix}/lib/gbi/slides/link-core'.format(prefix=sys.prefix), ['src/slides/link-core/slideshow.js',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/browse.jpg',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/customize.jpg',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/music.jpg',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/office.jpg',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/photos.jpg',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/pkgng.jpg',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/social.jpg',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/ubuntuone.jpg',]),
    ('{prefix}/lib/gbi/slides/screenshots'.format(prefix=sys.prefix), ['src/slides/screenshots/welcome.jpg',]),
    ('{prefix}/lib/gbi/timezone'.format(prefix=sys.prefix), ['src/timezone/continent',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Africa',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/America',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Antarctica',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Arctic',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Asia',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Atlantic',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Australia',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Europe',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Indian',]),
    ('{prefix}/lib/gbi/timezone/city'.format(prefix=sys.prefix), ['src/timezone/city/Pacific',]),
]
data_files.extend(datafilelist('{prefix}/share/locale'.format(prefix=sys.prefix), 'build/mo'))

# cmdclass ={
#             "build" : DistUtilsExtra.command.build_extra.build_extra,
#             "build_i18n" :  DistUtilsExtra.command.build_i18n.build_i18n,
#             "clean": DistUtilsExtra.command.clean_i18n.clean_i18n,
# }

setup(
    name = "gbi",
    version = PROGRAM_VERSION,
    description = "GBI is the GhostBSD front end user interface for pc-sysinstall",
    license = 'BSD',
    author = 'Eric Turgeon',
    url = 'https://github/GhostBSD/gbi/',
    package_dir = {'': '.'},
    data_files = data_files,
    # install_requires = [ 'setuptools', ],
    scripts = ['gbi'],
)
# cmdclass = cmdclass,