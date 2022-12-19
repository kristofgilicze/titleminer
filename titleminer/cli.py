import logging
import random
import click
import time
import tabulate
import os
import openai

from titleminer.crawl import fetch_rss, extract_titles
from titleminer.models import Medium
from titleminer.utils import senitment_to_csv
from titleminer.process import (
    remove_punctuation,
    remove_stopwords,
    get_most_common_words,
    lowercase_titles,
)

from wordcloud import WordCloud
from PIL import Image

RSS_FEEDS = []

__version__ = "0.0.1"

logger = logging.getLogger(__name__)

@click.group()
def root():
    pass


@root.command()
@click.argument("rss_feeds", type=click.types.File("r"), default="feeds.txt")
@click.option("--ignore-list", type=click.types.File("r"), default="ignore_list.txt")
@click.option("--generate-wordcloud", is_flag=True, help="Generate a wordcloud")
@click.option("--wordcloud-file", default="wordcloud.png", help="Wordcloud filename")
@click.option("--wordcloud-max-words", default=50, help="Max words in wordcloud")
@click.version_option(version=__version__)
def wordcloud(
    rss_feeds, ignore_list, generate_wordcloud: bool, wordcloud_file: str, wordcloud_max_words: int
):
    """Titleminer is a tool to mine the most common words from RSS feeds"""
    rss_feeds = [line.strip() for line in rss_feeds.readlines()]
    ignore_list = [line.strip() for line in ignore_list.readlines()]

    all_titles = []
    most_common_words = {}

    for rss_feed_url in rss_feeds:
        click.secho(f"Processing {rss_feed_url}", fg="green")
        articles = fetch_rss(rss_feed_url)
        titles = extract_titles(articles)
        lowercased_titles = lowercase_titles(titles)
        punctuation_removed = remove_punctuation(lowercased_titles)
        most_common_words = get_most_common_words(punctuation_removed)
        filtered_most_common_words = remove_stopwords(most_common_words, ignore_list)
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

        all_titles.extend(titles)

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



@root.command()
@click.argument("rss_feeds", type=click.types.File("r"), default="feeds.txt")
@click.option("--openai-key", required=True, help="OpenAI API key")
@click.option("--limit", default=2, help="Limit number of titles to process")
@click.version_option(version=__version__)
def sentiment(rss_feeds, openai_key: str, limit: int):
    openai.api_key = openai_key
    rss_feeds = [line.strip() for line in rss_feeds.readlines()]

    mediums = {}
    for rss_feed_url in rss_feeds:
        click.secho(f"Processing {rss_feed_url}", fg="green")
        articles = fetch_rss(rss_feed_url)
        mediums[rss_feed_url] = Medium(rss_feed_url)
        mediums[rss_feed_url].titles = extract_titles(articles)

    for medium in mediums:
        click.secho(f"\n# Medium: {medium}", fg="green")

        sampled = random.sample(mediums[medium].titles, limit)

        for title in sampled:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Decide whether a news title sentiment is positive, neutral, or negative.\n\nNews title: \"{title}\"\nSentiment: ",
                temperature=0,
                max_tokens=30,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0
            )
            click.secho(f"\n{title}", fg="white")
            sentiment = response.choices[0].text.strip().lower()

            match(sentiment):
                case "positive":
                    click.secho(sentiment, fg="green")
                    mediums[medium].positive_titles.append(title)
                case "neutral":
                    click.secho(sentiment, fg="yellow")
                    mediums[medium].neutral_titles.append(title)
                case "negative":
                    click.secho(sentiment, fg="red")
                    mediums[medium].negative_titles.append(title)
                case _:
                    click.secho(sentiment, fg="white")
            time.sleep(3)
            click.secho("")

    for medium in mediums:
        click.secho(f"\n# Medium: {medium}", fg="white")
        click.secho(f"Positive titles: {len(mediums[medium].positive_titles)}", fg="green")
        click.secho(f"Neutral titles: {len(mediums[medium].neutral_titles)}", fg="yellow")
        click.secho(f"Negative titles: {len(mediums[medium].negative_titles)}", fg="red")

    senitment_to_csv(mediums, "sentiment.csv")
