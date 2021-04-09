from gi.repository import Gtk
from events.groups_window_events import GroupsWindowEvents
from collection.groups import Groups

class GroupsWindow:
    glade_file = "layouts/connection_groups_window.glade"
    main_object = None
    handler_class = None
    builder = None
    window = None
    refresh_list_callback = None
    groups = None

    def __init__(self, groups=None):
        # Set some properties
        gtk_settings = Gtk.Settings.get_default()
        gtk_settings.props.gtk_button_images = True
        self.groups = Groups()
        self.groups.load_groups()

        # Build the Window
        self.build_window()

        # Connect the signals
        self.connect_events()

    def build_window(self):
        # Get the builder
        self.builder = Gtk.Builder()

        # inflate the layout
        self.builder.add_from_file(self.glade_file)

        self.window = self.builder.get_object("connection_groups_window")
        # Build the connection TreeView
        self.build_groups_treeview()

        self.window.show_all()

    def connect_events(self):
        # Connect the signals
        self.handler_class = GroupsWindowEvents(self.window, self.builder, self.refresh_list_callback, self.groups)
        self.builder.connect_signals(self.handler_class)

    def build_groups_treeview(self):
        # Get the connection TreeView
        groups = self.builder.get_object('group_tree')

        # Create the Column
        column = Gtk.TreeViewColumn('Groups', Gtk.CellRendererText(), text=0)
        column.set_clickable(False)

        # Append the column on the TreeView
        groups.append_column(column)

        # Set the model
        groups.set_model(self.groups.get_groups_names_model())