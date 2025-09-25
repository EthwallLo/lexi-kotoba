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

    # Page 1
    root.article_frame = ctk.CTkScrollableFrame(root, width=850, height=300)
    root.article_frame.pack(padx=10, pady=10, fill="both", expand=True)
    root.date_frame = ctk.CTkFrame(root)
    root.date_frame.pack(pady=10, fill="x")

    root.date_frame.columnconfigure(0, weight=0)   # bouton Select
    root.date_frame.columnconfigure(1, weight=1)   # label occupe l’espace au milieu
    root.date_frame.columnconfigure(2, weight=0)   # bouton Search
    root.date_frame.columnconfigure(3, weight=0)   # bouton Next

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

    def set_language(root, lang):
        root.selected_lang = lang

    root.settings_button = ctk.CTkOptionMenu(
        root.date_frame,
        values=["fr", "en", "es", "de"],
        command=lambda lang: set_language(root, lang),
        font=("Verdana", 14),
        button_color="#1f6aa5",
        button_hover_color="#144870"
    )
    root.settings_button.set("en")  # langue par défaut
    root.selected_lang = "en"
    root.settings_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")

    # Page 2
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

    return root