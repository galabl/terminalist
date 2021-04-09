from gi.repository import Gtk
from database.sqlite import DBConnection
from model.settings import Settings


class Groups:
    id = None
    name = None
    model = None

    def load(self):
        # Create the Password Manager

        # Create the DBConnection
        database = DBConnection()

        # Create the SQL
        sql = "SELECT * FROM connection_groups WHERE id_group = {}"

        # Bind the value
        sql = sql.format(self.id)

        # Execute the query
        rows = database.select_query(sql)

        # Set the attrs
        for row in rows:
            self.name = row['name']

    def save(self):

        # Create the DBConnection
        database = DBConnection()

        # Create the SQL
        if self.id is None:
            sql = "INSERT INTO connection_groups (name)" \
                  " VALUES ('{}');"
        else:
            sql = "UPDATE connection_groups SET name = '{}' where id_group = {}"

        # Bind the values
        sql = sql.format(
            self.name,
            self.id
        )

        # Execute the SQL
        if database.execute_query(sql) > 0:
            # Get the last row inserted
            if self.id is None:
                self.id = database.cursor.lastrowid

            # Return true telling it's OK
            return True
        else:
            # Return False for fail
            return False

    def delete(self):
        # Check if have the connection ID
        if self.id is not None:
            # Create the DBConnection
            database = DBConnection()

            # Create the SQL
            sql = "DELETE FROM connection_groups WHERE id_group = {}"

            # Bind the value
            sql = sql.format(self.id)

            # Execute the query
            if database.execute_query(sql) > 0:
                # Return true telling it's OK
                return True
            else:
                # Return False
                return False

    def get_model(self):
        # Create the Model
        self.model = Gtk.ListStore(str, str)
        self.model.append(["Name", self.name])

        # Return the Model
        return self.model
