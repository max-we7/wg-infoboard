import feedparser
import json
from random import shuffle


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


def update_news():
    # Topics: WORLD NATION BUSINESS TECHNOLOGY ENTERTAINMENT SPORTS SCIENCE HEALTH
    feed1 = feedparser.parse("https://news.google.com/news/rss/headlines/section/topic/WORLD?hl=de&gl=DE&ceid=DE%3Asv").entries
    feed2 = feedparser.parse("https://news.google.com/news/rss/headlines/section/topic/NATION?hl=de&gl=DE&ceid=DE%3Asv").entries
    feed3 = feedparser.parse("https://news.google.com/news/rss/headlines/section/topic/BUSINESS?hl=de&gl=DE&ceid=DE%3Asv").entries
    feed4 = feedparser.parse("https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?hl=de&gl=DE&ceid=DE%3Asv").entries
    feed5 = feedparser.parse("https://news.google.com/news/rss/headlines/section/topic/SCIENCE?hl=de&gl=DE&ceid=DE%3Asv").entries

    titles = []

    for feed in [feed1, feed2, feed3, feed4, feed5]:
        for i in range(len(feed)):
            if not str(feed[i].title).__contains__("BILD"):
                titles.append(feed[i].title)
    shuffle(titles)

    dump_to_json(titles)

    with open("../data/news_unsanitized.json", "r", encoding="utf-8") as input:
        with open("../data/news.json", "w", encoding="utf-8") as output:
            document = json.load(input)
            json.dump(document, output, ensure_ascii=False, indent=2)
