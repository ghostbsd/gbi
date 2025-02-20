#!/usr/bin/env python

# install.py give the job to pc-sysinstall to install GhostBSD.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import threading
import os
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from partition_handler import deletePartition, destroyPartition, addPartition
from create_cfg import GhostBSDCfg
import sys

gbi_dir = "/usr/local/lib/gbi"
sys.path.append(gbi_dir)
gbi_tmp = "/tmp/.gbi"
pc_sysinstall = "/usr/local/sbin/pc-sysinstall"


cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


def update_progess(probar, bartext):
    new_val = probar.get_fraction() + 0.000003
    probar.set_fraction(new_val)
    probar.set_text(bartext[0:80])


def read_output(command, probar, main_window):
    GLib.idle_add(update_progess, probar, "Creating pcinstall.cfg")
    GhostBSDCfg()
    sleep(1)
    if os.path.exists(f'{gbi_tmp}/delete'):
        GLib.idle_add(update_progess, probar, "Deleting partition")
        deletePartition()
        sleep(1)
    # destroy disk partition and create scheme
    if os.path.exists(f'{gbi_tmp}/destroy'):
        GLib.idle_add(update_progess, probar, "Creating disk partition")
        destroyPartition()
        sleep(1)
    # create partition
    if os.path.exists(f'{gbi_tmp}/create'):
        GLib.idle_add(update_progess, probar, "Creating new partitions")
        addPartition()
        sleep(1)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
              stderr=STDOUT, close_fds=True, universal_newlines=True)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        bartext = line.rstrip()
        GLib.idle_add(update_progess, probar, bartext)
        # Those for next 4 line is for debugin only.
        # filer = open("/tmp/.gbi/tmp", "a")
        # filer.writelines(bartext)
        # filer.close
        print(bartext)
    if bartext.rstrip() == "Installation finished!":
        Popen(f'python {gbi_dir}/end.py', shell=True, close_fds=True)
    else:
        Popen(f'python {gbi_dir}/error.py', shell=True, close_fds=True)
    main_window.hide()


class installWindow():

    def close_application(self, widget, event=None):
        Gtk.main_quit()

    def __init__(self):
        self.vBox = Gtk.VBox(False, 0)
        self.vBox.show()
        label = Gtk.Label("Installation in progress", name="Header")
        label.set_property("height-request", 50)
        self.vBox.pack_start(label, False, False, 0)

        hBox = Gtk.HBox(False, 0, name="install")
        hBox.show()
        self.vBox.pack_end(hBox, True, True, 0)
        vBox2 = Gtk.VBox(False, 0)
        vBox2.show()
        label2 = Gtk.Label(name="sideText")

        label2.set_markup("Thank you for choosing GhostBSD!\n\n"
                          "We believe every computer operating system should "
                          "be simple, elegant, secure and protect your privacy"
                          " while being easy to use. GhostBSD is simplifying "
                          "FreeBSD for those who lack the technical expertise "
                          "required to use it and lower the entry-level of "
                          "using BSD. \n\nWe hope you'll enjoy our BSD "
                          "operating system.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        # label2.set_max_width_chars(10)
        label2.set_alignment(0.0, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)

        image = Gtk.Image()
        image.set_from_file(f"{gbi_dir}/image/G_logo.gif")
        # image.set_size_request(width=256, height=256)
        image.show()
        hBox.pack_end(image, True, True, 20)

    def get_model(self):
        return self.vBox


class installProgress():

    def __init__(self, main_window):
        self.pbar = Gtk.ProgressBar()
        self.pbar.set_show_text(True)
        command = f'sudo {pc_sysinstall} -c {gbi_tmp}/pcinstall.cfg'
        thr = threading.Thread(
            target=read_output,
            args=(
                command,
                self.pbar,
                main_window
            )
        )
        thr.setDaemon(True)
        thr.start()
        self.pbar.show()

    def getProgressBar(self):
        return self.pbar
