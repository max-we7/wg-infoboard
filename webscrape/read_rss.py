import feedparser
import json


def dump_to_json(data):
    """
    write news to JSON file
    """
    path = "../data/news_unsanitized.json"
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError as exception:
        print("Error")


NewsFeed = feedparser.parse("https://news.google.com/news/rss?hl=de&gl=DE&ceid=DE%3Asv")
entry = NewsFeed.entries

titles = []

for i in range(len(entry)):
    # print(entry.keys())
    # print(entry[i].title)
    if not str(entry[i].title).__contains__("BILD"):
        titles.append(entry[i].title)
    else:
        titles.append("An dieser Stelle wurde ein BILD-Artikel zensiert ;-)")

dump_to_json(titles)
# print(titles)
# print(len(titles))


with open("../data/news_unsanitized.json", "r", encoding="utf-8") as input:
    with open("../data/news.json", "w", encoding="utf-8") as output:
        document = json.load(input)
        json.dump(document, output, ensure_ascii=False, indent=2)