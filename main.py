import tkinter as tk
from tkinter_functions import main_page_click
from telegram_functions import initialize, listen

def main():
    #Initialize Tkinter window, set default size, and application name
    root = tk.Tk()
    root.title("Telegram to Discord App")
    root.resizable(width=False, height=False)

    main_page_click(root)    
    root.mainloop()

if __name__ == '__main__':
    main()
