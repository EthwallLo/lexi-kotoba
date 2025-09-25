import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from tkinter import simpledialog, messagebox
from articles import articles_links, checkboxes

def extract_kanji_with_furigana(url: str):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
    except Exception as e:
        print(f"Erreur récupération article : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # --- Titre ---
    title_tag = soup.find("h1", class_="article-title")
    if title_tag:
        for ruby in title_tag.find_all("ruby"):
            kanji = "".join([t for t in ruby.contents if t.name != "rt" and isinstance(t, str)])
            rt_tag = ruby.find("rt")
            furigana = rt_tag.get_text(strip=True) if rt_tag else ""
            if kanji.strip():
                results.append((kanji.strip(), furigana))

    # --- Corps ---
    article_body = soup.find("div", class_="article-body")
    if article_body:
        for container in article_body.find_all(recursive=False):
            for ruby in container.find_all("ruby"):
                following_text = ""
                for elem in ruby.next_siblings:
                    if isinstance(elem, str):
                        following_text += elem
                    elif elem.name == "rt":
                        continue
                    elif elem.string:
                        following_text += elem.string

                if following_text:
                    kanji = "".join([t for t in ruby.contents if t.name != "rt" and isinstance(t, str)]) + following_text
                    furigana = (ruby.find("rt").get_text(strip=True) if ruby.find("rt") else "") + following_text
                    results.append((kanji, furigana))
                else:
                    kanji = "".join([t for t in ruby.contents if t.name != "rt" and isinstance(t, str)])
                    furigana = ruby.find("rt").get_text(strip=True) if ruby.find("rt") else ""
                    results.append((kanji, furigana))

    return results

def get_translation(word: str, target_lang: str) -> str:
    """
    Traduit un mot en utilisant l’API de Jisho + GoogleTranslator si besoin.
    """
    try:
        url = f"https://jisho.org/api/v1/search/words?keyword={word}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()

        if data["data"]:
            senses = data["data"][0]["senses"]
            english_defs = senses[0]["english_definitions"]
            english_text = ", ".join(english_defs)

            if target_lang == "en":
                return english_text
            else:
                return GoogleTranslator(source="en", target=target_lang).translate(english_text)

        return "Pas de traduction trouvée"
    except Exception as e:
        return f"Erreur : {e}"


def recuperer_vocabulaire(root):
    """
    Récupère le vocabulaire des articles sélectionnés,
    traduit les mots et affiche le résultat dans page2_text.
    """
    # 1️⃣ Articles sélectionnés
    selected_idxs = [idx for cb, idx in checkboxes if cb.var.get()]
    if not selected_idxs:
        messagebox.showinfo("Info", "Veuillez sélectionner au moins un article.")
        return

    # 2️⃣ Choix de la langue
    lang_choice = simpledialog.askstring(
        "Langue",
        "Choisissez la langue de traduction : fr, en, es, de",
        parent=root
    )
    if not lang_choice or lang_choice.lower() not in ("fr", "en", "es", "de"):
        messagebox.showinfo("Info", "Langue non reconnue, traduction par défaut en français.")
        lang_choice = "fr"
    else:
        lang_choice = lang_choice.lower()

    # 3️⃣ Parcours des articles et récupération vocabulaire
    vocab_text = ""
    for idx in selected_idxs:
        url = articles_links.get(idx)
        if not url:
            continue

        kanji_furigana = extract_kanji_with_furigana(url)

        seen = set()
        for kanji, furigana in kanji_furigana:
            if (kanji, furigana) not in seen:
                seen.add((kanji, furigana))
                traduction = get_translation(kanji, lang_choice)
                vocab_text += f"{kanji} ({furigana}) → {traduction}\n"

    # 4️⃣ Affichage dans la zone texte
    if vocab_text:
        root.page2_text.configure(state="normal")
        root.page2_text.delete("0.0", "end")
        root.page2_text.insert("end", vocab_text)
        root.page2_text.configure(state="disabled")
    else:
        messagebox.showinfo("Info", "Aucun vocabulaire trouvé.")
