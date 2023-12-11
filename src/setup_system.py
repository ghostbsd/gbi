#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import threading
from time import sleep

gbi_dir = "/usr/local/lib/gbi"
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


def read_output(command, probar, main_window, welcome, kb, tz, adminuser):
    GLib.idle_add(update_progess, probar, "Setting system language")
    welcome.save_language()
    sleep(1)
    GLib.idle_add(update_progess, probar, "Setting system language")
    kb.save_keyboard()
    sleep(1)
    GLib.idle_add(update_progess, probar, "Setting system language")
    tz.save_timezone()
    sleep(1)
    GLib.idle_add(update_progess, probar, "Setting system language")
    adminuser.save_adminuser()
    sleep(1)
    GLib.idle_add(update_progess, probar, "Setting system language")

    # main_window.hide()


class setup_window():

    def close_application(self, widget, event=None):
        Gtk.main_quit()

    def __init__(self):
        self.vBox = Gtk.VBox(False, 0)
        self.vBox.show()
        label = Gtk.Label(label="Getting everything ready", name="Header")
        label.set_property("height-request", 50)
        self.vBox.pack_start(label, False, False, 0)

        hBox = Gtk.HBox(False, 0, name="install")
        hBox.show()
        self.vBox.pack_end(hBox, True, True, 0)
        vBox2 = Gtk.VBox(False, 0)
        vBox2.show()
        label2 = Gtk.Label(name="sideText")

        label2.set_markup(
            "This should not take too long.\n\n"
            "Don't turn your system off."
        )
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        # label2.set_max_width_chars(10)
        label2.set_alignment(0.5, 0.4)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 0)

        image = Gtk.Image()
        image.set_from_file(f"{gbi_dir}/image/G_logo.gif")
        # image.set_size_request(width=256, height=256)
        image.show()
        hBox.pack_end(image, True, True, 20)

    def get_model(self):
        return self.vBox


class installProgress():

    def __init__(self, main_window, welcome, kb, tz, adminuser):
        self.pbar = Gtk.ProgressBar()
        self.pbar.set_show_text(True)
        command = f'sudo {pc_sysinstall} -c {gbi_tmp}/pcinstall.cfg'
        thr = threading.Thread(
            target=read_output,
            args=(
                command,
                self.pbar,
                main_window,
                welcome,
                kb,
                tz,
                adminuser
            )
        )
        thr.setDaemon(True)
        thr.start()
        self.pbar.show()

    def getProgressBar(self):
        return self.pbar
