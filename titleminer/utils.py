import csv
from titleminer.models import Medium

def senitment_to_csv(mediums: list[Medium], filename: str):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["medium", "title", "sentiment"])
        for medium in mediums:
            for title in mediums[medium].positive_titles:
                writer.writerow([medium, title, "positive"])
            for title in mediums[medium].neutral_titles:
                writer.writerow([medium, title, "neutral"])
            for title in mediums[medium].negative_titles:
                writer.writerow([medium, title, "negative"])
