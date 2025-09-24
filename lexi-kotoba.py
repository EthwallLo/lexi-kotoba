import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def extract_kanji_with_furigana(url: str) -> list[tuple[str, str]]:
    """
    Extrait tous les mots du titre et du corps de l'article avec kanji + furigana.
    Dans le corps, si un <ruby> est dans un mot plus grand, on prend le mot entier.
    Les ruby isolés déjà inclus dans un mot complet sont ignorés.
    """
    response = requests.get(url)
    response.encoding = response.apparent_encoding
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
            # Cherche tous les ruby dans le container
            for ruby in container.find_all("ruby"):
                parent = ruby.parent
                # Vérifie si le ruby est suivi de texte dans le parent
                following_text = ""
                for elem in ruby.next_siblings:
                    if isinstance(elem, str):
                        following_text += elem
                    elif elem.name == "rt":
                        continue
                    elif elem.string:
                        following_text += elem.string

                if following_text:
                    # mot complet = kanji du ruby + texte qui suit
                    kanji = "".join([t for t in ruby.contents if t.name != "rt" and isinstance(t, str)]) + following_text
                    furigana = (ruby.find("rt").get_text(strip=True) if ruby.find("rt") else "") + following_text
                    results.append((kanji, furigana))
                else:
                    # Ruby seul dans le corps (pas suivi par texte) -> on l'ajoute
                    kanji = "".join([t for t in ruby.contents if t.name != "rt" and isinstance(t, str)])
                    furigana = ruby.find("rt").get_text(strip=True) if ruby.find("rt") else ""
                    results.append((kanji, furigana))

    return results

def get_translation(word: str) -> str:
    """Récupère la définition en anglais sur Jisho puis traduit en français."""
    try:
        url = f"https://jisho.org/api/v1/search/words?keyword={word}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        if data["data"]:
            senses = data["data"][0]["senses"]
            english_defs = senses[0]["english_definitions"]
            english_text = ", ".join(english_defs)
            french_text = GoogleTranslator(source="en", target="fr").translate(english_text)
            return french_text
        return "Pas de traduction trouvée"
    except Exception as e:
        return f"Erreur : {e}"

# --- Utilisation ---
url = "https://www3.nhk.or.jp/news/easy/ne2025092212004/ne2025092212004.html"
kanji_furigana = extract_kanji_with_furigana(url)

# --- Supprimer les doublons par paire (kanji, furigana) ---
seen = set()
for kanji, furigana in kanji_furigana:
    pair = (kanji, furigana)
    if pair not in seen:
        seen.add(pair)
        traduction = get_translation(kanji)
        print(f"{kanji} ({furigana}) → {traduction}")
