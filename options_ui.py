import customtkinter as ctk

def create_options_frame(root):
    root.options_frame = ctk.CTkFrame(root)
    root.options_frame.pack_propagate(False)

    # Titre
    ctk.CTkLabel(root.options_frame, text="Options", font=("Verdana", 20)).pack(pady=20)

    # Frame pour la langue
    lang_frame = ctk.CTkFrame(root.options_frame)
    lang_frame.pack(pady=30, padx=50, fill="x")

    lang_frame.columnconfigure(0, weight=0)
    lang_frame.columnconfigure(1, weight=1)

    ctk.CTkLabel(lang_frame, text="Language:", font=("Verdana", 16)).grid(row=0, column=0, sticky="w", padx=10, pady=5)

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
    root.language_menu.set("French")
    root.selected_lang = "fr"
    root.language_menu.grid(row=0, column=1, sticky="e", padx=10, pady=5)

    # Bouton Back
    def back_to_main():
        root.options_frame.pack_forget()
        root.article_frame.pack(padx=10, pady=10, fill="both", expand=True)
        root.date_frame.pack(pady=10, fill="x")

    ctk.CTkButton(
        root.options_frame,
        text="Back",
        command=back_to_main,
        corner_radius=12,
        fg_color="#1f6aa5",
        hover_color="#144870",
        font=("Verdana", 14)
    ).pack(pady=20)

    return root.options_frame
