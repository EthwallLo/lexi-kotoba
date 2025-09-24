import requests

# URL de l'API NHK Easy
url = "https://www3.nhk.or.jp/news/easy/news-list.json"

response = requests.get(url)
data = response.json()  # c'est une liste

# Demander à l'utilisateur d'entrer une date
target_date = input("Entrez la date au format YYYY-MM-DD : ").strip()

# Parcourir tous les éléments de la liste pour trouver la date
found = False
for item in data:
    if target_date in item:
        articles = item[target_date]
        for i, article in enumerate(articles):
            print(f"{i}: {article.get('news_web_url')}")
        found = True
        break

if not found:
    print(f"Aucun article trouvé pour la date {target_date}")
