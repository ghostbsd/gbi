#!/usr/bin/env python

import re
import os
from subprocess import Popen, run, PIPE

pc_sysinstall = '/usr/local/sbin/pc-sysinstall'


def replace_patern(current, new, file):
    parser_file = open(file, 'r').read()
    parser_patched = re.sub(current, new, parser_file)
    save_parser_file = open(file, 'w')
    save_parser_file.writelines(parser_patched)
    save_parser_file.close()


def language_dictionary():
    langs = Popen(f'{pc_sysinstall} query-langs', shell=True, stdin=PIPE,
                  stdout=PIPE, universal_newlines=True,
                  close_fds=True).stdout.readlines()
    dictionary = {}
    for line in langs:
        lang_list = line.rstrip()
        lang_name = lang_list.partition(' ')[2]
        lang_code = lang_list.partition(' ')[0]
        dictionary[lang_name] = lang_code
    return dictionary


def localize_system(locale):
    slick_greeter = "/usr/local/share/xgreeters/slick-greeter.desktop"
    gtk_greeter = "/usr/local/share/xgreeters/lightdm-gtk-greeter.desktop"
    replace_patern('lang=C', f'lang={locale}', '/etc/login.conf')
    replace_patern('en_US', locale, '/etc/profile')
    replace_patern('en_US', locale, '/usr/share/skel/dot.profile')

    if os.path.exists(slick_greeter):
        replace_patern(
            'Exec=slick-greeter',
            f'Exec=env LANG={locale}.UTF-8 slick-greeter',
            slick_greeter
        )
    elif os.path.exists(gtk_greeter):
        replace_patern(
            'Exec=lightdm-gtk-greete',
            f'Exec=env LANG={locale}.UTF-8 lightdm-gtk-greeter',
            gtk_greeter
        )


def keyboard_dictionary():
    xkeyboard_layouts = Popen(f'{pc_sysinstall} xkeyboard-layouts', shell=True,
                              stdout=PIPE,
                              universal_newlines=True).stdout.readlines()
    dictionary = {}
    for line in xkeyboard_layouts:
        keyboard_list = list(filter(None, line.rstrip().split('  ')))
        kb_name = keyboard_list[1].strip()
        kb_layouts = keyboard_list[0].strip()
        kb_variant = None
        dictionary[kb_name] = {'layout': kb_layouts, 'variant': kb_variant}

    xkeyboard_variants = Popen(f'{pc_sysinstall} xkeyboard-variants',
                               shell=True, stdout=PIPE,
                               universal_newlines=True).stdout.readlines()
    for line in xkeyboard_variants:
        xkb_variant = line.rstrip()
        kb_name = xkb_variant.partition(':')[2].strip()
        keyboard_list = list(filter
                             (None, xkb_variant.partition(':')[0].split()))
        kb_layouts = keyboard_list[1].strip()
        kb_variant = keyboard_list[0].strip()
        dictionary[kb_name] = {'layout': kb_layouts, 'variant': kb_variant}
    return dictionary


def keyboard_models():
    xkeyboard_models = Popen(f'{pc_sysinstall} xkeyboard-models', shell=True,
                             stdout=PIPE,
                             universal_newlines=True).stdout.readlines()
    dictionary = {}
    for line in xkeyboard_models:
        kbm_name = line.rstrip().partition(' ')[2]
        kbm_code = line.rstrip().partition(' ')[0]
        dictionary[kbm_name] = kbm_code
    return dictionary


def change_keyboard(kb_layout, kb_variant=None, kb_model=None):
    if kb_variant is None and kb_model is not None:
        run(f"setxkbmap -layout {kb_layout} -model {kb_model}", shell=True)
    elif kb_variant is not None and kb_model is None:
        run(f"setxkbmap -layout {kb_layout} -variant {kb_variant}", shell=True)
    elif kb_variant is not None and kb_model is not None:
        set_kb_cmd = f"setxkbmap -layout {kb_layout} -variant {kb_variant} " \
            f"-model {kb_model}"
        run(set_kb_cmd, shell=True)
    else:
        run(f"setxkbmap -layout {kb_layout}", shell=True)


def set_keyboard(kb_layout, kb_variant=None, kb_model=None):
    pass


def timezone_dictionary():
    tz_list = Popen(f'{pc_sysinstall} list-tzones', shell=True,
                    stdout=PIPE, universal_newlines=True).stdout.readlines()
    city_list = []
    dictionary = {}
    last_continent = ''
    for zone in tz_list:
        zone_list = zone.partition(':')[0].rstrip().split('/')
        continent = zone_list[0]
        if continent != last_continent:
            city_list = []
        if len(zone_list) == 3:
            city = zone_list[1] + '/' + zone_list[2]
        elif len(zone_list) == 4:
            city = zone_list[1] + '/' + zone_list[2] + '/' + zone_list[3]
        else:
            city = zone_list[1]
        city_list.append(city)
        dictionary[continent] = city_list
        last_continent = continent
    return dictionary


def set_addmin_user(username, name, password, shell, homedir, hostname):
    # Set Root user
    run(f"echo '{password}' | pw usermod -n root -h 0", shell=True)
    cmd = f"echo '{password}' | pw useradd {username} -c {name} -h 0" \
        f" -s {shell} -m -d {homedir} -g wheel,operator"
    run(cmd, shell=True)
    run(f"sysrc hostname={hostname}", shell=True)
    run(f"hostname {hostname}", shell=True)
