#!/usr/bin/env python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import threading
from time import sleep
import sys
import os
installer = "/usr/local/lib/gbi/"
rcconfgbsd = "/etc/rc.conf.ghostbsd"
rcconfdbsd = "/etc/rc.conf.desktopbsd"

sys.path.append(installer)
cssProvider = Gtk.CssProvider()
if os.path.exists(rcconfgbsd):
    cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
elif os.path.exists(rcconfdbsd):
    cssProvider.load_from_path('/usr/local/lib/gbi/desktopbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,
                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)


class gbsdSlides:
    def Welcome(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Welcome to GhostBSD 10.3!", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="welcome")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        vBox2 = Gtk.VBox(False, 0)
        vBox2.show()
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("Thank you for choosing GhostBSD. We hope you enjoy the BSD experience.\n\n"
                          "We believe every computer Operating System should be Secure, respect your privacy and true freedom, be elegant and light, GhostBSD makes FreeBSD desktop computing more easier.\n\n"
                          "We want GhostBSD to work for you. So while your software is installing, this slideshow will introduce you to GhostBSD.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        # label2.set_max_width_chars(10)
        label2.set_alignment(0.0, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def Software(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Install more software ", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="software")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("Search, install, upgrade and uninstall software with OctoPkg software manager.\n\n"
                          "OctoPkg is a powerful tool to manage GhostBSD/FreeBSD software. It has a simple interface which consists of just 2 panels, a list of all available software including results of searches and a tab widget showing 6 useful tabs information, files, transaction, output, news and a quick help guide\n\n"
                          "There are over 25000 softwares available to install.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def TheWeb(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Make the most of the web", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="web")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("GhostBSD includes Mozilla Firefox, the web browser used by millions of people around the world.\n\n"
                          "Browse the web safely and with private, share your files, software, and multimedia, send and receive e-mail, and communicate with friends and family.\n\n"
                          "Web browsers such as Chromium and Epiphany are easily installable.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def email(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Make the most of the web", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="web")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("GhostBSD includes Mozilla Firefox, the web browser used by millions of people around the world.\n\n"
                          "Browse the web safely and with private, share your files, software, and multimedia, send and receive e-mail, and communicate with friends and family.\n\n"
                          "Web browsers such as Chromium and Epiphany are easily installable.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def Photos(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label(name="Header")
        label.set_markup('Organize, retouch, and share your photos')
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="photo")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("With Shotwell, it is really easy to organize and share your photos\n\n"
                          "Use the Export option to copy your photos to a remote computer, iPod, a custom HTML gallery, or to export to services such as Flickr, Facebook, PicasaWeb, and more.\n\n"
                          "For more advanced photos editing, Gimp is available for installation.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def MultiMedia(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Play your movies and musics", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="mutimedia")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("GhostBSD is ready to play videos and music from the web, CDs and DVDs.\n\n"
                          "Exail audio player lets you organize your music and listen to Internet radio, podcasts, and more, as well as synchronizes your audio collection to a portable audio player.\n\n"
                          "\nGnome MPlayer allows you to easily watch videos from your computer, DVD.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def communicate(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Play your movies and musics", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="communicate")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("GhostBSD is ready to play videos and music from the web, CDs and DVDs.\n\n"
                          "Exail audio player lets you organize your music and listen to Internet radio, podcasts, and more, as well as synchronizes your audio collection to a portable audio player.\n\n"
                          "Gnome MPlayer allows you to easily watch videos from your computer, DVD.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def Help(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Help & Support", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="help")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("Check out the forums for answers to all your GhostBSD questions.\n\n"
                          "There's a good chance your question will have been answered already and, if not, you'll find volunteers eager to help.\n\n"
                          "For more support options, go to our <a href='http://www.ghostbsd.org/support'>support page</a>.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def SlideRight(self):
        if self.stack.get_visible_child() == self.welcome:
            self.stack.set_visible_child(self.software)
        elif self.stack.get_visible_child() == self.software:
            self.stack.set_visible_child(self.web)
        elif self.stack.get_visible_child() == self.web:
            self.stack.set_visible_child(self.photos)
        elif self.stack.get_visible_child() == self.photos:
            self.stack.set_visible_child(self.multimedia)
        elif self.stack.get_visible_child() == self.multimedia:
            self.stack.set_visible_child(self.help)
        elif self.stack.get_visible_child() == self.help:
            self.stack.set_visible_child(self.welcome)

    def __init__(self):
        self.hBox = Gtk.HBox(False, 0)
        self.hBox.show()
        self.stack = Gtk.Stack()
        self.hBox.add(self.stack)
        # Adding slide self.grid in to stack
        self.welcome = self.Welcome()
        self.stack.add_named(self.welcome, "welcome")
        self.software = self.Software()
        self.stack.add_named(self.software, "software")
        self.web = self.TheWeb()
        self.stack.add_named(self.web, "web")
        self.photos = self.Photos()
        self.stack.add_named(self.photos, "photos")
        self.multimedia = self.MultiMedia()
        self.stack.add_named(self.multimedia, "multimedia")
        self.help = self.Help()
        self.stack.add_named(self.help, "help")
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.stack.show()
        thr = threading.Thread(target=self.slidesThreading)
        thr.setDaemon(True)
        thr.start()

    def get_slide(self):
        return self.hBox

    def slidesThreading(self):
        while 1:
            sleep(60)
            GLib.idle_add(self.SlideRight)

                                     
class dbsdSlides:
    def Welcome(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Welcome to DesktopBSD!", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="welcome")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        vBox2 = Gtk.VBox(False, 0)
        vBox2.show()
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("Thank you for choosing DesktopBSD. We hope you enjoy the BSD experience.\n\n"
                          "We believe every computer Operating System should be Secure, respect your privacy and true freedom, be elegant and light, DesktopBSD makes FreeBSD desktop computing more easier.\n\n"
                          "We want DesktopBSD to work for you. So while your software is installing, this slideshow will introduce you to DesktopBSD.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        # label2.set_max_width_chars(10)
        label2.set_alignment(0.0, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def Software(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Install more software ", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="software")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("Search, install, upgrade and uninstall software with OctoPkg software manager.\n\n"
                          "OctoPkg is a powerful tool to manage DesktopBSD/FreeBSD software. It has a simple interface which consists of just 2 panels, a list of all available software including results of searches and a tab widget showing 6 useful tabs information, files, transaction, output, news and a quick help guide\n\n"
                          "There are over 25000 softwares available to install.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def TheWeb(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Make the most of the web", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="web")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("DesktopBSD includes the BSD licensed Chromium web browser from Google.\n\n"
                          "Check out the Chrome Web Store for more apps to install in addition to the ones provided by DesktopBSD/FreeBSD.\n\n"
                          "Web browsers such as Firefox and Epiphany are easily installable.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def email(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Make the most of the web", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="web")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("DesktopBSD includes Mozilla Thunderbird.\n\n"
                          "Share your files, software, and multimedia, send and receive e-mail, and communicate with friends and family.\n\n"
                          "Other email clients such as Evolution are easily installable.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def Photos(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label(name="Header")
        label.set_markup('Organize, retouch, and share your photos')
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="photo")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("With Shotwell, it is really easy to organize and share your photos\n\n"
                          "Use the Export option to copy your photos to a remote computer, iPod, a custom HTML gallery, or to export to services such as Flickr, Facebook, PicasaWeb, and more.\n\n"
                          "For more advanced photos editing, Gimp is available for installation.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def MultiMedia(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Play your movies and musics", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="mutimedia")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("DesktopBSD is ready to play videos and music from the web, CDs and DVDs.\n\n"
                          "Exaile audio player lets you organize your music and listen to Internet radio, podcasts, and more, as well as synchronizes your audio collection to a portable audio player.\n\n"
                          "\nVLC allows you to easily watch videos from your computer, DVD.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def communicate(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Play your movies and musics", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="communicate")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("DesktopBSD is setup to connect you to the world.\n\n"
                          "Hexchat can be used to connect you to the DesktopBSD chat room on IRC.\n\n"
                          "Pidgin can connect you to many popular instant messaging networks including Facebook.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def Help(self):
        vBox = Gtk.VBox(False, 0)
        vBox.show()
        label = Gtk.Label("Help & Support", name="Header")
        label.set_property("height-request", 40)
        vBox.pack_start(label, False, False, 0)
        hBox = Gtk.HBox(False, 0, name="help")
        hBox.show()
        vBox.pack_end(hBox, True, True, 0)
        label2 = Gtk.Label(name="slideText")
        label2.set_markup("Check out the forums for answers to all your DesktopBSD questions.\n\n"
                          "There's a good chance your question will have been answered already and, if not, you'll find volunteers eager to help.\n\n"
                          "For more support options, go to our <a href='http://www.desktopbsd.net'>website</a>.")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        label2.set_alignment(0.1, 0.2)
        hBox2 = Gtk.HBox(False, 0, name="TransBox")
        hBox2.show()
        hBox.pack_start(hBox2, True, True, 0)
        hBox2.pack_start(label2, True, True, 30)
        label3 = Gtk.Label()
        hBox.pack_end(label3, True, True, 160)
        return vBox

    def SlideRight(self):
        if self.stack.get_visible_child() == self.welcome:
            self.stack.set_visible_child(self.software)
        elif self.stack.get_visible_child() == self.software:
            self.stack.set_visible_child(self.web)
        elif self.stack.get_visible_child() == self.web:
            self.stack.set_visible_child(self.photos)
        elif self.stack.get_visible_child() == self.photos:
            self.stack.set_visible_child(self.multimedia)
        elif self.stack.get_visible_child() == self.multimedia:
            self.stack.set_visible_child(self.help)
        elif self.stack.get_visible_child() == self.help:
            self.stack.set_visible_child(self.welcome)

    def __init__(self):
        self.hBox = Gtk.HBox(False, 0)
        self.hBox.show()
        self.stack = Gtk.Stack()
        self.hBox.add(self.stack)
        # Adding slide self.grid in to stack
        self.welcome = self.Welcome()
        self.stack.add_named(self.welcome, "welcome")
        self.software = self.Software()
        self.stack.add_named(self.software, "software")
        self.web = self.TheWeb()
        self.stack.add_named(self.web, "web")
        self.photos = self.Photos()
        self.stack.add_named(self.photos, "photos")
        self.multimedia = self.MultiMedia()
        self.stack.add_named(self.multimedia, "multimedia")
        self.help = self.Help()
        self.stack.add_named(self.help, "help")
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.stack.show()
        thr = threading.Thread(target=self.slidesThreading)
        thr.setDaemon(True)
        thr.start()
        
    def get_slide(self):
        return self.hBox

    def slidesThreading(self):
        while 1:
            sleep(60)
            GLib.idle_add(self.SlideRight)

