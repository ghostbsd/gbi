#!/usr/bin/env python
#
# Copyright (c) 2013 GhostBSD
#
# See COPYING for licence terms.
#
# install.py v 0.4 Sunday, February 08 2015 Eric Turgeon
#
# install.py give the job to pc-sysinstall to install GhostBSD.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib
import threading
import locale
import os
from subprocess import Popen, PIPE, STDOUT, call
from time import sleep
from partition_handler import rDeleteParttion, destroyParttion, makingParttion
from create_cfg import gbsd_cfg 
from create_cfg import dbsd_cfg
from slides import gbsdSlides
from slides import dbsdSlides
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


def update_progess(probar, bartext):
    new_val = probar.get_fraction() + 0.000003
    probar.set_fraction(new_val)
    probar.set_text("Copying system to drive")


def read_output(command, probar):
    call('service hald stop', shell=True)
    GLib.idle_add(update_progess, probar, "Creating pcinstall.cfg")
    # If rc.conf.ghostbsd exists run gbsd_cfg
    if os.path.exists(rcconfgbsd):
        gbsd_cfg()
        call('umount /media/GhostBSD', shell=True)
        sleep (1)
    # If rc.conf.desktopbsd exists run dbsd_cfg
    elif os.path.exists(rcconfdbsd):
        dbsd_cfg()
        call('umount /media/DESKTOPBSD', shell=True)
        sleep (1)
    if os.path.exists(tmp + 'delete'):
        GLib.idle_add(update_progess, probar, "Deleting partition")
        rDeleteParttion()
        sleep(1)
    # destroy disk partition and create scheme
    if os.path.exists(tmp + 'destroy'):
        GLib.idle_add(update_progess, probar, "Creating disk partition")
        destroyParttion()
        sleep(1)
    # create partition
    if os.path.exists(tmp + 'create'):
        GLib.idle_add(update_progess, probar, "Creating new partitions")
        makingParttion()
        sleep(1)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
              stderr=STDOUT, close_fds=True)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        bartext = line
        GLib.idle_add(update_progess, probar, "Copying system to drive")
        # Those for next 4 line is for debugin only.
        # filer = open("/tmp/.gbi/tmp", "a")
        # filer.writelines(bartext)
        # filer.close
        # print(bartext)
    call('service hald start', shell=True)
    if bartext.rstrip() == "Installation finished!":
        Popen('python %send.py' % gbi_path, shell=True, close_fds=True)
        call("rm -rf /tmp/.gbi/", shell=True, close_fds=True)
        Gtk.main_quit()
    else:
        Popen('python %serror.py' % gbi_path, shell=True, close_fds=True)
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
