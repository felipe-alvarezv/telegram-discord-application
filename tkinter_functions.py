import os
import tkinter as tk
from tkinter import Toplevel
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import messagebox
from sqlite_connection import load_channel, add_channel, load_channel_info
from telegram_functions import initialize, listen
from input_validation import is_alphanumerical, is_number, is_link, is_directory_not_empty

#Main Page
def main_page_click(root):
    # Initialize Telegram client with config data
    telegram_client = initialize()

    #Initialize Tkinter notebook to store tabs
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    #Information Tab
    info_frame = tk.Frame(root)
    info_frame.pack()

    #Information Tab - Widgets
    info_label = tk.Label(info_frame, text="The purpose of this application is to foward text messages from a Telegram channel to a Discord channel webhook.")
    info_label.grid(row=0, column=0)
    
    media_label = tk.Label(info_frame, text='Media is not currently supported!')
    media_label.grid(row=1, column=0, pady=10)

    info_start_btn = tk.Button(info_frame, text="Start Application", command=lambda: start_application(root, telegram_client))
    info_start_btn.grid(row=2, column=0, pady=40)

    author_label = tk.Label(info_frame, text="Made by Felipe Alvarez")
    author_label.grid(row=3, column=0)

    #Channel Management Tab
    manage_frame = tk.Frame(root)
    manage_frame.pack()

    #Channel Management Tab - Frames
    manage_left_frame_top = tk.Frame(manage_frame)
    manage_left_frame_top.grid(row=0, column=0)

    manage_left_frame_bottom = tk.Frame(manage_frame)
    manage_left_frame_bottom.grid(row=1, column=0)

    manage_right_frame_top = tk.Frame(manage_frame)
    manage_right_frame_top.grid(row=0, column=1, sticky='ns')

    manage_right_frame_bottom = tk.Frame(manage_frame)
    manage_right_frame_bottom.grid(row=1, column=1)

    channels = load_channel() #Load channel objects

    #Create Treeview for channels
    root_tree = ttk.Treeview(manage_left_frame_top, column=('c1'), show='headings', height=8, selectmode='browse')
    root_tree.column('#1', width=200, anchor='center')
    root_tree.heading('#1', text='Description')
    root_tree.grid(row=0, column=1, padx=5, pady=5)
    root_tree.bind('<ButtonRelease-1>', lambda event: show_channel_info(event, root_tree, root_desc, root_id, root_wh))
    root_tree.bind('<KeyRelease-Up>', lambda event: show_channel_info(event, root_tree, root_desc, root_id, root_wh))
    root_tree.bind('<KeyRelease-Down>', lambda event: show_channel_info(event, root_tree, root_desc, root_id, root_wh))

    root_tree_scroll = Scrollbar(manage_left_frame_top, orient=tk.VERTICAL, command=root_tree.yview)
    root_tree['yscrollcommand'] = root_tree_scroll.set
    root_tree_scroll.grid(row=0, column=0, sticky='ns')

    #Add all loaded channels to Treeview
    for channel in channels:
        root_tree.insert('', 'end', text='1', values=channel)

    #Add Channel Button Widget
    add_btn = tk.Button(manage_left_frame_bottom, text="Add Channel", command=lambda: add_channel_btn(root, telegram_client, root_tree))
    add_btn.grid(row=0, column=0)

    #Channel Information Listbox Widgets
    channel_desc_label = tk.Label(manage_right_frame_top, justify='left', text="Description:")
    channel_desc_label.grid(row=0, column=0, sticky='w')

    root_desc = tk.Entry(manage_right_frame_top, state='disabled', disabledbackground='white', disabledforeground='black', width=44)
    root_desc.grid(row=0, column=1, sticky='ew')

    channel_id_label = tk.Label(manage_right_frame_top, justify='left', text='ID:')
    channel_id_label.grid(row=1, column=0, sticky='w')

    root_id = tk.Entry(manage_right_frame_top, state='disabled', disabledbackground='white', disabledforeground='black')
    root_id.grid(row=1, column=1, sticky='ew')

    channel_wh_label = tk.Label(manage_right_frame_top, justify='left', text="Webhook:")
    channel_wh_label.grid(row=2, column=0, sticky='w')

    root_wh = tk.Entry(manage_right_frame_top, state='disabled', disabledbackground='white', disabledforeground='black')
    root_wh.grid(row=2, column=1, sticky='ew')

    #Delete Channel Button Widget
    delete_btn = tk.Button(manage_right_frame_bottom, text='Delete Channel', command=lambda: delete_channel_btn(root_tree))
    delete_btn.grid(row=0, column=1)

    #Set the names of the tabs
    notebook.add(info_frame, text="Information")
    notebook.add(manage_frame, text="Channel Management")

def show_channel_info(event, channel_tree, channel_desc_entry, channel_id_entry, channel_wh_entry):
    selection = channel_tree.selection() #Get the selected item of the tree

    if selection:
        #Get the selected channel
        desc = channel_tree.item(selection)['values'][0]

        #Enable Entry widgets for information
        channel_desc_entry.configure(state='normal')
        channel_id_entry.configure(state='normal')
        channel_wh_entry.configure(state='normal')

        #Clear previous data
        channel_desc_entry.delete(0, 'end')
        channel_id_entry.delete(0, 'end')
        channel_wh_entry.delete(0, 'end')

        #Set new data
        channel_desc_entry.insert(0, desc)
        channel_id_entry.insert(0, load_channel_info(desc, 'id'))
        channel_wh_entry.insert(0, load_channel_info(desc, 'webhook'))

        #Disable widgets to prevent modifying values
        channel_desc_entry.configure(state='disable')
        channel_id_entry.configure(state='disable')
        channel_wh_entry.configure(state='disable')


