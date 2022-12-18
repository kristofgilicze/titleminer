def get_most_common_words(titles):
    # Create an empty dictionary to store word frequencies
    word_counts = {}
    for title in titles:
        # Split the title into a list of words
        words = title.split()
        # Increment the count for each word
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
    # Sort the dictionary by value in descending order
    sorted_word_counts = dict(
        sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    )
    return sorted_word_counts


def lowercase_titles(titles: list[str]):
    return [title.lower() for title in titles]


def filter_common_words(data: dict) -> dict:
    COMMON_WORDS = [
        "több",
        "éves",
        "szerint",
        "volt",
        "meg",
        "minden",
        "jó",
        "-",
        "videó",
        "kép",
        "A",
        "a",
        "az",
        "és",
        "is",
        "nem",
        "van",
        "azt",
        "egy",
        "nagy",
        "hogy",
        "még",
        "kell",
        "volt",
        "nincs",
        "itt",
        "már",
        "miatt",
    ]

    # filter out common words
    for word in COMMON_WORDS:
        data.pop(word, None)

    return data
