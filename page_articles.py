import customtkinter as ctk
from articles import fetch_articles, articles_links, checkboxes
from display_vocab import display_secondpage
from options_ui import create_options_frame

def create_articles_page(root):
    """
    Crée la page principale avec la liste des articles,
    le calendrier et les boutons Search, Next et Options.
    """

    # --- PAGE 1 ---
    root.article_frame = ctk.CTkScrollableFrame(root, width=850, height=300)
    root.article_frame.pack(padx=10, pady=10, fill="both", expand=True)

    root.date_frame = ctk.CTkFrame(root)
    root.date_frame.pack(pady=10, fill="x")

    root.date_frame.columnconfigure(0, weight=0)  # bouton Select
    root.date_frame.columnconfigure(1, weight=1)  # label occupe l’espace au milieu
    root.date_frame.columnconfigure(2, weight=0)  # bouton Search
    root.date_frame.columnconfigure(3, weight=0)  # bouton Next
    root.date_frame.columnconfigure(4, weight=0)  # bouton Options

    # --- Boutons Select, Search, Next ---
    from datepicker import pick_date
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
    # Créer le frame Options si pas déjà créé
    if not hasattr(root, "options_frame"):
        root.options_frame = create_options_frame(root)
        root.options_frame.pack_forget()  # cacher au départ

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
