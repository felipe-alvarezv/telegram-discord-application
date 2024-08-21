import os
import pickle
import tkinter as tk
from tkinter import Toplevel
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import messagebox
from Channel import Channel 
from load_functions import load_channel_list
from telegram_functions import initialize, listen

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
    manage_right_frame_top.grid(row=0, column=1)

    manage_right_frame_bottom = tk.Frame(manage_frame)
    manage_right_frame_bottom.grid(row=1, column=1)

    channels = load_channel_list() #Load channel objects as a list

    #Create Treeview for channels
    channel_tree = ttk.Treeview(manage_left_frame_top, column=('c1', 'c2', 'c3'), show='headings', height=8, selectmode='browse')
    channel_tree.column('#1', width=200, anchor='center')
    channel_tree.heading('#1', text='Description')
    channel_tree.column('#2', width=0, stretch = "no")
    channel_tree.heading('#2', text='ID')
    channel_tree.column("#3", width = 0, stretch = "no")
    channel_tree.heading('#3', text='Webhook')
    channel_tree.grid(row=0, column=1, padx=5, pady=5)
    channel_tree.bind('<ButtonRelease-1>', lambda event: show_channel_info(event, channel_tree, channel_info_list))
    channel_tree.bind('<KeyRelease-Up>', lambda event: show_channel_info(event, channel_tree, channel_info_list))
    channel_tree.bind('<KeyRelease-Down>', lambda event: show_channel_info(event, channel_tree, channel_info_list))

    channel_tree_scroll = Scrollbar(manage_left_frame_top, orient=tk.VERTICAL, command=channel_tree.yview)
    channel_tree['yscrollcommand'] = channel_tree_scroll.set
    channel_tree_scroll.grid(row=0, column=0, sticky='ns')

    #Add all loaded channels to Listbox
    for channel in channels:
        channel_tree.insert('', 'end', text='1', values=channel)

    #Add Channel Button Widget
    add_btn = tk.Button(manage_right_frame_bottom, text="Add Channel", command=lambda: add_channel_btn(root, telegram_client, channel_tree))
    add_btn.grid(row=0, column=0)

    #Channel Information Listbox Widget
    channel_info_list = tk.Listbox(manage_right_frame_top, width=80, height=6)
    channel_info_list.grid(row=0, column=0, padx=5, pady=5, sticky='n')

    info_scroll = Scrollbar(manage_right_frame_top, orient=tk.HORIZONTAL, command=channel_info_list.xview)
    channel_info_list['xscrollcommand'] = info_scroll.set
    info_scroll.grid(row=1, column=0, sticky='ew')

    #Delete Channel Button Widget
    delete_btn = tk.Button(manage_right_frame_bottom, text='Delete Channel', command=lambda: delete_channel_btn(root, telegram_client, channel_tree))
    delete_btn.grid(row=0, column=1)

    #Set the names of the tabs
    notebook.add(info_frame, text="Information")
    notebook.add(manage_frame, text="Channel Management")

def show_channel_info(event, channel_tree, channel_info_list):
    selection = channel_tree.selection() #Get the selected item of the tree
    channel_info_list.delete(0, 'end') #Delete the previous info displayed

    if selection:
        #Get the selected channel
        data = channel_tree.item(selection)['values']

        #Add the channel's information to the list
        for item in data:
            channel_info_list.insert("end", item)

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
    if description_entry.get() and selected_channel and webhook_entry.get():
        filename = 'channels/' + description_entry.get() + '.pkl'
        channel_file = open(filename, 'wb')
        temp_channel = Channel(description_entry.get(), selected_channel.get()[1], webhook_entry.get()) #Make a Channel object with the passed variable
        pickle.dump(temp_channel, channel_file)
        channel_file.close()
        add_channel_window.destroy()

        channel_tree.delete(*channel_tree.get_children())  #Clear Treeview
        channels = load_channel_list() #Load channel objects as a list

        #Add all loaded Channels to Treeview
        for channel in channels:
            channel_tree.insert('', 'end', text='1', values=channel)

        

#Delete Channel Button Event
def delete_channel_btn(root, telegram_client, channel_tree):
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
            channels = load_channel_list() #Load channel objects as a list

            #Add all loaded Channels to Treeview
            for channel in channels:
                channel_tree.insert('', 'end', text='1', values=channel)

def start_application(root, telegram_client):
    root.destroy()
    listen(telegram_client)