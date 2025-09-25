import customtkinter as ctk
from display_vocab import previous, fetch_vocabulary

def create_vocab_page(root):
    root.page2_frame = ctk.CTkFrame(root)
    root.page2_text = ctk.CTkTextbox(root.page2_frame, width=780, height=400, font=("Verdana", 18))
    root.page2_text.pack(padx=10, pady=10, fill="both", expand=True)
    root.page2_text.configure(state="disabled")

    root.button_frame2 = ctk.CTkFrame(root.page2_frame)
    root.button_frame2.pack(pady=10)

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
