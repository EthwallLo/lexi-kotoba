import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def extract_kanji_with_furigana(url: str) -> list[tuple[str, str]]:
    """Extrait tous les mots du titre et du corps de l'article avec kanji + furigana."""
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
    """Récupère la définition sur Jisho. Si target_lang != 'en', traduit en conséquence."""
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
                return english_text  # On laisse en anglais
            else:
                return GoogleTranslator(source="en", target=target_lang).translate(english_text)
        return "Pas de traduction trouvée"
    except Exception as e:
        return f"Erreur : {e}"

# --- Interface utilisateur ---
url = input("Entrez l'URL de l'article NHK Easy à scanner : ").strip()
if not url:
    print("Aucune URL fournie. Fin du programme.")
    exit()

# Choix de la langue
lang_map = {
    "fr": "français",
    "en": "anglais",
    "es": "espagnol",
    "de": "allemand"
}

print("Langues disponibles : français (fr), anglais (en), espagnol (es), allemand (de)")
lang_choice = input("Choisissez la langue de traduction : ").strip().lower()
if lang_choice not in lang_map:
    print("Langue non reconnue, traduction par défaut en français.")
    lang_choice = "fr"

kanji_furigana = extract_kanji_with_furigana(url)

# --- Supprimer les doublons ---
seen = set()
for kanji, furigana in kanji_furigana:
    pair = (kanji, furigana)
    if pair not in seen:
        seen.add(pair)
        traduction = get_translation(kanji, lang_choice)
        print(f"{kanji} ({furigana}) → {traduction}")
