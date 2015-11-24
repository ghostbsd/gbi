#!/usr/bin/env python
#
# Copyright (c) 2013 GhostBSD
#
# See COPYING for licence terms.
#
# install.py v 0.4 Sunday, February 08 2015 Eric Turgeon
#
# install.py give the job to pc-sysinstall to install GhostBSD.
from gi.repository import Gtk, GObject
from gi.repository import WebKit
import threading
import locale
import os
from subprocess import Popen, PIPE, STDOUT, call
from time import sleep
from partition_handler import rDeleteParttion, destroyParttion, makingParttion
from create_cfg import cfg_data

tmp = "/home/ghostbsd/.gbi/"
gbi_path = "/usr/local/lib/gbi/"
sysinstall = "/usr/local/sbin/pc-sysinstall"

encoding = locale.getpreferredencoding()
utf8conv = lambda x: str(x, encoding).encode('utf8')
threadBreak = False
GObject.threads_init()


def close_application(self, widget):
    Gtk.main_quit()


def read_output(command, probar):
    call('service hald stop', shell=True)
    call('umount /media/GhostBSD', shell=True)
    probar.set_fraction(0.004)
    probar.set_text("Creating pcinstall.cfg")
    cfg_data()
    probar.set_text("Partition table Configuration")
    sleep(2)
    if os.path.exists(tmp + 'delete'):
        probar.set_fraction(0.004)
        probar.set_text("Deleting partition")
        rDeleteParttion()
        sleep(2)
    # destroy disk partition and create scheme
    if os.path.exists(tmp + 'destroy'):
        probar.set_fraction(0.005)
        probar.set_text("Creating new disk with partitions")
        destroyParttion()
        sleep(2)
    # create partition
    if os.path.exists(tmp + 'create'):
        probar.set_fraction(0.008)
        probar.set_text("Creating new partitions")
        makingParttion()
        sleep(2)
    probar.set_text("Beginning installation")
    sleep(2)
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
              stderr=STDOUT, close_fds=True)
    while 1:
        line = p.stdout.readline()
        if not line:
            break
        new_val = probar.get_fraction() + 0.000003
        probar.set_fraction(new_val)
        bartext = line
        probar.set_text("%s" % bartext.rstrip())
        ## Those for next 4 line is for debugin only.
        # filer = open("/home/ghostbsd/.gbi/tmp", "a")
        # filer.writelines(bartext)
        # filer.close
        print(bartext)
    probar.set_fraction(1.0)
    call('service hald start',shell=True)
    if bartext.rstrip() == "Installation finished!":
        call('python %send.py' % gbi_path, shell=True, close_fds=True)
        call("rm -rf /home/ghostbsd/.gbi/", shell=True, close_fds=True)
        #GObject.idle_add(window.destroy)
    else:
        call('python %serror.py' % gbi_path, shell=True, close_fds=True)
        #GObject.idle_add(window.destroy)


class Installs():
    default_site = "/usr/local/lib/gbi/slides/welcome.html"

    def close_application(self, widget):
        Gtk.main_quit()

    def __init__(self, button1, button2, button3, notebook):
        self.box1 = Gtk.VBox(False, 0)
        self.box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        self.box1.pack_start(box2, True, True, 0)
        box2.show()
        self.pbar = Gtk.ProgressBar()
        self.pbar.set_fraction(0.0)
        self.pbar.set_size_request(-1, 20)
        box2.pack_start(self.pbar, False, False, 0)
        web_view = WebKit.WebView()
        web_view.open(self.default_site)
        sw = Gtk.ScrolledWindow()
        sw.add(web_view)
        sw.show()
        box2.pack_start(sw, True, True, 0)
        command = '%s -c %spcinstall.cfg' % (sysinstall, tmp)
        # This is only for testing
        # command = 'cd /usr/ports/editors/openoffice-4 && make install clean'
        thr = threading.Thread(target=read_output,
                               args=(command, self.pbar))
        thr.setDaemon(True)
        thr.start()
        return

    def get_model(self):
        return self.box1