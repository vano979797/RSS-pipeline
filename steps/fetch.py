"""ШАГ 1. Получение.

Идея: сходить в RSS (или News API) и вернуть list[Article].
Пока объект Article одинаковый, источнику всё равно, что будет дальше.

RSS — XML-лента. feedparser разбирает её в список entry.
У каждой entry обычно есть: title, link, summary/content, дата.
"""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import os

import feedparser
import requests

from models import Article

USER_AGENT = "news-pipeline/1.0 (portfolio project; python)"
TIMEOUT_SEC = 20


def _published_iso(entry: dict) -> str | None:
    """Дата в ISO, чтобы в Parquet лежало одно и то же, а не каша форматов."""
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        try:
            return datetime(*parsed[:6], tzinfo=timezone.utc).isoformat()
        except (TypeError, ValueError):
            pass

    raw = entry.get("published") or entry.get("updated")
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw).isoformat()
    except (TypeError, ValueError, IndexError):
        return str(raw)


def _raw_html(entry: dict) -> str:
    """RSS прячет текст то в summary, то в content. Берём что есть."""
    content = entry.get("content")
    if content:
        value = content[0].get("value")
        if value:
            return value
    return entry.get("summary") or entry.get("description") or ""


def fetch_feed(url: str, source: str) -> list[Article]:
    """Скачать один RSS и превратить записи в Article."""
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT_SEC,
    )
    response.raise_for_status()

    feed = feedparser.parse(response.content)
    articles: list[Article] = []

    for entry in feed.entries:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not title and not link:
            continue
        articles.append(
            Article(
                title=title,
                url=link,
                text=_raw_html(entry),
                source=source,
                published=_published_iso(entry),
            )
        )
    return articles


def fetch_all(feeds: list[tuple[str, str]]) -> list[Article]:
    """Обойти все источники. Один мёртвый фид не роняет весь пайплайн."""
    collected: list[Article] = []
    for source, url in feeds:
        try:
            batch = fetch_feed(url, source)
            print(f"    {source}: {len(batch)} статей")
            collected.extend(batch)
        except requests.RequestException as exc:
            print(f"    {source}: ошибка ({exc})")
    return collected


def fetch_newsapi(api_key: str, query: str = "technology") -> list[Article]:
    """Тот же выход list[Article], другой вход.

    News API — запасной вариант из задания. Пайплайн после fetch не меняется.
    Ключ кладётся в переменную окружения NEWSAPI_KEY, не в код.
    """
    response = requests.get(
        "https://newsapi.org/v2/everything",
        params={"q": query, "pageSize": 50, "language": "en"},
        headers={"X-Api-Key": api_key, "User-Agent": USER_AGENT},
        timeout=TIMEOUT_SEC,
    )
    response.raise_for_status()
    payload = response.json()

    articles: list[Article] = []
    for item in payload.get("articles") or []:
        title = (item.get("title") or "").strip()
        url = (item.get("url") or "").strip()
        if not title and not url:
            continue
        articles.append(
            Article(
                title=title,
                url=url,
                text=item.get("content") or item.get("description") or "",
                source=item.get("source", {}).get("name") or "NewsAPI",
                published=item.get("publishedAt"),
            )
        )
    return articles


def maybe_fetch_newsapi() -> list[Article]:
    key = os.getenv("NEWSAPI_KEY")
    if not key:
        return []
    try:
        batch = fetch_newsapi(key)
        print(f"    NewsAPI: {len(batch)} статей")
        return batch
    except requests.RequestException as exc:
        print(f"    NewsAPI: ошибка ({exc})")
        return []
