from events.delete_connection_window_events import DeleteConnectionWindowEvents
from gi.repository import Gtk


class DeleteConnectionWindow:
    glade_file = "layouts/delete_connection_window.glade"
    main_object = None
    handler_class = None
    builder = None
    window = None
    id_connection = None
    refresh_callback = None

    def __init__(self, id_connection, refresh_callback):
        # Set some properties
        gtk_settings = Gtk.Settings.get_default()
        gtk_settings.props.gtk_button_images = True
        self.id_connection = id_connection
        self.refresh_callback = refresh_callback

        # Build the Window
        self.build_window()

        # Connect the signals
        self.connect_events()

    def build_window(self):
        # Get the builder
        self.builder = Gtk.Builder()

        # inflate the layout
        self.builder.add_from_file(self.glade_file)

        self.window = self.builder.get_object("message_box")

        self.window.show_all()

    def connect_events(self):
        # Connect the signals
        self.handler_class = DeleteConnectionWindowEvents(
            self.window, self.builder, self.id_connection, self.refresh_callback
        )
        self.builder.connect_signals(self.handler_class)

