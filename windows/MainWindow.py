from gi.repository import Gtk
from collection.connections import Connections
from collection.groups import Groups
from events.main_window_events import MainWindowEvents


class MainWindow:
    glade_file = "layouts/main_window.glade"
    main_object = None
    handler_class = None
    builder = None
    window = None
    connections = None
    groups = None
    active_group = None

    def __init__(self):
        gtk_settings = Gtk.Settings.get_default()
        gtk_settings.props.gtk_button_images = True

        # Get all groups
        self.groups = Groups()
        self.groups.load_groups()

        # Get the connections
        self.connections = Connections()
        self.connections.load_connections()

        # Build the Window
        self.build_window()

        # Connect the signals
        self.connect_events()

        # Main Loop of GTK
        Gtk.main()

    def build_window(self):
        # Get the builder
        self.builder = Gtk.Builder()

        # inflate the layout
        self.builder.add_from_file(self.glade_file)

        self.window = self.builder.get_object("terminalist_window")
        self.window.set_title("Terminalist - V0.1")
        self.window.connect("delete-event", Gtk.main_quit)

        # Build the connection TreeView
        self.build_groups_treeview()

        self.window.show_all()

    # Connect glade signals
    def connect_events(self):
        self.handler_class = MainWindowEvents(self.window, self.builder, self.connections)
        self.builder.connect_signals(self.handler_class)

    # Show connections
    def build_connection_treeview(self):
        # Get the connection TreeView
        connection = self.builder.get_object('connections_tree')
        # Create the Column
        if len(connection.get_columns()) == 0:
            column = Gtk.TreeViewColumn('Connections', Gtk.CellRendererText(), text=0)
            column.set_clickable(False)
            # Append the column on the TreeView
            connection.append_column(column)

        # Set the model
        connection.set_model(self.connections.get_connection_names_model())

    # Show groups
    def build_groups_treeview(self):
        # Get the connection TreeView
        groups = self.builder.get_object('groups_tree')

        # Create the Column
        column = Gtk.TreeViewColumn('Groups', Gtk.CellRendererText(), text=0)
        column.set_clickable(False)
        groups.connect("cursor-changed", self.group_open)

        # Append the column on the TreeView
        groups.append_column(column)

        # Set the model
        groups.set_model(self.groups.get_groups_names_model())

    def group_open(self, column):
        # Get the selected ID
        tree = self.builder.get_object("groups_tree")

        # Get the selection
        (model, treeiter) = tree.get_selection().get_selected_rows()

        # Get the connection ID
        if model is not None and len(treeiter) > 0:
            # Get the ID
            group_id = model[treeiter][1]
            self.connections = Connections()
            self.connections.load_connections(group_id)

            self.build_connection_treeview()
