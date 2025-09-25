import customtkinter as ctk
from datetime import datetime
from datepicker import pick_date
from articles import fetch_articles, articles_links, checkboxes
from display_vocab import display_secondpage
from tkinter import PhotoImage
from options_ui import create_options_frame  # import de la page Options

def create_main_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # --- Création de la fenêtre ---
    root = ctk.CTk()
    root.title("Lexi-Kotoba")

    window_width = 900
    window_height = 550
    root.resizable(False, False)

    # --- Centrage sur l'écran où se trouve la souris ---
    root.update_idletasks()
    mouse_x = root.winfo_pointerx()
    mouse_y = root.winfo_pointery()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = mouse_x - window_width // 2
    y = mouse_y - window_height // 2

    # Empêche la fenêtre de dépasser les bords
    x = max(0, min(x, screen_width - window_width))
    y = max(0, min(y, screen_height - window_height))

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # --- Icône ---
    icon = PhotoImage(file="kotoba.png")
    root.iconphoto(False, icon)

    # --- PAGE 1 ---
    root.article_frame = ctk.CTkScrollableFrame(root, width=850, height=300)
    root.article_frame.pack(padx=10, pady=10, fill="both", expand=True)

    root.date_frame = ctk.CTkFrame(root)
    root.date_frame.pack(pady=10, fill="x")

    root.date_frame.columnconfigure(0, weight=0)
    root.date_frame.columnconfigure(1, weight=1)
    root.date_frame.columnconfigure(2, weight=0)
    root.date_frame.columnconfigure(3, weight=0)
    root.date_frame.columnconfigure(4, weight=0)

    # Boutons Select, Search, Next
    root.date_button = ctk.CTkButton(
        root.date_frame,
        text="Select a date / period",
        font=("Verdana", 14),
        command=lambda: pick_date(root),
        corner_radius=12
    )
    root.date_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    root.date_label = ctk.CTkLabel(root.date_frame, text="No date selected", font=("Verdana", 14))
    root.date_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    ctk.CTkButton(
        root.date_frame,
        text="Search",
        command=lambda: fetch_articles(root),
        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#144870",
        font=("Verdana", 14)
    ).grid(row=0, column=2, padx=5, pady=5, sticky="e")

    ctk.CTkButton(
        root.date_frame,
        text="Next",
        command=lambda: display_secondpage(root),
        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#144870",
        font=("Verdana", 14)
    ).grid(row=0, column=3, padx=5, pady=5, sticky="e")

    # --- BOUTON OPTIONS ---
    root.selected_lang = "en"  # par défaut
    root.options_frame = create_options_frame(root)  # création de la page Options

    def open_options():
        root.article_frame.pack_forget()
        root.date_frame.pack_forget()
        root.options_frame.pack(fill="both", expand=True)

    root.settings_button = ctk.CTkButton(
        root.date_frame,
        text="Options",
        command=open_options,
        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#144870",
        font=("Verdana", 14)
    )
    root.settings_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # --- PAGE 2 (vocabulaire) ---
    root.page2_frame = ctk.CTkFrame(root)
    root.page2_text = ctk.CTkTextbox(root.page2_frame, width=780, height=400, font=("Verdana", 18))
    root.page2_text.pack(padx=10, pady=10, fill="both", expand=True)
    root.page2_text.configure(state="disabled")

    root.button_frame2 = ctk.CTkFrame(root.page2_frame)
    root.button_frame2.pack(pady=10)

    from display_vocab import previous, fetch_vocabulary

    ctk.CTkButton(
        root.button_frame2,
        text="Previous",
        command=lambda: previous(root),
        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#144870",
        font=("Verdana", 14)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        root.button_frame2,
        text="Fetch vocabulary",
        command=lambda: fetch_vocabulary(root),
        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#144870",
        font=("Verdana", 14)
    ).pack(side="left", padx=5)

    return root
