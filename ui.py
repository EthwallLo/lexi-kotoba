import customtkinter as ctk
from datetime import datetime
from datepicker import pick_date
from articles import fetch_articles, articles_links, checkboxes
from page2 import afficher_page2

def create_main_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("NHK Easy Articles")
    root.geometry("900x550")
    root.resizable(False, False)

    # Page 1
    root.article_frame = ctk.CTkScrollableFrame(root, width=850, height=300)
    root.article_frame.pack(padx=10, pady=10, fill="both", expand=True)

    root.date_frame = ctk.CTkFrame(root)
    root.date_frame.pack(pady=10, fill="x")

    root.date_button = ctk.CTkButton(root.date_frame, text="Choisir une date/période",
                                     command=lambda: pick_date(root), corner_radius=12)
    root.date_button.pack(side="left", padx=5)

    root.date_label = ctk.CTkLabel(root.date_frame, text="Aucune date sélectionnée", font=("Verdana", 14))
    root.date_label.pack(side="left", padx=10)

    root.button_frame = ctk.CTkFrame(root)
    root.button_frame.pack(pady=15)

    ctk.CTkButton(root.button_frame, text="Rechercher", command=lambda: fetch_articles(root),
                   corner_radius=12, fg_color="#1f6aa5", hover_color="#144870",
                   font=("Verdana", 14)).pack(side="left", padx=5)

    ctk.CTkButton(root.button_frame, text="Suivant", command=lambda: afficher_page2(root),
                   corner_radius=12, fg_color="#1f6aa5", hover_color="#144870",
                   font=("Verdana", 14)).pack(side="left", padx=5)

    # Page 2
    root.page2_frame = ctk.CTkFrame(root)
    root.page2_text = ctk.CTkTextbox(root.page2_frame, width=780, height=400, font=("Verdana", 14))
    root.page2_text.pack(padx=10, pady=10, fill="both", expand=True)
    root.page2_text.configure(state="disabled")

    root.button_frame2 = ctk.CTkFrame(root.page2_frame)
    root.button_frame2.pack(pady=10)

    from page2 import precedent, recuperer_vocabulaire

    ctk.CTkButton(root.button_frame2, text="Précédent", command=lambda: precedent(root),
                   corner_radius=12, fg_color="#1f6aa5", hover_color="#144870", font=("Verdana", 14)).pack(side="left", padx=5)
    ctk.CTkButton(root.button_frame2, text="Récupérer le vocabulaire",
                   command=lambda: recuperer_vocabulaire(root),
                   corner_radius=12, fg_color="#1f6aa5", hover_color="#144870", font=("Verdana", 14)).pack(side="left", padx=5)

    return root
