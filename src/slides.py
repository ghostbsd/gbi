#!/usr/bin/env python3

from gi.repository import Gtk, Gdk
import threading
from time import sleep

class Slides:
    def Welcome(self):
        grid = Gtk.Grid()
        grid.show()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        label = Gtk.Label()
        label.set_markup('<span foreground="#F9F9F9" size="xx-large">Welcome to GhostBSD 10.2!</span>')
        eb = Gtk.EventBox()
        eb.add(label)
        eb.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#3C3B37"))
        grid.attach(eb, 0, 0, 8, 1)
        label2 = Gtk.Label()
        label2.set_markup("Thank you for choosing GhostBSD. We hope you enjoy the BSD experience.\n"
                            "\nWe believe every computer Operating System should be Secure, respect\nyour privacy and true freedom, be elegant and light, GhostBSD makes \nFreeBSD desktop computing more easier.\n"
                            "\nWe want GhostBSD to work for you. So while your software is installing,\nthis slideshow will introduce you to GhostBSD.\n")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        grid.attach(label2, 1, 1, 6, 4)
        image = Gtk.Image.new_from_file('/usr/local/lib/gbi/slide-images/G-logo.png')
        grid.attach(image, 1, 4, 6, 6)
        return grid

    def TheWeb(self):
        grid = Gtk.Grid()
        grid.show()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        label = Gtk.Label()
        label.set_markup('<span foreground="#F9F9F9" size="xx-large">Make the most of the web</span>')
        eb = Gtk.EventBox()
        eb.add(label)
        eb.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#3C3B37"))
        grid.attach(eb, 0, 0, 8, 1)
        label2 = Gtk.Label()
        label2.set_markup("GhostBSD includes Mozilla Firefox, the web browser used by millions of\npeople around the world.\n"
                            "\nBrowse the web safely and with private, share your files, software,\nand multimedia, send and receive e-mail, and communicate with friends\n and family.\n"
                            "\nWeb browsers such as Chromium and Epiphany are easily installable.\n")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        grid.attach(label2, 1, 1, 6, 4)
        image = Gtk.Image.new_from_file('/usr/local/lib/gbi/slide-images/Mozilla-Firefox-Start-Page.png')
        grid.attach(image, 1, 4, 6, 6)
        return grid

    def Photos(self):
        grid = Gtk.Grid()
        grid.show()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        label = Gtk.Label()
        label.set_markup('<span foreground="#F9F9F9" size="xx-large">Organize, retouch, and share your photos</span>')
        eb = Gtk.EventBox()
        eb.add(label)
        eb.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#3C3B37"))
        grid.attach(eb, 0, 0, 8, 1)
        label2 = Gtk.Label()
        label2.set_markup("With Shotwell, it is really easy to organize and share your photos\n"
                            "\nUse the Export option to copy your photos to a remote computer, iPod,\na custom HTML gallery, or to export to services such as Flickr, \nFacebook, PicasaWeb, and more.\n"
                            "\nFor more advanced photos editing, Gimp is available for installation.\n")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        grid.attach(label2, 1, 1, 6, 4)
        image = Gtk.Image.new_from_file('/usr/local/lib/gbi/slide-images/Shotwell.png')
        grid.attach(image, 1, 4, 6, 6)
        return grid

    def MultiMedia(self):
        grid = Gtk.Grid()
        grid.show()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        label = Gtk.Label()
        label.set_markup('<span foreground="#F9F9F9" size="xx-large">Play your movies and musics</span>')
        eb = Gtk.EventBox()
        eb.add(label)
        eb.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#3C3B37"))
        grid.attach(eb, 0, 0, 8, 1)
        label2 = Gtk.Label()
        label2.set_markup("GhostBSD is ready to play videos and music from the web, CDs and DVDs.\n"
                            "\nExail audio player lets you organize your music and listen to Internet\nradio, podcasts, and more, as well as synchronizes your audio \ncollection to a portable audio player.\n"
                            "\nGnome MPlayer allows you to easily watch videos from your computer, DVD.\n")
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_line_wrap(True)
        grid.attach(label2, 1, 1, 6, 4)
        image = Gtk.Image.new_from_file('/usr/local/lib/gbi/slide-images/Exaile.png')
        grid.attach(image, 1, 4, 6, 6)
        return grid

    def SlideRight(self, widget):
        if self.stack.get_visible_child() == self.welcome:
            self.stack.set_visible_child(self.web)
        elif self.stack.get_visible_child() == self.web:
            self.stack.set_visible_child(self.photos)
        elif self.stack.get_visible_child() == self.photos:
            self.stack.set_visible_child(self.multimedia)


    def SlideLeft(self, widget):
        if self.stack.get_visible_child() == self.web:
            self.stack.set_visible_child(self.welcome)
        elif self.stack.get_visible_child() == self.photos:
            self.stack.set_visible_child(self.web)
        elif self.stack.get_visible_child() == self.multimedia:
            self.stack.set_visible_child(self.photos)

    def __init__(self):
        self.grid = Gtk.Grid()
        self.grid.show()
        self.grid.set_row_homogeneous(True)
        self.grid.set_column_homogeneous(False)
        self.stack = Gtk.Stack()
        self.grid.attach(self.stack, 1, 0, 10, 10)
        # Adding slide self.grid in to stack
        self.welcome = self.Welcome()
        self.stack.add_named(self.welcome, "welcome")
        self.web = self.TheWeb()
        self.stack.add_named(self.web, "web")
        self.photos = self.Photos()
        self.stack.add_named(self.photos, "photos")
        self.multimedia = self.MultiMedia()
        self.stack.add_named(self.multimedia, "multimedia")
        label = Gtk.Label()
        eb = Gtk.EventBox()
        eb.add(label)
        eb.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#3C3B37"))
        self.grid.attach(eb, 0, 0, 1, 1)
        Bimg = Gtk.Image()
        Bimg.set_from_icon_name("go-previous", Gtk.IconSize.BUTTON)
        BackButton = Gtk.Button(None, image=Bimg)
        BackButton.connect("clicked", self.SlideLeft)
        BackButton.show()
        Nimg = Gtk.Image()
        Nimg.set_from_icon_name("go-next", Gtk.IconSize.BUTTON)
        NextButton = Gtk.Button(None, image=Nimg)
        NextButton.set_sensitive(True)
        NextButton.connect("clicked", self.SlideRight)
        NextButton.show()
        self.grid.attach(NextButton, 11, 5, 1, 1)
        self.grid.attach(BackButton, 0, 5, 1, 1)
        label = Gtk.Label()
        eb = Gtk.EventBox()
        eb.add(label)
        eb.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#3C3B37"))
        self.grid.attach(eb, 11, 0, 1, 1)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)
        self.stack.show()
        #thr = threading.Thread(target=self.slidesThreading)
        #thr.setDaemon(True)
        #thr.start()
        return

    def get_slide(self):
        return self.grid

    # def slidesThreading(self):
    #     while 1:
    #         sleep(60)
    #         self.SlideRight()