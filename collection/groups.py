from database.sqlite import DBConnection
from model.groups import Groups as Group
from gi.repository import Gtk


class Groups:
    db_connection = None
    groups = []
    model = None

    def __init__(self):
        # Create the DB connection
        self.db_connection = DBConnection()

    def load_groups(self):
        # Reset the List
        self.groups = []

        # Create the SQL
        sql = "select * from connection_groups order by name"

        # Execute the sql
        results = self.db_connection.select_query(sql)

        # Create a model for every connection
        for row in results:
            # Create new Connection
            groups = Group()
            groups.id = row['id_group']
            groups.name = row['name']

            # Add to the list
            self.groups.append(groups)

    # Method to get ListStore of names
    def get_groups_names_model(self):
        # Create the ListStore
        self.model = Gtk.ListStore(str, int)

        # Looping passing by every group
        for group in self.groups:
            self.model.append([group.name, group.id])

        # return the model
        return self.model

    # Return all Connection
    def get_groups(self):
        return self.groups
