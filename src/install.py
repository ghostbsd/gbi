#!/usr/bin/env python
#
# Copyright (c) 2013 GhostBSD
#
# See COPYING for licence terms.
#
# install.py v 0.4 Sunday, February 08 2015 Eric Turgeon
#
# install.py give the job to pc-sysinstall to install GhostBSD.
from gi.repository import Gtk, GObject, GLib
import threading
import locale
import os
from subprocess import Popen, PIPE, STDOUT, call
from time import sleep
from partition_handler import rDeleteParttion, destroyParttion, makingParttion
from create_cfg import gbsd_cfg
from slides import Slides
import sys
installer = "/usr/local/lib/gbi/"
sys.path.append(installer)
# sys.path.append("/home/ericbsd/gbi/src/")
tmp = "/home/ghostbsd/.gbi/"
gbi_path = "/usr/local/lib/gbi/"
sysinstall = "/usr/local/sbin/pc-sysinstall"
rcconfgbsd = "/etc/rc.conf.ghostbsd"

GObject.threads_init()


def update_progess(probar, bartext):
    new_val = probar.get_fraction() + 0.000003
    probar.set_fraction(new_val)
    probar.set_text("%s" % bartext.rstrip())

def read_output(command, probar):
    call('service hald stop', shell=True)
    call('umount /media/GhostBSD', shell=True)
    GLib.idle_add(update_progess, probar, "Creating pcinstall.cfg")
    if os.path.exists(rcconfgbsd):
        gbsd_cfg()
        sleep(1)
    if os.path.exists(tmp + 'delete'):
        GLib.idle_add(update_progess, probar, "Deleting partition")
        rDeleteParttion()
        sleep(1)
    # destroy disk partition and create scheme
    if os.path.exists(tmp + 'destroy'):
        probar.set_fraction(0.005)
        GLib.idle_add(update_progess, probar, "Creating disk partition")
        destroyParttion()
        sleep(1)
    # create partition
    if os.path.exists(tmp + 'create'):
        probar.set_fraction(0.008)
        # probar.set_text("Creating new partitions")
        GLib.idle_add(update_progess, probar, "Creating new partitions")
        makingParttion()
        sleep(1)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
              stderr=STDOUT, close_fds=True)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        new_val = probar.get_fraction() + 0.000003
        probar.set_fraction(new_val)
        bartext = line
        GLib.idle_add(update_progess, probar, bartext)
        probar.set_text("%s" % bartext.rstrip())
        ## Those for next 4 line is for debugin only.
        # filer = open("/home/ghostbsd/.gbi/tmp", "a")
        # filer.writelines(bartext)
        # filer.close
        #print(bartext)
        # while Gtk.events_pending():
        #     Gtk.main_iteration()
    probar.set_fraction(1.0)
    call('service hald start',shell=True)
    if bartext.rstrip() == "Installation finished!":
        Popen('python %send.py' % gbi_path, shell=True, close_fds=True)
        call("rm -rf /home/ghostbsd/.gbi/", shell=True, close_fds=True)
        Gtk.main_quit()
    else:
        Popen('python %serror.py' % gbi_path, shell=True, close_fds=True)
        Gtk.main_quit()


class Installs():
    default_site = "/usr/local/lib/gbi/slides/welcome.html"

    def close_application(self, widget):
        Gtk.main_quit()

    def __init__(self, button1, button2, button3, notebook):
        # def __init__(self):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 0)
        box2.set_border_width(0)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()
        self.pbar = Gtk.ProgressBar()
        box2.pack_start(self.pbar, True, True, 10)
        slide = Slides()
        getSlides = slide.get_slide()
        # web_view = WebKit.WebView()
        # web_view.open(self.default_site)
        # sw = Gtk.ScrolledWindow()
        # sw.add(web_view)
        # sw.show()
        #box2.pack_start(getSlides, True, True, 0)
        command = '%s -c %spcinstall.cfg' % (sysinstall, tmp)
        thr = threading.Thread(target=read_output,
                               args=(command, self.pbar))
        thr.setDaemon(True)
        thr.start()
        return

    def get_model(self):
        return self.box1