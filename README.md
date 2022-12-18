# What is titleminer?

titleminer is a tool for extracting titles from a set of news pages.
It is a command line tool that takes a list of URLs as input and outputs a list of titles.
It is written in Python and uses the [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) library for parsing HTML.

# Installation

titleminer requires Python 3.10 and poetry.

To install titleminer, run the following commands:

    poetry install

# Usage

titleminer takes a list of URLs in a text file and outputs the most common words in the titles of the web pages to the console.
    
        poetry run titleminer feeds.txt

It is possible to generate wordcloud with --wordcloud option.

        poetry run titleminer feeds.txt --wordcloud

See the help for more options:

        poetry run titleminer --help

