from dataclasses import dataclass, field

@dataclass
class Medium:
    rss_feed_url: str
    titles: list[str] = field(default_factory=list)
    positive_titles: list[str] = field(default_factory=list)
    negative_titles: list[str] = field(default_factory=list)
    neutral_titles: list[str] = field(default_factory=list)
