#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
# from glob import glob
from setuptools import setup

# import DistUtilsExtra.command.build_extra
# import DistUtilsExtra.command.build_i18n
# import DistUtilsExtra.command.clean_i18n

# to update i18n .mo files (and merge .pot file into .po files) run on Linux:
# ,,python setup.py build_i18n -m''

# silence pyflakes, __VERSION__ is properly assigned below...
__VERSION__ = '5.9'
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
    ('{prefix}/share/applications'.format(prefix=sys.prefix),
     ['src/gbi.desktop']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/install.png']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/logo.png']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/create_cfg.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/end.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/error.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/gbiWindow.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/ghostbsd-style.css']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix),
     ['src/desktopbsd-style.css']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/install.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/installType.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/keyboard.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/language.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/partition.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix),
     ['src/partition_handler.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/root.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/slides.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/sys_handler.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/timezone.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/use_ufs.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/use_zfs.py']),
    ('{prefix}/lib/gbi'.format(prefix=sys.prefix), ['src/addUser.py']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-laptop.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-nics.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-sheme.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-vmware.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/detect-wifi.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/disk-info.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/disk-label.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/disk-list.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/disk-part.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/enable-net.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/list-components.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/list-rsync-backups.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/list-tzones.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/query-langs.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/send-logs.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/setup-ssh-keys.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/sys-mem.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/test-live.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/test-netup.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/update-part-list.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/xkeyboard-layouts.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/xkeyboard-models.sh']),
    ('{prefix}/lib/gbi/backend-query'.format(prefix=sys.prefix), ['src/backend-query/xkeyboard-variants.sh']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/D-logo.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/browser.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/customize.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/email.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/help.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/music.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/office.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/photo.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/social.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/software.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/videos.png']),
    ('{prefix}/lib/gbi/slide-images/desktopbsd'.format(prefix=sys.prefix), ['src/slide-images/desktopbsd/welcome.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/browser.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/customize.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/email.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/help.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/G-logo.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/music.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/office.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/photo.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/social.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/software.png']),
    ('{prefix}/lib/gbi/slide-images/ghostbsd'.format(prefix=sys.prefix), ['src/slide-images/ghostbsd/welcome.png']),
]

data_files.extend(datafilelist('{prefix}/share/locale'.format(prefix=sys.prefix), 'build/mo'))

# cmdclass ={
#             "build" : DistUtilsExtra.command.build_extra.build_extra,
#             "build_i18n" :  DistUtilsExtra.command.build_i18n.build_i18n,
#             "clean": DistUtilsExtra.command.clean_i18n.clean_i18n,
# }

setup(name="gbi",
      version=PROGRAM_VERSION,
      description="GBI is a GTK front end user interface for pc-sysinstall",
      license='BSD',
      author='Eric Turgeon',
      url='https://github/GhostBSD/gbi/',
      package_dir={'': '.'},
      data_files=data_files,
      # install_requires = [ 'setuptools', ],
      scripts=['gbi'],)
# cmdclass = cmdclass,
