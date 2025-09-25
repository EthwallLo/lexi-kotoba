import customtkinter as ctk
from tkinter import PhotoImage
from page_articles import create_articles_page
from page_vocab import create_vocab_page
from options_ui import create_options_frame

def create_main_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Lexi-Kotoba")
    window_width = 900
    window_height = 550
    root.resizable(False, False)

    # Centrer sur l'écran de la souris
    root.update_idletasks()
    mouse_x = root.winfo_pointerx()
    mouse_y = root.winfo_pointery()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = max(0, min(mouse_x - window_width // 2, screen_width - window_width))
    y = max(0, min(mouse_y - window_height // 2, screen_height - window_height))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Icône
    icon = PhotoImage(file="kotoba.png")
    root.iconphoto(False, icon)

    # Pages
    create_articles_page(root)
    create_vocab_page(root)
    create_options_frame(root)

    return root
