# -*- coding: utf-8 -*-
from gi.repository import Gtk
from database.sqlite import DBConnection
from model.settings import Settings


class Connection:
    id = None
    name = None
    host = None
    port = 22
    user = None
    use_key = False
    key_path = None
    connection_group_id = None
    model = None

    def load(self):
        # Create the Password Manager

        # Create the DBConnection
        database = DBConnection()

        # Create the SQL
        sql = "SELECT * FROM connections WHERE id_connection = {}"

        # Bind the value
        sql = sql.format(self.id)

        # Execute the query
        rows = database.select_query(sql)

        # Set the attrs
        for row in rows:
            self.name = row['name']
            self.host = row['host']
            self.port = row['port']
            self.user = row['user']
            self.password = row['passwd']
            self.use_key = True if int(row['use_key']) == 1 else False
            self.key_path = row['key_path']
            self.connection_group_id = row["connection_group_id"]

    def save(self):

        # Create the DBConnection
        database = DBConnection()

        # Create the SQL
        if self.id is None:
            sql = "INSERT INTO connections (name, host, port, user, passwd, use_key, key_path, connection_group_id)" \
                  " VALUES ('{}', '{}', {}, '{}', '{}', {}, '{}', '{}');"
        else:
            sql = "UPDATE connections SET name = '{}', host = '{}', port = {}, user = '{}', passwd = '{}'," \
                  " use_key = {}, key_path = '{}', connection_group_id = '{}' where id_connection = {}"

        # Bind the values
        sql = sql.format(
            self.name,
            self.host,
            self.port,
            self.user,
            self.password,
            1 if self.use_key else 0,
            self.key_path,
            self.connection_group_id,
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
            sql = "DELETE FROM connections WHERE id_connection = {}"

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
        self.model.append(["Host", self.host])
        self.model.append(["Port", str(self.port)])
        self.model.append(["User", self.user])
        self.model.append(["Use Key", "Yes" if self.use_key else "No"])
        self.model.append(["Key Path", self.key_path])

        # Return the Model
        return self.model

    def generate_ssh_command(self):
        # Get the settings
        # Check if uses key
        if self.use_key is True:
            command = "/usr/bin/ssh {}@{} -i {}"
            command = command.format(self.user, self.host, self.key_path)
        else:
            command = "/usr/bin/sshpass -p{} /usr/bin/ssh {}@{}"
            command = command.format(self.password, self.user, self.host)

        # Format other parameters
        command += " -p {}"
        command = command.format(self.port)

        # Strict key checking
        command += " -o StrictHostKeyChecking=no"

        # Get the settings and apply here
        settings = Settings()
        settings.load()

        # X11 forwarding
        if settings.x11_forward == 1:
            command += " -X"

        if settings.request_compression == 1:
            command += " -C"

        if settings.force_ipv4 == 1:
            command += " -4"

        if settings.force_ipv6 == 1:
            command += " -6"

        # At the end, return the command
        return command
