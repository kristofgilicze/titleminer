import logging
import click
import tabulate

from titleminer.crawl import fetch_rss, extract_titles
from titleminer.process import (
    filter_common_words,
    get_most_common_words,
    lowercase_titles,
)

from wordcloud import WordCloud
from PIL import Image

RSS_FEEDS = []

__version__ = "0.0.1"

logger = logging.getLogger(__name__)


@click.command()
@click.argument("rss_feeds", type=click.types.File("r"), default="feeds.txt")
@click.option("--generate-wordcloud", is_flag=True, help="Generate a wordcloud")
@click.option("--wordcloud-file", default="wordcloud.png", help="Wordcloud filename")
@click.option("--wordcloud-max-words", default=50, help="Max words in wordcloud")
@click.version_option(version=__version__)
def root(
    rss_feeds, generate_wordcloud: bool, wordcloud_file: str, wordcloud_max_words: int
):
    """Titleminer is a tool to mine the most common words from RSS feeds"""
    rss_feeds = [line.strip() for line in rss_feeds.readlines()]

    most_common_words = {}

    for rss_feed_url in rss_feeds:
        click.secho(f"Processing {rss_feed_url}", fg="green")
        articles = fetch_rss(rss_feed_url)
        titles = extract_titles(articles)
        lowercased_titles = lowercase_titles(titles)
        most_common_words = get_most_common_words(lowercased_titles)
        filtered_most_common_words = filter_common_words(most_common_words)
        ten_most_common_words_as_dict = dict(
            sorted(
                filtered_most_common_words.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:10]
        )
        tbl = tabulate.tabulate(
            [
                [key, ten_most_common_words_as_dict[key]]
                for key in ten_most_common_words_as_dict
            ],
            headers=["Word", "Count"],
        )
        click.secho(tbl, fg="white")

        for word in filtered_most_common_words:
            most_common_words[word] = filtered_most_common_words[word]

    sorted_most_common_words = dict(
        sorted(most_common_words.items(), key=lambda item: item[1], reverse=True)
    )

    if generate_wordcloud:
        cloud = WordCloud(
            background_color="white",
            width=1000,
            height=1000,
            max_words=wordcloud_max_words,
            max_font_size=300,
            random_state=42,
        ).generate_from_frequencies(sorted_most_common_words)

        img = cloud.to_image()
        img.save(wordcloud_file)
        click.secho("Generated wordcloud at ./wordcloud.png", fg="yellow")
