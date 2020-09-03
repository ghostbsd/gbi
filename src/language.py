#!/usr/bin/env python

from gi.repository import Gtk, Gdk
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
# Text to be replace be multiple language file.
welltext = """Select the language you want to use with GhostBSD."""

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('/usr/local/lib/gbi/ghostbsd-style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(
    screen,
    cssProvider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class Language:

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

    # Initial definition.
    def __init__(self):
        # Add a Default vertical box
        self.vbox1 = Gtk.VBox(False, 0)
        self.vbox1.show()
        # Add a second vertical box
        grid = Gtk.Grid()
        Title = Gtk.Label('Welcome To GhostBSD!', name="Header")
        Title.set_property("height-request", 50)
        self.vbox1.pack_start(Title, False, False, 0)
        self.vbox1.pack_start(grid, True, True, 0)
        grid.set_row_spacing(10)
        grid.set_column_spacing(3)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_margin_left(10)
        grid.set_margin_right(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        # Adding a Scrolling Window
        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # Adding a treestore and store language in it.
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
        grid.attach(sw, 1, 2, 1, 9)
        # add text in a label.
        vbox2 = Gtk.VBox(False, 0)
        vbox2.set_border_width(10)
        vbox2.show()
        self.wellcometext = Gtk.Label(welltext)
        self.wellcometext.set_use_markup(True)
        table = Gtk.Table()
        # wall = Gtk.Label()
        # table.attach(wall, 0, 1, 2, 3)
        table.attach(self.wellcometext, 0, 1, 3, 4)
        vbox2.pack_start(table, False, False, 5)
        image = Gtk.Image()
        image.set_from_file(logo)
        image.show()
        # grid.attach(self.wellcome, 1, 1, 3, 1)
        vbox2.pack_start(image, True, True, 5)
        grid.attach(vbox2, 2, 2, 2, 9)
        grid.show()
        return

    def get_model(self):
        return self.vbox1
