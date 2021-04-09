from gi.repository import Gtk
from events.connection_window_events import ConnectionWindowEvents
from collection.groups import Groups


class ConnectionWindow:
    glade_file = "layouts/connection_window.glade"
    main_object = None
    handler_class = None
    builder = None
    window = None
    refresh_list_callback = None
    connection = None
    groups = None

    def __init__(self, refresh_list_callback, connection=None):
        # Set some properties
        gtk_settings = Gtk.Settings.get_default()
        gtk_settings.props.gtk_button_images = True
        self.refresh_list_callback = refresh_list_callback
        self.connection = connection
        self.groups = Groups()

        # Build the Window
        self.build_window()

        # Connect the signals
        self.connect_events()

    def build_window(self):
        # Get the builder
        self.builder = Gtk.Builder()

        # inflate the layout
        self.builder.add_from_file(self.glade_file)

        self.window = self.builder.get_object("new_connection_window")

        self.groups.load_groups()
        groups = self.builder.get_object("combo_groups")
        groups.set_model(self.groups.get_groups_names_model())
        renderer_text = Gtk.CellRendererText()
        groups.pack_start(renderer_text, True)
        groups.add_attribute(renderer_text, "text", 0)

        # If connection is not None, is an Edit, so, change the Title
        if self.connection is not None:
            self.window.set_title("Edit Connection - Terminalist")
            groups.set_active(self.connection.connection_group_id)

        self.window.show_all()

    def connect_events(self):
        # Connect the signals
        self.handler_class = ConnectionWindowEvents(self.window, self.builder, self.refresh_list_callback, self.connection)
        self.builder.connect_signals(self.handler_class)
