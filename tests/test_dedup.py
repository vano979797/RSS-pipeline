from models import Article
from steps.dedup import drop_duplicates, normalize_title


def _article(title: str, url: str) -> Article:
    return Article(title=title, url=url, text="x" * 50, source="test")


def test_normalize_title_ignores_punctuation_and_case():
    assert normalize_title("Hello, World!!!") == "hello world"


def test_same_url_is_duplicate():
    items = [
        _article("A", "https://ex.com/news/1/"),
        _article("A copy", "https://ex.com/news/1"),
    ]
    assert len(drop_duplicates(items)) == 1


def test_same_title_different_url_is_duplicate():
    items = [
        _article("Big News", "https://a.com/1"),
        _article("big news!!!", "https://b.com/2"),
    ]
    assert len(drop_duplicates(items)) == 1


def test_different_stories_stay():
    items = [
        _article("Alpha", "https://a.com/1"),
        _article("Beta", "https://b.com/2"),
    ]
    assert len(drop_duplicates(items)) == 2
