from database.sqlite import DBConnection
from model.connection import Connection
from gi.repository import Gtk


class Connections:
    db_connection = None
    connections = []
    model = None

    def __init__(self):
        # Create the DB connection
        self.db_connection = DBConnection()

    def load_connections(self, group_id=1):
        # Reset the List
        self.connections = []

        # Create the SQL
        sql = "select * from connections where connection_group_id = ? order by name"

        # Execute the sql
        params = (group_id,)
        results = self.db_connection.select_query(sql, params)

        # Create a model for every connection
        for row in results:
            # Create new Connection
            connection = Connection()
            connection.id = row['id_connection']
            connection.name = row['name']
            connection.host = row['host']
            connection.user = row['user']
            connection.port = row['port']
            connection.use_key = True if row['use_key'] == 1 else False
            connection.key_path = row['key_path']

            # Add to the list
            self.connections.append(connection)

    # Method to get ListStore of names
    def get_connection_names_model(self):
        # Create the ListStore
        self.model = Gtk.ListStore(str, int)

        # Looping passing by every connection
        for connection in self.connections:
            self.model.append([connection.name, connection.id])

        # return the model
        return self.model

    # Return all Connection
    def get_connections(self):
        return self.connections

    def search_connections(self, search_text):
        search_text = f"%{search_text}%"
        params = (search_text, )
        sql = "select * from connections where name like ? order by name"

        results = self.db_connection.select_query(sql, params)

        return results
