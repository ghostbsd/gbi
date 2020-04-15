#!/usr/bin/env python3.7

from subprocess import Popen, PIPE

pc_sysinstall = '/usr/local/sbin/pc-sysinstall'

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
