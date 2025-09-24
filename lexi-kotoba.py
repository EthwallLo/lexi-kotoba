import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

def extract_kanji_with_furigana(url: str) -> list[tuple[str, str]]:
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", class_="article-title")
    if not title_tag:
        return []

    results = []
    for ruby in title_tag.find_all("ruby"):
        rb_text = "".join([t for t in ruby.contents if t.name != "rt" and isinstance(t, str)])
        rt_tag = ruby.find("rt")
        rt_text = rt_tag.get_text(strip=True) if rt_tag else ""
        if rb_text.strip():
            results.append((rb_text.strip(), rt_text))
    return results

def get_translation(word: str) -> str:
    """Récupère la définition en anglais sur Jisho puis traduit en français."""
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    r = requests.get(url)
    if r.status_code != 200:
        return "Pas de traduction trouvée"

    data = r.json()
    if data["data"]:
        senses = data["data"][0]["senses"]
        english_defs = senses[0]["english_definitions"]
        english_text = ", ".join(english_defs)

        # Traduction automatique vers le français
        french_text = GoogleTranslator(source="en", target="fr").translate(english_text)
        return french_text
    return "Pas de traduction trouvée"

url = "https://www3.nhk.or.jp/news/easy/ne2025092212004/ne2025092212004.html"
kanji_furigana = extract_kanji_with_furigana(url)

for kanji, furigana in kanji_furigana:
    traduction = get_translation(kanji)
    print(f"{kanji} ({furigana}) → {traduction}")
