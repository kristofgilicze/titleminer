import requests
from bs4 import BeautifulSoup

RSS_FEEDS = {
    "telex": "https://telex.hu/rss",
    "444": "https://444.hu/feed",
    "index": "https://index.hu/24ora/rss/",
    "origo": "https://www.origo.hu/rss/origo.xml",
}


def fetch_rss(rss_feed_url: str):
    """Fetches the RSS feed and returns a list of articles"""
    response = requests.get(rss_feed_url)
    soup = BeautifulSoup(response.content, "xml")
    articles = soup.findAll("item")
    return articles


def extract_titles(articles) -> list[str]:
    return [article.title.text for article in articles]
