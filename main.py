import tkinter as tk
from tkinter_functions import main_page_click
from tkinter import ttk

from telegram_functions import initialize, listen

def main():
    # Initialize client with config data
    telegram_client = initialize()

    root = tk.Tk()
    root.minsize(250, 125)
    root.maxsize(400, 400)
    root.title("Telegram to Discord App")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')


    infor_frame = tk.Frame(root)
    manage_frame = tk.Frame(root)

    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    main_page_click(root, frame, telegram_client)
    root.mainloop()

if __name__ == '__main__':
    main()