def add_channel_btn(root, telegram_client, channel_tree):
    #Create a new window with for add channel widgets
    add_channel_window = Toplevel(root)
    add_channel_window.title("Add Channel")
    add_channel_window.grab_set()
    add_channel_window.resizable(width=False, height=False)

    #Geometry to place new window on top of root
    x = root.winfo_x()
    y = root.winfo_y()
    add_channel_window.geometry("+%d+%d" % (x + 80, y + 60))

    #Frames for right and left side
    left_side = tk.Frame(add_channel_window)
    left_side.grid(row=0, column=0)

    right_side = tk.Frame(add_channel_window)
    right_side.grid(row=0, column=1)

    bottom_left = tk.Frame(add_channel_window)
    bottom_left.grid(row=1, column=0)

    bottom_right = tk.Frame(add_channel_window)
    bottom_right.grid(row=1, column=1)

    #Widgets for Description
    description_label = tk.Label(left_side, text='Description:')
    description_label.grid(row=0, column=0, sticky='w', pady=(0, 5))

    description_entry = tk.Entry(right_side, width=44)
    description_entry.grid(row=0, column=0, pady=(0, 5))

    #Widgets for ID
    id_label = tk.Label(left_side, text="ID:")
    id_label.grid(row=1, column=0, sticky='w', pady=(0, 5))

    #Varianble to store existing channels
    channels = []
    for dialog in telegram_client.iter_dialogs():
        if dialog.is_channel:
            temp_channel = [dialog.title, dialog.id * -1]
            channels.append(temp_channel)

    selected_channel = tk.Variable(right_side)

    id_options = tk.OptionMenu(right_side, selected_channel, *channels)
    id_options.grid(row=1, column=0, sticky='ew', pady=(0, 5))

    #Widgets for Webhook
    webhook_label = tk.Label(left_side, text="Webhook:")
    webhook_label.grid(row=2, column=0, sticky='w', pady=(0, 5))

    webhook_entry = tk.Entry(right_side)
    webhook_entry.grid(row=2, column=0, sticky='ew', pady=(0, 5))

    #Widget for submition
    submit_button = tk.Button(bottom_right, text="Submit", command=lambda: add_channel_btn_clicked(add_channel_window, channel_tree, description_entry, selected_channel, webhook_entry))
    submit_button.grid(row=0, column=0, pady=5)

    add_channel_window.grab_set()


#Add Channel Button Event
def add_channel_btn_clicked(add_channel_window, channel_tree, description_entry, selected_channel, webhook_entry):
    if description_entry and selected_channel.get() and webhook_entry:
        #Store description input
        description = description_entry.get()
        channel_id = selected_channel.get()[1]
        webhook = webhook_entry.get()

        if description and channel_id and webhook:
            if is_alphanumerical(description) and is_number(channel_id) and is_link(webhook):
                add_channel(description, channel_id, webhook)
                add_channel_window.destroy()

                channel_tree.delete(*channel_tree.get_children())  #Clear Treeview
                channels = load_channel()

                #Add all loaded Channels to Treeview
                for channel in channels:
                    new_channel = channel_tree.insert('', 'end', text='1', values=channel)

                    if channel.get_id() == selected_channel.get()[1]:
                        channel_tree.selection_set(new_channel)
            else:
                messagebox.showerror('Invalid Field', 'Please make sure to enter valid information that meets these requirements:\n\nDescription must only be alphanumerical.\nWebhook must be a valid link.')
        else:
            messagebox.showerror('Invalid Field', 'Please make sure to enter valid information that meets these requirements:\n\nDescription must only be alphanumerical.\nWebhook must be a valid link.')
    else:
        messagebox.showerror('Invalid Field', 'Please make sure to select a channel.')

#Delete Channel Button Event
def delete_channel_btn(channel_tree):
    selection = channel_tree.selection() #Get the selected item of the tree

    if selection:
        response = messagebox.askquestion('Delete Channel', 'Are you sure you want to delete the channel?')

        if response == 'yes':
            #Get the selected channel description
            data = channel_tree.item(selection)['values'][0]

            if data:
                filename = 'channels/' + data + '.pkl'
                os.remove(filename) #Delete channel file

            channel_tree.delete(*channel_tree.get_children())  #Clear Treeview
            channels = load_channel() #Load channel objects

            #Add all loaded Channels to Treeview
            for channel in channels:
                channel_tree.insert('', 'end', text='1', values=channel)
    else:
        messagebox.showerror('Invalid Channel', 'Please make sure to select a channel.')

def start_application(root, telegram_client):
    directory = './channels/'
    if is_directory_not_empty(directory):
        root.destroy()
        listen(telegram_client)
    else:
        messagebox.showerror('Empty Directory', 'Make sure to at least add one channel to begin the application.')