from events.dropbox_oauth_window_events import DropboxOauthWindowEvents
from gi.repository import Gtk
from dropbox import DropboxOAuth2FlowNoRedirect
import os
from dotenv import load_dotenv


class DropboxOauthWindow:
    glade_file = "layouts/dropbox_oauth_window.glade"
    main_object = None
    handler_class = None
    builder = None
    window = None
    APP_KEY = None
    APP_SECRET = None
    auth_flow = None

    def __init__(self):
        # Build the Window
        load_dotenv()
        self.APP_KEY = os.environ.get("APP_KEY")
        self.APP_SECRET = os.environ.get("APP_SECRET")
        self.build_window()
        # Connect the signals
        self.connect_events()

    def build_window(self):
        # Get the builder
        self.builder = Gtk.Builder()

        # inflate the layout
        self.builder.add_from_file(self.glade_file)

        self.window = self.builder.get_object("dropbox_connection_popup")

        self.auth_flow = DropboxOAuth2FlowNoRedirect(self.APP_KEY, self.APP_SECRET)

        authorize_url = self.auth_flow.start()
        link = self.builder.get_object("authorize_url_btn")
        link.set_uri(authorize_url)
        label = self.builder.get_object("dropbox_oauth_label")
        label.set_text("""
            2. Click \"Allow\" (you might have to log in first). \n
            3. Copy the authorization code.
        """)

        # Show the Window
        self.window.show_all()

    def connect_events(self):
        # Connect the signals
        self.handler_class = DropboxOauthWindowEvents(self.window, self.builder, self.auth_flow)
        self.builder.connect_signals(self.handler_class)
