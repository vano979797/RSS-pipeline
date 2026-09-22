"""Карта всего проекта. Читай этот файл первым.

получение → очистка html → язык → дубли → Parquet

Каждая стрелка — функция из steps/. Здесь мы только зовём их по порядку
и печатаем, сколько статей осталось после шага. Это и есть ETL.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from config import MIN_TEXT_LEN, OUTPUT_FILE, RSS_FEEDS
from models import Article
from steps.clean import clean_html
from steps.dedup import drop_duplicates
from steps.fetch import fetch_all, maybe_fetch_newsapi
from steps.language import detect_language
from steps.save import save_parquet


def _print_languages(articles: list[Article]) -> None:
    counts = Counter(article.language or "unknown" for article in articles)
    pretty = ", ".join(f"{lang}={n}" for lang, n in counts.most_common())
    print(f"    языки: {pretty}")


def run_pipeline(
    feeds: list[tuple[str, str]] | None = None,
    output: Path | None = None,
    min_text_len: int = MIN_TEXT_LEN,
) -> Path:
    feeds = feeds or RSS_FEEDS
    output = output or OUTPUT_FILE

    print("[1/5] Получение RSS")
    articles = fetch_all(feeds)
    articles.extend(maybe_fetch_newsapi())
    print(f"    всего сырых: {len(articles)}")

    print("[2/5] Очистка HTML")
    cleaned: list[Article] = []
    for article in articles:
        article.text = clean_html(article.text)
        if not article.text:
            article.text = clean_html(article.title)
        if len(article.text) >= min_text_len:
            cleaned.append(article)
    articles = cleaned
    print(f"    после фильтра коротких: {len(articles)}")

    print("[3/5] Определение языка")
    for article in articles:
        article.language = detect_language(article.text)

    print("[4/5] Удаление дублей")
    before = len(articles)
    articles = drop_duplicates(articles)
    print(f"    убрали {before - len(articles)}, осталось {len(articles)}")
    _print_languages(articles)

    print("[5/5] Запись Parquet")
    frame = save_parquet(articles, output)
    print(f"    {output}  ({len(frame)} строк, {list(frame.columns)})")
    return output
