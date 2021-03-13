#!/usr/bin/env python

from gi.repository import Gtk, Gdk, GdkPixbuf
import os
import os.path
from sys_handler import language_dictionary
# Folder use for the installer.
tmp = "/tmp/.gbi/"
installer = "/usr/local/lib/gbi/"
query = "sh /usr/local/lib/gbi/backend-query/"
if not os.path.exists(tmp):
    os.makedirs(tmp)
logo = "/usr/local/lib/gbi/logo.png"
langfile = '%slanguage' % tmp
lang_dictionary = language_dictionary()

Messages = """To run GhostBSD without installing, select "Try GhostBSD."

To install GhostBSD on your computer's hard disk drive, select "Install GhostBSD."

Note: Language selection only works when selecting "Try GhostBSD." When installing GhostBSD, the installation program is only in English."""

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class Welcome:

    # On selection it overwrite the delfaut language file.
    def Language_Selection(self, tree_selection):
        model, treeiter = tree_selection.get_selected()
        if treeiter is not None:
            value = model[treeiter][0]
            self.language = lang_dictionary[value]
        return

    def Language_Columns(self, treeView):
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, cell, text=0)
        column_header = Gtk.Label('Language')
        column_header.set_use_markup(True)
        column_header.show()
        column.set_widget(column_header)
        column.set_sort_column_id(0)
        treeView.append_column(column)
        return

    def save_selection(self):
        lang_file = open(langfile, 'w')
        lang_file.writelines(self.language)
        lang_file.close()
        return

    def install_system(self, widget):
        self.what = 'install'
        self.install_ghostbsd()

    def try_system(self, widget):
        self.what = 'try'
        self.try_ghostbsd()

    def get_what(self):
        return self.what

    def __init__(self, next_install_page, next_setup_install):
        self.install_ghostbsd = next_install_page
        self.try_ghostbsd = next_setup_install
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        main_grid = Gtk.Grid()
        Title = Gtk.Label('Welcome To GhostBSD!', name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        self.vbox1.pack_start(main_grid, True, True, 0)
        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        store = Gtk.TreeStore(str)
        for line in lang_dictionary:
            store.append(None, [line])
        treeView = Gtk.TreeView(store)
        treeView.set_model(store)
        treeView.set_rules_hint(True)
        self.Language_Columns(treeView)
        tree_selection = treeView.get_selection()
        tree_selection.set_mode(Gtk.SelectionMode.SINGLE)
        tree_selection.connect("changed", self.Language_Selection)
        sw.add(treeView)
        sw.show()
        vbox2 = Gtk.VBox(False, 0)
        vbox2.set_border_width(10)
        vbox2.show()
        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename='/usr/local/lib/gbi/laptop.png',
            width=190,
            height=190,
            preserve_aspect_ratio=True
        )
        image1 = Gtk.Image.new_from_pixbuf(pixbuf1)
        image1.show()
        pixbuf2 = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename='/usr/local/lib/gbi/disk.png',
            width=120,
            height=120,
            preserve_aspect_ratio=True)
        image2 = Gtk.Image.new_from_pixbuf(pixbuf2)
        image2.show()
        install_button = Gtk.Button(label='Install GhostBSD', image=image1, image_position=2)
        install_button.set_always_show_image(True)
        install_button.connect("clicked", self.install_system)
        try_button = Gtk.Button(label='Try GhostBSD', image=image2, image_position=2)
        try_button.set_always_show_image(True)
        try_button.connect("clicked", self.try_system)
        text_label = Gtk.Label(Messages)
        text_label.set_line_wrap(True)
        right_grid = Gtk.Grid()
        right_grid.set_row_spacing(10)
        right_grid.set_column_spacing(2)
        right_grid.set_column_homogeneous(True)
        right_grid.set_row_homogeneous(True)
        right_grid.set_margin_left(10)
        right_grid.set_margin_right(10)
        right_grid.set_margin_top(10)
        right_grid.set_margin_bottom(10)
        right_grid.attach(install_button, 1, 1, 1, 5)
        right_grid.attach(try_button, 2, 1, 1, 5)
        right_grid.attach(text_label, 1, 6, 2, 5)
        main_grid.set_row_spacing(10)
        main_grid.set_column_spacing(4)
        main_grid.set_column_homogeneous(True)
        main_grid.set_row_homogeneous(True)
        main_grid.set_margin_left(10)
        main_grid.set_margin_right(10)
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.attach(sw, 1, 1, 1, 10)
        main_grid.attach(right_grid, 2, 1, 3, 10)
        main_grid.show()
        return

    def get_model(self):
        return self.vbox1
