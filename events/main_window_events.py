# -*- coding: utf-8 -*-
from windows.about_window import AboutWindow
from model.connection import Connection
from windows.connection_window import ConnectionWindow
from windows.shell import Shell
from windows.settings_window import SettingsWindow
from windows.delete_connection_window import DeleteConnectionWindow
from windows.groups_window import GroupsWindow
from windows.sync_window import SyncWindow
from gi.repository import Gtk


class MainWindowEvents:
    window = None
    builder = None
    connections = None

    def __init__(self, window, builder, connections):
        # Copy the parameters
        self.window = window
        self.builder = builder
        self.connections = connections

    def on_btn_edit_clicked(self, btn):
        # Get the ID of selected Connection
        tree = self.builder.get_object("connections_tree")

        # Get the selection
        (model, treeiter) = tree.get_selection().get_selected_rows()

        # Get the connection ID
        if model is not None and len(treeiter) > 0:
            # Get the ID
            connection_id = model[treeiter][1]

            # Load the Connection
            connection = Connection()
            connection.id = connection_id
            connection.load()

            # Open the Window with the connection
            ConnectionWindow(self.refresh_connections_list, connection)

    def on_btn_remove_clicked(self, btn):
        # Get the selected ID
        tree = self.builder.get_object("connections_tree")

        # Get the selection
        (model, treeiter) = tree.get_selection().get_selected_rows()

        # Get the connection ID
        if model is not None and len(treeiter) > 0:
            # Get the ID
            connection_id = model[treeiter][1]
            # Instance the dialog of delete
            DeleteConnectionWindow(connection_id, self.refresh_connections_list)

    def on_btn_connect_clicked(self, btn):
        # Get the selected ID
        tree = self.builder.get_object("connections_tree")
        connection_tabs = self.builder.get_object("connection_tabs")

        # Get the selection
        (model, treeiter) = tree.get_selection().get_selected_rows()

        # Get the connection ID
        if model is not None and len(treeiter) > 0:
            # Get the ID
            connection_id = model[treeiter][1]

            # Load the Model
            connection = Connection()
            connection.id = connection_id
            connection.load()

            # Get the SSH Command
            command = connection.generate_ssh_command()

            # Open the Shell
            shell = Shell(command, connection.name, connection_tabs)
            shell.run()

    def on_refresh_item_activate(self, btn):
        # Refresh the list
        self.refresh_connections_list()

    def on_btn_add_clicked(self, btn):
        # Create the Window
        ConnectionWindow(self.refresh_connections_list)

    @staticmethod
    def on_settings_exit_activate(item):
        # Quit the Gtk main loop
        Gtk.main_quit()

    def on_settings_item_activate(self, item):
        # Create the Window
        SettingsWindow(self.refresh_connections_list)

    def on_groups_item_activate(self, item):
        # Create the Window
        GroupsWindow()

    @staticmethod
    def on_about_item_activate(item):
        # Open the about dialog
        AboutWindow()

    def refresh_connections_list(self):
        tree = self.builder.get_object("groups_tree")

        # Get the selection
        (model, treeiter) = tree.get_selection().get_selected_rows()

        # Get the connection ID
        if model is not None and len(treeiter) > 0:
            # Get the ID
            group_id = model[treeiter][1]
            # Reload the connections
            self.connections.load_connections(group_id)
        else:
            self.connections.load_connections()

        # Get the treeview
        connection = self.builder.get_object('connections_tree')

        # Get the model and clear the list
        model = connection.get_model()
        model.clear()

        # Set the new Model
        connection.set_model(self.connections.get_connection_names_model())

    def on_connection_search_submit(self, search):
        search_result = self.connections.search_connections(search.get_text())
        if len(search_result) == 0:
            self.refresh_connections_list()
        else:
            connection_tree = self.builder.get_object('connections_tree')
            model = connection_tree.get_model()
            model.clear()
            for connection in search_result:
                model.append([connection["name"], connection["id_connection"]])
            connection_tree.set_model(model)

    def on_connection_search_changed(self, search):
        if len(search.get_text()) == 0:
            self.refresh_connections_list()

    def on_settings_sync_activate(self, item):
        # Open Sync Window
        SyncWindow()

