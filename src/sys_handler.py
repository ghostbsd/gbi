#!/usr/bin/env python

from subprocess import Popen, PIPE


def timezone_dictionary():
    tz_list = Popen('pc-sysinstall list-tzones', shell=True,
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
