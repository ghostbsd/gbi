#!/usr/bin/env python
#
# Copyright (c) 2020 GhostBSD

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import sys
import os
import re
networkmgr = "/usr/local/share/networkmgr"
sys.path.append(networkmgr)
from net_api import networkdictionary

os.system("netcardmgr")
logo = "/usr/local/lib/gbi/logo.png"

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class network_setup():

    def get_model(self):
        return self.vbox1

    def __init__(self):
        self.network_info = networkdictionary()
        self.vbox1 = Gtk.VBox(homogeneous=False, spacing=0)
        self.vbox1.show()
        Title = Gtk.Label(label='Network Setup', name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        card_list = list(self.network_info['cards'].keys())
        r = re.compile("wlan")
        wlan_list = list(filter(r.match, card_list))
        wire_list = list(set(card_list).difference(wlan_list))

        self.wire_detection_label = Gtk.Label()
        self.wire_detection_image = Gtk.Image()
        self.wire_detection_label.set_xalign(0.01)
        self.wire_connection_label = Gtk.Label()
        self.wire_connection_label.set_xalign(0.01)
        self.wire_connection_image = Gtk.Image()
        if wire_list:
            self.wire_detection_label.set_label('Network internet card detected')
            self.wire_detection_image.set_from_stock(Gtk.STOCK_YES, 5)
            for card in wire_list:
                if self.network_info['cards'][card]['state']['connection'] == 'Connected':
                    self.wire_connection_label.set_label('Network card connected to the internet')
                    self.wire_connection_image.set_from_stock(Gtk.STOCK_YES, 5)
                    break
            else:
                self.wire_connection_label.set_label('Network card connected to the internet')
                self.wire_connection_image.set_from_stock(Gtk.STOCK_NO, 5)
        else:
            self.wire_detection_label.set_label('No network card detected')
            self.wire_detection_image.set_from_stock(Gtk.STOCK_NO, 5)

        self.wifi_detection_label = Gtk.Label()
        self.wifi_detection_label.set_xalign(0.01)
        self.wifi_detection_image = Gtk.Image()
        self.wifi_connection_label = Gtk.Label()
        self.wifi_connection_label.set_xalign(0.01)
        self.wifi_connection_image = Gtk.Image()

        if wlan_list:
            self.wifi_detection_label.set_label('WiFi card detected')
            self.wifi_detection_image.set_from_stock(Gtk.STOCK_YES, 5)
            self.wifi_connection_label.set_label('WiFi connected to the internet')
            self.wifi_connection_image.set_from_stock(Gtk.STOCK_YES, 5)
        else:
            self.wifi_detection_label.set_label('No WiFi card detected')
            self.wifi_detection_image.set_from_stock(Gtk.STOCK_NO, 5)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        store = Gtk.TreeStore(str)
        # for line in lang_dictionary:
        #     store.append(None, [line])
        treeView = Gtk.TreeView(store)
        treeView.set_model(store)
        treeView.set_rules_hint(True)
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label(label='WiFi Network Detected')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        # tree_selection.connect("changed", self.Language_Selection)
        sw.add(treeView)
        sw.hide()
        self.hbox1 = Gtk.HBox(homogeneous=True, spacing=20)
        self.hbox1.hide()
        self.hbox1.pack_start(sw, True, True, 50)
        main_grid = Gtk.Grid()
        main_grid.set_row_spacing(10)
        main_grid.set_column_spacing(10)
        main_grid.set_column_homogeneous(True)
        main_grid.set_row_homogeneous(True)
        self.vbox1.pack_start(main_grid, True, True, 10)
        main_grid.attach(self.wire_detection_image, 2, 1, 1, 1)
        main_grid.attach(self.wire_detection_label, 3, 1, 8, 1)
        main_grid.attach(self.wire_connection_image, 2, 2, 1, 1)
        main_grid.attach(self.wire_connection_label, 3, 2, 8, 1)
        main_grid.attach(self.wifi_detection_image, 2, 3, 1, 1)
        main_grid.attach(self.wifi_detection_label, 3, 3, 8, 1)
        main_grid.attach(self.wifi_connection_image, 2, 4, 1, 1)
        main_grid.attach(self.wifi_connection_label, 3, 4, 8, 1)
        main_grid.attach(self.hbox1, 1, 5, 10, 5)
