import tkinter as tk
from tkinter import ttk, Toplevel, Scrollbar, messagebox
from json_functions import load_configuration, save_configuration
from sqlite_functions import load_channel, load_channel_by_description, add_channel, delete_channel, is_channels_populated
from regex_functions import is_alphanumerical, is_numerical, is_link
from telegram_functions import initialize, listen
import os.path

#Empty Telegram Client
telegram_client = []

#Main Page
def main_page_click(root):
    #Initialize Tkinter notebook to store tabs
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    #Information Tab
    info_frame = tk.Frame(root)
    info_frame.pack()

    #Information Tab - Widgets
    info_label = tk.Label(info_frame, text='The purpose of this application is to foward text messages from a Telegram channel to a Discord channel webhook.')
    info_label.grid(row=0, column=0)
    
    media_label = tk.Label(info_frame, text='Media is not currently supported!')
    media_label.grid(row=1, column=0, pady=10)

    start_session_btn = tk.Button(info_frame, text='Start Session', command=start_session)
    start_session_btn.grid(row=2, column=0, pady=10)

    start_listening_btn = tk.Button(info_frame, text='Start Listening', command=lambda: start_listening(root))
    start_listening_btn.grid(row=3, column=0, pady=10)

    author_label = tk.Label(info_frame, text='Made by Felipe Alvarez')
    author_label.grid(row=4, column=0)

    #API Configuration Tab
    api_frame = tk.Frame(root)
    api_frame.pack()

    api_frame_top_left = tk.Frame(api_frame)
    api_frame_top_left.grid(row=0, column=0)

    api_frame_top_right = tk.Frame(api_frame)
    api_frame_top_right.grid(row=0, column=1)

    api_frame_bottom_left = tk.Frame(api_frame)
    api_frame_bottom_left.grid(row=1, column=0)

    api_frame_bottom_right = tk.Frame(api_frame)
    api_frame_bottom_right.grid(row=1, column=1)

    #API Configuration Label Widgets
    api_id_label = tk.Label(api_frame_top_left, justify='left', text='API ID:')
    api_id_label.grid(row=0, column=0, sticky='w')

    api_hash_label = tk.Label(api_frame_top_left, justify='left', text='API Hash:')
    api_hash_label.grid(row=1, column=0, sticky='w')

    api_title_label = tk.Label(api_frame_top_left, justify='left', text='API Title:')
    api_title_label.grid(row=2, column=0, sticky='w')

    #API Configuration Entry Widgets
    api_id_entry = tk.Entry(api_frame_top_right, width=33)
    api_id_entry.grid(row=0, column=1, sticky='w')

    api_hash_entry = tk.Entry(api_frame_top_right, width=33)
    api_hash_entry.grid(row=1, column=1, sticky='w')

    api_title_entry = tk.Entry(api_frame_top_right, width=33)
    api_title_entry.grid(row=2, column=1, sticky='w')

    #Load existing API configuration
    config = load_configuration()
    
    #Insert API configuration into fields if found
    if config:
        api_id_entry.insert(0, config['api_id'])
        api_hash_entry.insert(0, config['api_hash'])
        api_title_entry.insert(0, config['api_title'])

    #API Configuration Button Widgets
    api_button = tk.Button(api_frame_bottom_right, text='Save', command=lambda: api_save_btn(api_id_entry, api_hash_entry, api_title_entry))
    api_button.grid(row=3, column=1)

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
    add_btn = tk.Button(manage_left_frame_bottom, text='Add Channel', command=lambda: add_channel_btn(root, root_tree, root_desc, root_id, root_wh))
    add_btn.grid(row=0, column=0)

    #Channel Information Listbox Widgets
    channel_desc_label = tk.Label(manage_right_frame_top, justify='left', text='Description:')
    channel_desc_label.grid(row=0, column=0, sticky='w')

    root_desc = tk.Entry(manage_right_frame_top, state='disabled', disabledbackground='white', disabledforeground='black', width=44)
    root_desc.grid(row=0, column=1, sticky='ew')

    channel_id_label = tk.Label(manage_right_frame_top, justify='left', text='ID:')
    channel_id_label.grid(row=1, column=0, sticky='w')

    root_id = tk.Entry(manage_right_frame_top, state='disabled', disabledbackground='white', disabledforeground='black')
    root_id.grid(row=1, column=1, sticky='ew')

    channel_wh_label = tk.Label(manage_right_frame_top, justify='left', text='Webhook:')
    channel_wh_label.grid(row=2, column=0, sticky='w')

    root_wh = tk.Entry(manage_right_frame_top, state='disabled', disabledbackground='white', disabledforeground='black')
    root_wh.grid(row=2, column=1, sticky='ew')

    #Delete Channel Button Widget
    delete_btn = tk.Button(manage_right_frame_bottom, text='Delete Channel', command=lambda: delete_channel_btn(root_tree, root_desc, root_id, root_wh))
    delete_btn.grid(row=0, column=1)

    #Set the names of the tabs
    notebook.add(info_frame, text='Information')
    notebook.add(api_frame, text='API Configuration')
    notebook.add(manage_frame, text='Channel Management')

