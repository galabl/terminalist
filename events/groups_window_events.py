# -*- coding: utf-8 -*-
from windows.message_box import MessageBox
from model.groups import Groups


class GroupsWindowEvents:
    window = None
    builder = None
    refresh_list_callback = None
    index_to_remove = None
    group = None

    def __init__(self, window, builder, refresh_list_callback, group=None):
        # Copy the parameters
        self.window = window
        self.builder = builder
        self.refresh_list_callback = refresh_list_callback

    def on_btn_save_clicked(self, btn):
        # Save the connection
        if self.save_group():
            # Run the callback
            if self.refresh_list_callback is not None:
                # Call the callback to refresh the connection list
                self.refresh_list_callback()

            # Close the Window
            self.window.destroy()
        else:
            # Show a message Box telling the save fails
            MessageBox("Fail to save the connection. Check if have duplicate names. Try again")

    def on_btn_cancel_clicked(self, btn):
        self.window.destroy()

    def save_group(self):
        # Get all object that need be validated
        name = self.builder.get_object("group_name")

        # Create a new Connection
        if self.group is None:
            self.group = Groups()

        self.group.name = name.get_text()

        # Save the connection
        saved = self.group.save()

        # return if is saved or not
        return saved

    def on_delete_group_btn_clicked(self, button):

        tree = self.builder.get_object("group_tree")
        (model, treeiter) = tree.get_selection().get_selected_rows()

        # Get the group ID
        if model is not None and len(treeiter) > 0:
            group_id = model[treeiter][1]
            group = Groups()
            group.id = group_id

            # Delete the connection
            if group.delete() is False:
                MessageBox("Fail to delete the group, please try again")
            else:
                # TODO refresh groups after delete
                print('refresh groups')
