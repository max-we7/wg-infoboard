import feedparser

url = "https://www.tagesschau.de/xml/rss2_https/"
feed = feedparser.parse(url)
news = "<news>"

for entry in feed.entries:
    try:
        title = entry['title']
        description = entry['content'][1]['value']
        start_index = str(entry['content'][0]['value']).find("src")
        url_beginning = (entry['content'][0]['value'][start_index+5:])
        index2 = str(url_beginning).find("/>")
        url = url_beginning[:index2-2]

        # filter articles with question mark in title
        if not str(title).__contains__("?") and not str(title).__contains__("Live"):
            news += f"<item><title>{title}</title>"
            news += f"<description>{description}</description>"
            news += f"<photo>{url}</photo></item>"
    except Exception:
        pass

news += "</news>"

try:
    with open(f"../../data/newsfeed.xml", "w") as f:
        f.write(news)
except FileNotFoundError:
    pass
