"""ШАГ 4. Удаление дублей.

Одна новость живёт в нескольких лентах. Если не схлопнуть копии,
RAG будет доставать одно и то же три раза и казаться «глупым».

Два ключа, от простого к достаточному:
  1) URL  — это та же страница
  2) нормализованный заголовок — та же новость с другого зеркала
"""

from __future__ import annotations

import re

from models import Article

NOT_LETTERS = re.compile(r"[^\w\s]", flags=re.UNICODE)
SPACES = re.compile(r"\s+")


def normalize_title(title: str) -> str:
    """«Hello, World!!!» и «hello world» должны стать одним ключом."""
    lowered = (title or "").casefold().strip()
    without_punct = NOT_LETTERS.sub(" ", lowered)
    return SPACES.sub(" ", without_punct).strip()


def drop_duplicates(articles: list[Article]) -> list[Article]:
    """Оставить первую встречу, остальное выбросить."""
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[Article] = []

    for article in articles:
        url_key = article.url.rstrip("/").casefold()
        title_key = normalize_title(article.title)

        if url_key and url_key in seen_urls:
            continue
        if title_key and title_key in seen_titles:
            continue

        if url_key:
            seen_urls.add(url_key)
        if title_key:
            seen_titles.add(title_key)
        unique.append(article)

    return unique
