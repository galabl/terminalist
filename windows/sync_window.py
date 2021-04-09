from gi.repository import Gtk
from events.sync_window_events import SyncWindowEvents
import os
from dotenv import load_dotenv
from windows.dropbox_oauth_window import DropboxOauthWindow
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

class SyncWindow:
    glade_file = "layouts/dropbox_drive_connect_window.glade"
    builder = None
    window = None
    handler_class = None
    token = None
    APP_KEY = None
    APP_SECRET = None
    dbx = None

    def __init__(self):
        # Load env
        load_dotenv()
        self.token = os.getenv("ACCESS_TOKEN")
        self.APP_KEY = os.getenv("APP_KEY")
        self.APP_SECRET = os.getenv("APP_SECRET")
        # Build the Window
        self.build_window()
        # Connect the signals
        self.connect_events()

    def build_window(self):
        # Get the builder
        self.builder = Gtk.Builder()

        # inflate the layout
        self.builder.add_from_file(self.glade_file)

        self.window = self.builder.get_object("dropbox_drive_connect_window")
        dropbox_check = self.check_dropbox_connection()
        connect_box = self.builder.get_object("dropbox_connect_box")
        sync_box = self.builder.get_object("dropbox_sync_box")
        app_key_entry = self.builder.get_object("dropbox_app_key")
        app_secret_entry = self.builder.get_object("dropbox_secret_key")
        # Show the Window
        self.window.show_all()

        if dropbox_check:
            connect_box.hide()
        else:
            if self.APP_KEY and self.APP_SECRET is not None:
                app_key_entry.set_text(self.APP_KEY)
                app_secret_entry.set_text(self.APP_SECRET)
            sync_box.hide()

    def check_dropbox_connection(self):
        if self.token is not None:
            with dropbox.Dropbox(oauth2_access_token=self.token) as self.dbx:
                # Check that the access token is valid
                try:
                    self.dbx.users_get_current_account()
                    return True
                except AuthError:
                    return False

    def connect_events(self):
        # Connect the signals
        self.handler_class = SyncWindowEvents(self.window, self.builder)
        self.builder.connect_signals(self.handler_class)
