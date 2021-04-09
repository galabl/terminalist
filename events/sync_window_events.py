from windows.message_box import MessageBox
from windows.dropbox_oauth_window import DropboxOauthWindow
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import os
from dotenv import load_dotenv


class SyncWindowEvents:
    window = None
    builder = None
    local_file = 'database/sshclient.db'
    backup_path = '/sshclient.db'
    token = None
    dbx = None

    def __init__(self, window, builder):
        load_dotenv()
        self.token = os.getenv("ACCESS_TOKEN")
        self.window = window
        self.builder = builder

    def on_keys_save_btn_clicked(self, btn):
        app_key = self.builder.get_object("dropbox_app_key")
        app_secret = self.builder.get_object("dropbox_secret_key")
        with open(".env", "a") as f:
            if os.environ.get("APP_KEY") is None:
                os.environ["APP_KEY"] = app_key.get_text()
                f.write("\nAPP_KEY = \"%s\"" % app_key.get_text())
            if os.environ.get("APP_SECRET") is None:
                os.environ["APP_SECRET"] = app_secret.get_text()
                f.write("\nAPP_SECRET = \"%s\"" % app_secret.get_text())
        MessageBox("Keys successfully saved in .env file")

    def on_connect_btn_clicked(self, btn):
        # Close current window
        self.window.destroy()
        # Open Oauth Window
        DropboxOauthWindow()

    def on_upload_btn_clicked(self, btn):
        self.dropbox_connect()
        with open(self.local_file, 'rb') as f:
            print("Uploading " + self.local_file + " to Dropbox as " + self.backup_path + "...")
            try:
                self.dbx.files_upload(f.read(), self.backup_path, mode=WriteMode('overwrite'))
                MessageBox(
                    "Successfully uploaded export to Dropbox")
            except ApiError as err:
                if (err.error.is_path() and
                        err.error.get_path().reason.is_insufficient_space()):
                    MessageBox("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    MessageBox(err.user_message_text)
                else:
                    MessageBox(err)

    def on_download_btn_clicked(self, btn):
        self.dropbox_connect()
        try:
            self.dbx.files_download_to_file(self.local_file, self.backup_path)
            MessageBox("Successfully synced database w/ Dropbox")
        except ApiError as err:
            MessageBox(err)

    def dropbox_connect(self):
        with dropbox.Dropbox(oauth2_access_token=self.token) as self.dbx:
            # Check that the access token is valid
            try:
                self.dbx.users_get_current_account()
            except AuthError:
                MessageBox(
                    "ERROR: Invalid access token try re-generating an access token from the app console on the web.")

    def on_btn_close_clicked(self, btn):
        self.window.destroy()
