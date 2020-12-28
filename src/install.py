#!/usr/bin/env python

# install.py give the job to pc-sysinstall to install GhostBSD.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import threading
import os
from subprocess import Popen, PIPE, STDOUT, call
from time import sleep
from partition_handler import deletePartition, destroyPartition, addPartition
from create_cfg import gbsd_cfg
from slides import gbsdSlides
import sys
installer = "/usr/local/lib/gbi/"
sys.path.append(installer)
tmp = "/tmp/.gbi/"
gbi_path = "/usr/local/lib/gbi/"
sysinstall = "/usr/local/sbin/pc-sysinstall"
rcconfgbsd = "/etc/rc.conf.ghostbsd"
rcconfdbsd = "/etc/rc.conf.desktopbsd"
default_site = "/usr/local/lib/gbi/slides/welcome.html"
logo = "/usr/local/lib/gbi/logo.png"

cmd = "kenv | grep rc_system"
rc_system = Popen(cmd, shell=True, stdout=PIPE, universal_newlines=True)
if 'openrc' in rc_system.stdout.read():
    rc = 'rc-'
else:
    rc = ''


def update_progess(probar, bartext):
    new_val = probar.get_fraction() + 0.000003
    probar.set_fraction(new_val)
    probar.set_text(bartext[0:80])


def read_output(command, probar):
    GLib.idle_add(update_progess, probar, "Creating pcinstall.cfg")
    gbsd_cfg()
    sleep(1)
    if os.path.exists(tmp + 'delete'):
        GLib.idle_add(update_progess, probar, "Deleting partition")
        deletePartition()
        sleep(1)
    # destroy disk partition and create scheme
    if os.path.exists(tmp + 'destroy'):
        GLib.idle_add(update_progess, probar, "Creating disk partition")
        destroyPartition()
        sleep(1)
    # create partition
    if os.path.exists(tmp + 'create'):
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
        Popen(f'python {gbi_path}end.py', shell=True, close_fds=True)
        Gtk.main_quit()
    else:
        Popen(f'python {gbi_path}error.py', shell=True, close_fds=True)
        Gtk.main_quit()


class installSlide():

    def close_application(self, widget, event=None):
        Gtk.main_quit()

    def __init__(self):
        self.mainHbox = Gtk.HBox(False, 0)
        self.mainHbox.show()
        self.mainVbox = Gtk.VBox(False, 0)
        self.mainVbox.show()
        self.mainHbox.pack_start(self.mainVbox, True, True, 0)
        slide = gbsdSlides()
        getSlides = slide.get_slide()
        self.mainVbox.pack_start(getSlides, True, True, 0)

    def get_model(self):
        return self.mainHbox


class installProgress():

    def __init__(self):
        self.pbar = Gtk.ProgressBar()
        self.pbar.set_show_text(True)
        command = '%s -c %spcinstall.cfg' % (sysinstall, tmp)
        thr = threading.Thread(target=read_output,
                               args=(command, self.pbar))
        thr.setDaemon(True)
        thr.start()
        self.pbar.show()

    def getProgressBar(self):
        return self.pbar
