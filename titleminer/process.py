import io


def get_most_common_words(titles):
    word_counts = {}
    for title in titles:
        words = title.split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

    sorted_word_counts = dict(
        sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    )
    return sorted_word_counts


def lowercase_titles(titles: list[str]) -> list[str]:
    return [title.lower() for title in titles]


def remove_stopwords(data: dict, ignore_list: list[str]) -> dict:
    for word in ignore_list:
        data.pop(word, None)

    return data

def remove_punctuation(titles: list[str]) -> list[str]:
    marks = [".", ",", ":", ";", "!", "?"]
    for mark in marks:
        titles = [title.replace(mark, "") for title in titles]
    return titles