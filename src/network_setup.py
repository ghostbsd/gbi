#!/usr/bin/env python
#
# Copyright (c) 2020 GhostBSD

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import re
import sys
import _thread
from time import sleep
networkmgr = "/usr/local/share/networkmgr"
sys.path.append(networkmgr)
from net_api import (
    networkdictionary,
    connectToSsid,
    delete_ssid_wpa_supplicant_config,
    wlan_status
)

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
        print(self.network_info)
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
            for wlan_card in wlan_list:
                if self.network_info['cards'][wlan_card]['state']['connection'] == 'Connected':
                    self.wifi_connection_label.set_label('WiFi connected to an access point')
                    self.wifi_connection_image.set_from_stock(Gtk.STOCK_YES, 5)
                    break
            else:
                self.wifi_connection_label.set_label('WiFi not connected to an access point')
                self.wifi_connection_image.set_from_stock(Gtk.STOCK_NO, 5)
        else:
            wlan_card = ""
            self.wifi_detection_label.set_label('No WiFi card detected')
            self.wifi_detection_image.set_from_stock(Gtk.STOCK_NO, 5)
        if wlan_card:
            sw = Gtk.ScrolledWindow()
            sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
            sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            store = Gtk.TreeStore(str)
            for line in self.network_info['cards'][wlan_card]['info']:
                store.append(None, [line])
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
            tree_selection.connect("changed", self.wifi_setup)
            sw.add(treeView)
            self.connection_box = Gtk.HBox(homogeneous=True, spacing=20)
            self.connection_box.pack_start(sw, True, True, 50)
        else:
            self.connection_box = Gtk.HBox(homogeneous=True, spacing=20)
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
        main_grid.attach(self.connection_box, 1, 5, 10, 5)

    def wifi_setup(self, tree_selection):
        model, treeiter = tree_selection.get_selected()
        if treeiter is not None:
            value = model[treeiter][0]
            print(value)
        return

    def add_to_wpa_supplicant(self, widget, ssid_info, card):
        pwd = self.password.get_text()
        self.setup_wpa_supplicant(ssid_info[0], ssid_info, pwd, card)
        _thread.start_new_thread(
            self.try_to_connect_to_ssid,
            (ssid_info[0], ssid_info, card)
        )
        self.window.hide()

    def try_to_connect_to_ssid(self, ssid, ssid_info, card):
        if connectToSsid(ssid, card) is False:
            delete_ssid_wpa_supplicant_config(ssid)
            GLib.idle_add(self.restart_authentication, ssid_info, card)
        else:
            for _ in list(range(30)):
                if wlan_status(card) == 'associated':
                    self.updateinfo()
                    break
                sleep(1)
            else:
                delete_ssid_wpa_supplicant_config(ssid)
                GLib.idle_add(self.restart_authentication, ssid_info, card)
        return

    def restart_authentication(self, ssid_info, card):
        self.Authentication(ssid_info, card, True)

    def on_check(self, widget):
        if widget.get_active():
            self.password.set_visibility(True)
        else:
            self.password.set_visibility(False)

    def Authentication(self, ssid_info, card, failed):
        self.window = Gtk.Window()
        self.window.set_title("wi-Fi Network Authentication Required")
        self.window.set_border_width(0)
        self.window.set_size_request(500, 200)
        box1 = Gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # Creating MBR or GPT drive
        if failed:
            title = f"{ssid_info[0]} Wi-Fi Network Authentication failed"
        else:
            title = f"Authentication required by {ssid_info[0]} Wi-Fi Network"
        label = Gtk.Label(f"<b><span size='large'>{title}</span></b>")
        label.set_use_markup(True)
        pwd_label = Gtk.Label("Password:")
        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        check = Gtk.CheckButton("Show password")
        check.connect("toggled", self.on_check)
        table = Gtk.Table(1, 2, True)
        table.attach(label, 0, 5, 0, 1)
        table.attach(pwd_label, 1, 2, 2, 3)
        table.attach(self.password, 2, 4, 2, 3)
        table.attach(check, 2, 4, 3, 4)
        box2.pack_start(table, False, False, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        # Add create_scheme button
        cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        cancel.connect("clicked", self.close)
        connect = Gtk.Button(stock=Gtk.STOCK_CONNECT)
        connect.connect("clicked", self.add_to_wpa_supplicant, ssid_info, card)
        table = Gtk.Table(1, 2, True)
        table.set_col_spacings(10)
        table.attach(connect, 4, 5, 0, 1)
        table.attach(cancel, 3, 4, 0, 1)
        box2.pack_end(table, True, True, 5)
        self.window.show_all()
        return 'Done'

    def setup_wpa_supplicant(self, ssid, ssid_info, pwd, card):
        if 'RSN' in ssid_info[-1]:
            # /etc/wpa_supplicant.conf written by networkmgr
            ws = '\nnetwork={'
            ws += f'\n ssid="{ssid}"'
            ws += '\n key_mgmt=WPA-PSK'
            ws += '\n proto=RSN'
            ws += f'\n psk="{pwd}"\n'
            ws += '}\n'
        elif 'WPA' in ssid_info[-1]:
            ws = '\nnetwork={'
            ws += f'\n ssid="{ssid}"'
            ws += '\n key_mgmt=WPA-PSK'
            ws += '\n proto=WPA'
            ws += f'\n psk="{pwd}"\n'
            ws += '}\n'
        else:
            ws = '\nnetwork={'
            ws += f'\n ssid="{ssid}"'
            ws += '\n key_mgmt=NONE'
            ws += '\n wep_tx_keyidx=0'
            ws += f'\n wep_key0={pwd}\n'
            ws += '}\n'
        wsf = open("/etc/wpa_supplicant.conf", 'a')
        wsf.writelines(ws)
        wsf.close()

    def Open_Wpa_Supplicant(self, ssid, card):
        ws = '\nnetwork={'
        ws += f'\n ssid={ssid}'
        ws += '\n key_mgmt=NONE\n}\n'
        wsf = open("/etc/wpa_supplicant.conf", 'a')
        wsf.writelines(ws)
        wsf.close()
