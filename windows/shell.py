# -*- coding: utf-8 -*-
import gi
from gi.overrides.Gdk import Gdk

gi.require_version('Vte', '2.91')
from gi.repository import Gtk
from gi.repository import Gdk as gdk
from gi.repository import GLib
from gi.repository import Vte
from windows.message_box import MessageBox


class Shell:
    terminal = None
    command = None
    tab_box = None
    title = None
    executed = False
    pid = None
    tab_header = None
    tab = None

    def __init__(self, command, window_title, tab):
        # Command to Run and Env
        self.clipboard = Gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD)
        self.command = str(command).split(' ')
        self.title = window_title
        self.tab = tab

        # Create the terminal
        self.terminal = Vte.Terminal()
        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,  # Pty Flags
            None,  # Working DIR
            self.command,  # Command/BIN (argv)
            [],  # Environmental Variables (envv)
            GLib.SpawnFlags.DEFAULT,  # Spawn Flags
            None, None,  # Child Setup
            -1,  # Timeout (-1 for indefinitely)
            None,  # Cancellable
            None,  # Callback
            None  # User Data
        )

    def run(self):
        # create a window and add the VTE
        self.tab_box = Gtk.Box(expand=True)
        self.tab_box.pack_start(self.terminal, True, True, 0)

        self.tab_header = Gtk.HBox()
        self.tab_header.set_border_width(10)
        title_label = Gtk.Label(label=self.title)
        close_button = Gtk.Button('X')
        self.tab_header.pack_start(title_label,
                                   expand=True, fill=True, padding=0)
        self.tab_header.pack_end(close_button,
                                 expand=False, fill=False, padding=0)

        self.tab.append_page(self.tab_box, self.tab_header)
        self.tab_header.show_all()
        self.tab.show_all()
        tab_num = self.tab.page_num(self.tab_box)
        close_button.connect('clicked', self.quit_tab, tab_num)
        self.tab.set_current_page(tab_num)
        self.terminal.connect("key_press_event", self.copy_or_paste)
        self.terminal.connect("child-exited", self.child_quit, tab_num)

    def copy_or_paste(self, widget, event):
        control_key = Gdk.ModifierType.CONTROL_MASK
        shift_key = Gdk.ModifierType.SHIFT_MASK
        if event.type == Gdk.EventType.KEY_PRESS:
            if event.state == shift_key | control_key:  # both shift  and control
                if event.keyval == 67:  # that's the C key
                    self.terminal.copy_clipboard_format(Vte.Format.TEXT)
                elif event.keyval == 86:  # and that's the V key
                    self.terminal.paste_clipboard()
                return True

    def child_quit(self, *args):
        tab_num = args[2]
        self.tab.remove_page(tab_num)

    def quit_tab(self, btn, tab_num):
        self.tab.remove_page(tab_num)
