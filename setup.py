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
__VERSION__ = '10.6'
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


prefix = sys.prefix

lib_gbi = [
    'src/boot_manager.py',
    'src/create_cfg.py',
    'src/end.py',
    'src/error.py',
    'src/gbiWindow.py',
    'src/gbi_common.py',
    'src/ghostbsd-style.css',
    'src/install.py',
    'src/installType.py',
    'src/keyboard.py',
    'src/language.py',
    'src/partition.py',
    'src/partition_handler.py',
    'src/setup_system.py',
    'src/sys_handler.py',
    'src/timezone.py',
    'src/use_ufs.py',
    'src/use_zfs.py',
    'src/add_admin.py',
    'src/add_users.py',
    'src/welcome_live.py',
    'src/network_setup.py',
    'src/disk.png',
    'src/laptop.png'
]

lib_gbi_image = [
    'src/image/G_logo.gif',
    'src/image/install-gbsd.png',
    'src/image/logo.png',
    'src/image/disk.png',
    'src/image/laptop.png',
    'src/image/installation.jpg'
]

lib_gbi_backend_query = [
    'src/backend-query/detect-laptop.sh',
    'src/backend-query/detect-nics.sh',
    'src/backend-query/detect-sheme.sh',
    'src/backend-query/detect-vmware.sh',
    'src/backend-query/detect-wifi.sh',
    'src/backend-query/disk-info.sh',
    'src/backend-query/disk-label.sh',
    'src/backend-query/disk-list.sh',
    'src/backend-query/disk-part.sh',
    'src/backend-query/enable-net.sh',
    'src/backend-query/list-components.sh',
    'src/backend-query/list-rsync-backups.sh',
    'src/backend-query/list-tzones.sh',
    'src/backend-query/query-langs.sh',
    'src/backend-query/send-logs.sh',
    'src/backend-query/setup-ssh-keys.sh',
    'src/backend-query/sys-mem.sh',
    'src/backend-query/test-live.sh',
    'src/backend-query/test-netup.sh',
    'src/backend-query/update-part-list.sh',
    'src/backend-query/xkeyboard-layouts.sh',
    'src/backend-query/xkeyboard-models.sh',
    'src/backend-query/xkeyboard-variants.sh'
]

data_files = [
    (f'{prefix}/share/applications', ['src/gbi.desktop']),
    (f'{prefix}/lib/gbi', lib_gbi),
    (f'{prefix}/lib/gbi/backend-query', lib_gbi_backend_query),
    (f'{prefix}/lib/gbi/image', lib_gbi_image)
]

data_files.extend(datafilelist(f'{prefix}/share/locale', 'build/mo'))

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
