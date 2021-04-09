from dotenv import load_dotenv
from windows.message_box import MessageBox

load_dotenv()


class DropboxOauthWindowEvents:
    window = None
    builder = None
    auth_flow = None

    def __init__(self, window, builder, auth_flow):
        self.window = window
        self.builder = builder
        self.auth_flow = auth_flow

    def on_btn_save_clicked(self, btn):
        oauth_key = self.builder.get_object("dropbox_oauth_entry")
        try:
            oauth_result = self.auth_flow.finish(oauth_key.get_text())
            with open(".env", "a") as f:
                f.write("\nOAUTH_KEY = \"%s\"" % oauth_key.get_text())
                f.write("\nACCESS_TOKEN = \"%s\"" % oauth_result.access_token)
                MessageBox("Successfully connected with Dropbox")
        except Exception as e:
            MessageBox('Error: %s' % (e,))

    def on_btn_close_clicked(self, btn):
        self.window.destroy()