#Button handling to save the API configuration
def api_save_btn(api_id, api_hash, api_title):
    api_id_value = api_id.get()
    api_hash_value = api_hash.get()
    api_title_value = api_title.get()

    #Check if fields are empty
    if api_id_value != '' and api_hash_value != '' and api_title_value != '':
        #Check if entry data is valid for specified fields
        if is_numerical(api_id_value) and is_alphanumerical(api_hash_value) and is_alphanumerical(api_title_value):
            save_configuration(api_id_value, api_hash_value, api_title_value)
            messagebox.showinfo('Successfully Saved', 'The specified configuration has been saved.')

        else:
            messagebox.showerror('Invalid Field', 'Please make sure to enter valid information that meets these requirements:\n\nAPI ID must be numerical.\nAPI Hash must be alphanumerical.\nAPI Title must be alphanumerical.')
    else:
        messagebox.showerror('Invalid Field', 'Please fill out the empty fields.')

#Function to display corresponding info when selecting a channel in the tree
def show_channel_info(event, root_tree, root_desc, root_id, root_wh):
    selection = root_tree.selection()

    if selection:
        desc = root_tree.item(selection)['values'][0]
        modify_channel_info(root_desc, root_id, root_wh, desc)

#Function to add a new window with fields for addition of a new channel
def add_channel_btn(root, channel_tree, root_desc, root_id, root_wh):
    if telegram_client:
        #Create a new window with for add channel widgets
        add_channel_window = Toplevel(root)
        add_channel_window.title('Add Channel')
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
        id_label = tk.Label(left_side, text='ID:')
        id_label.grid(row=1, column=0, sticky='w', pady=(0, 5))

        #Varianble to store existing channels
        channels = []

        #Iterate through all Telegram channels the session is part of
        for dialog in telegram_client.iter_dialogs():
            if dialog.is_channel:
                temp_channel = [dialog.title, str(dialog.id)[1:]]
                channels.append(temp_channel)

        selected_channel = tk.Variable(right_side)

        id_options = tk.OptionMenu(right_side, selected_channel, *channels)
        id_options.grid(row=1, column=0, sticky='ew', pady=(0, 5))

        #Widgets for Webhook
        webhook_label = tk.Label(left_side, text='Webhook:')
        webhook_label.grid(row=2, column=0, sticky='w', pady=(0, 5))

        webhook_entry = tk.Entry(right_side)
        webhook_entry.grid(row=2, column=0, sticky='ew', pady=(0, 5))

        #Widget for submition
        submit_button = tk.Button(bottom_right, text='Submit', command=lambda: add_channel_btn_clicked(add_channel_window, channel_tree, root_desc, root_id, root_wh, description_entry, selected_channel, webhook_entry))
        submit_button.grid(row=0, column=0, pady=5)

        add_channel_window.grab_set()
    else:
        messagebox.showerror('Invalid Session', 'A Telegram session must be started before adding a channel.')


