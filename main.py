import tkinter as tk
from tkinter_functions import main_page_click
from sqlite_functions import create_tables

def main():
    #Execute function to create SQLite tables to store the added channels
    create_tables()

    #Initialize Tkinter window, set default size, and application name
    root = tk.Tk()
    root.title('Telegram to Discord App')
    root.resizable(width=False, height=False)

    #Run Tkinter application continously and show the application's main window
    main_page_click(root)
    root.mainloop()

if __name__ == '__main__':
    main()