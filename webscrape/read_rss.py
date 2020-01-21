import feedparser
import json


def dump_to_json(data):
    """
    write news to JSON file
    """
    path = "../data/news.json"
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
    titles.append(entry[i].title)

dump_to_json(titles)
# print(titles)
# print(len(titles))



