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
        print(f"Error fetching article : {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    title_tag = soup.find("h1", class_="article-title")
    if title_tag:
        for ruby in title_tag.find_all("ruby"):
            kanji = "".join([t for t in ruby.contents if t.name != "rt" and isinstance(t, str)])
            rt_tag = ruby.find("rt")
            furigana = rt_tag.get_text(strip=True) if rt_tag else ""
            if kanji.strip():
                results.append((kanji.strip(), furigana))

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
        return "No translation found"
    except Exception as e:
        return f"Erreur : {e}"

def fetch_vocabulary(root):
    selected_idxs = [idx for cb, idx in checkboxes if cb.var.get()]
    if not selected_idxs:
        messagebox.showinfo("Info", "Please select at least one article")
        return

    lang_choice = getattr(root, "selected_lang", "fr")  # utilise la langue configurée

    # Vide le textbox et le rend modifiable
    root.page2_text.configure(state="normal")
    root.page2_text.delete("1.0", "end")

    for idx in selected_idxs:
        url = articles_links.get(idx)
        if not url:
            continue

        kanji_furigana = extract_kanji_with_furigana(url)

        # Lire les mots déjà présents dans le fichier
        existing_words = set()
        try:
            with open("words.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if " - " in line:
                        existing_words.add(tuple(line.split(" - ", 1)))  # (kanji, furigana)
        except FileNotFoundError:
            pass  # si le fichier n'existe pas encore

        seen = set()
        with open("words.txt", "a", encoding="utf-8") as f:  # 'a' pour ajouter
            for kanji, furigana in kanji_furigana:
                if (kanji, furigana) not in seen:
                    seen.add((kanji, furigana))
                    traduction = get_translation(kanji, lang_choice)

                    # Vérifier si le mot est nouveau
                    is_new = (kanji, furigana) not in existing_words
                    new_indicator = " [!]" if is_new else ""

                    line = f"{kanji} ({furigana}) → {traduction}{new_indicator}\n"

                    # Affichage ligne par ligne dans le textbox
                    root.page2_text.insert("end", line)
                    root.page2_text.see("end")
                    root.page2_text.update()

                    # Ajouter au fichier seulement si pas déjà présent
                    if is_new:
                        f.write(f"{kanji} - {furigana}\n")
                        existing_words.add((kanji, furigana))
                                  
    root.page2_text.configure(state="disabled")