#Add Channel Button Event
def add_channel_btn_clicked(add_channel_window, channel_tree, root_desc, root_id, root_wh, description_entry, selected_channel, webhook_entry):
    if description_entry and selected_channel.get() and webhook_entry:
        #Store description input
        description = description_entry.get()
        channel_id = selected_channel.get()[1]
        webhook = webhook_entry.get()

        #Check if fields are not empty
        if description and channel_id and webhook:
            if is_alphanumerical(description) and is_numerical(channel_id) and is_link(webhook):
                result = add_channel(description, channel_id, webhook)

                if result: #If record was inserted successfully
                    add_channel_window.destroy()

                    channel_tree.delete(*channel_tree.get_children())  #Clear Treeview
                    channels = load_channel()

                    #Add all loaded Channels to Treeview
                    for channel in channels:
                        new_channel = channel_tree.insert('', 'end', text='1', values=channel)
                        channel_tree.selection_set(new_channel)

                    modify_channel_info(root_desc, root_id, root_wh, description)
                else:
                    messagebox.showerror('Primary Key Collision', 'Please make sure to enter a unique description.')
            else:
                messagebox.showerror('Invalid Field', 'Please make sure to enter valid information that meets these requirements:\n\nDescription must be alphanumerical.\nWebhook must be a valid link.')
        else:
            messagebox.showerror('Invalid Field', 'Please make sure to enter valid information that meets these requirements:\n\nDescription must be alphanumerical.\nWebhook must be a valid link.')
    else:
        messagebox.showerror('Invalid Field', 'Please make sure to select a channel.')

#Delete Channel Button Event
def delete_channel_btn(channel_tree, root_desc, root_id, root_wh):
    selection = channel_tree.selection() #Get the selected item of the tree

    if selection: #If channel from tree is selected
        response = messagebox.askquestion('Delete Channel', 'Are you sure you want to delete the channel?')

        if response == 'yes':
            #Get the selected channel description
            data = channel_tree.item(selection)['values'][0]

            if data:
                delete_channel(data)
                modify_channel_info(root_desc, root_id, root_wh, '')

            channel_tree.delete(*channel_tree.get_children()) 
            channels = load_channel()

            #Add all loaded Channels to Treeview
            for channel in channels:
                channel_tree.insert('', 'end', text='1', values=channel)
    else:
        messagebox.showerror('Invalid Channel', 'Please make sure to select a channel.')

#Function to modify the channel information display
def modify_channel_info(description_entry, id_entry, webhook_entry, description):
    #Allow modification of the fields
    description_entry.configure(state='normal')
    id_entry.configure(state='normal')
    webhook_entry.configure(state='normal')

    #Delete current data in the fields
    description_entry.delete(0, 'end')
    id_entry.delete(0, 'end')
    webhook_entry.delete(0, 'end')

    #If description is not empty load the channel info
    if description != '':
        channel_info = load_channel_by_description(description)

        if channel_info: #If the channel was found
            description_entry.insert(0, channel_info[0])
            id_entry.insert(0, channel_info[1])
            webhook_entry.insert(0, channel_info[2])

    #Disable modifcation of the fields
    description_entry.configure(state='disable')
    id_entry.configure(state='disable')
    webhook_entry.configure(state='disable')

#Function to start Telegram session
def start_session():
    if os.path.exists('./config.json'): #Check if configuration file exists
        global telegram_client #Access global client
        telegram_client = initialize()

        if telegram_client: #If Telegram session has been started
            messagebox.showinfo('Session Started', 'A session has been successfully started.')
        else:
            messagebox.showerror('Invalid Credentials', 'A session could not be started due to invalid credentials.')
    else:
        messagebox.showerror('Missing API Credentials', 'The API credentials have not been specified.')

#Function to start listening to Telegram messages
def start_listening(root):
    if telegram_client: #If Telegram session has been started
        if is_channels_populated(): #Check to see if there was any channels added
            root.destroy() #Destroy application, begin listening through console
            listen(telegram_client)
        else:
            messagebox.showerror('Empty Directory', 'There must be at least one channel added to start listening.')
    else:
        messagebox.showerror('Invalid Session', 'A Telegram session must be started before listening.')