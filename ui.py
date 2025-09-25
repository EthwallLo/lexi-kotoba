import customtkinter as ctk
from datetime import datetime
from datepicker import pick_date
from articles import fetch_articles, articles_links, checkboxes
from display_vocab import display_secondpage
from tkinter import PhotoImage  

def create_main_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Lexi-Kotoba")
    root.geometry("900x550")
    root.resizable(False, False)
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
        root.date_frame, text="Select a date / period", font=("Verdana", 14),
        command=lambda: pick_date(root), corner_radius=12
    )
    root.date_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    root.date_label = ctk.CTkLabel(root.date_frame, text="No date selected", font=("Verdana", 14))
    root.date_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    ctk.CTkButton(
        root.date_frame, text="Search",
        command=lambda: fetch_articles(root),
        corner_radius=12, fg_color="#1f6aa5", hover_color="#144870",
        font=("Verdana", 14)
    ).grid(row=0, column=2, padx=5, pady=5, sticky="e")

    ctk.CTkButton(
        root.date_frame, text="Next",
        command=lambda: display_secondpage(root),
        corner_radius=12, fg_color="#1f6aa5", hover_color="#144870",
        font=("Verdana", 14)
    ).grid(row=0, column=3, padx=5, pady=5, sticky="e")

    # --- BOUTON OPTIONS ---
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

    root.selected_lang = "en"  # par défaut

    # --- PAGE 2 (vocabulaire) ---
    root.page2_frame = ctk.CTkFrame(root)
    root.page2_text = ctk.CTkTextbox(root.page2_frame, width=780, height=400, font=("Verdana", 18))
    root.page2_text.pack(padx=10, pady=10, fill="both", expand=True)
    root.page2_text.configure(state="disabled")

    root.button_frame2 = ctk.CTkFrame(root.page2_frame)
    root.button_frame2.pack(pady=10)

    from display_vocab import previous, fetch_vocabulary

    ctk.CTkButton(
        root.button_frame2, text="Previous",
        command=lambda: previous(root),
        corner_radius=12, fg_color="#1f6aa5", hover_color="#144870",
        font=("Verdana", 14)
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        root.button_frame2, text="Fetch vocabulary",
        command=lambda: fetch_vocabulary(root),
        corner_radius=12, fg_color="#1f6aa5", hover_color="#144870",
        font=("Verdana", 14)
    ).pack(side="left", padx=5)

    # --- PAGE 3 (OPTIONS) ---
    root.options_frame = ctk.CTkFrame(root)
    root.options_frame.pack_propagate(False)

    # Titre
    ctk.CTkLabel(root.options_frame, text="Options", font=("Verdana", 20)).pack(pady=20)

    # Frame pour la langue
    lang_frame = ctk.CTkFrame(root.options_frame)
    lang_frame.pack(pady=30, padx=50, fill="x")

    # Colonne 0 = label, colonne 1 = OptionMenu
    lang_frame.columnconfigure(0, weight=0)  # label à gauche
    lang_frame.columnconfigure(1, weight=1)  # OptionMenu à droite

    # Label
    ctk.CTkLabel(lang_frame, text="Language:", font=("Verdana", 16)).grid(row=0, column=0, sticky="w", padx=10, pady=5)

    # OptionMenu
    language_values = ["English", "French", "Spanish", "German"]
    language_codes = {"English": "en", "French": "fr", "Spanish": "es", "German": "de"}

    def set_language_from_optionmenu(choice):
        root.selected_lang = language_codes[choice]

    root.language_menu = ctk.CTkOptionMenu(
        lang_frame,
        values=language_values,
        command=set_language_from_optionmenu,
        font=("Verdana", 16),
        button_color="#1f6aa5",
        button_hover_color="#144870"
    )
    root.language_menu.set("French")  # valeur par défaut
    root.selected_lang = "fr"
    root.language_menu.grid(row=0, column=1, sticky="e", padx=10, pady=5)

    # --- Fonction pour revenir à la page principale ---
    def back_to_main():
        root.options_frame.pack_forget()
        root.article_frame.pack(padx=10, pady=10, fill="both", expand=True)
        root.date_frame.pack(pady=10, fill="x")

    # --- Bouton Back ---
    ctk.CTkButton(
        root.options_frame,
        text="Back",
        command=back_to_main,  # <-- utiliser la fonction définie
        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#144870",
        font=("Verdana", 14)
    ).pack(pady=20)

    return root
