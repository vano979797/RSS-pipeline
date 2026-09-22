"""Одна новость = одна карточка.

Весь пайплайн гоняет один и тот же объект Article.
Поэтому RSS и News API взаимозаменяемы: на выходе fetch всегда list[Article].
"""

from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Article:
    title: str
    url: str
    text: str
    source: str
    published: Optional[str] = None
    language: Optional[str] = None

    def to_row(self) -> dict:
        """Словарь для pandas / Parquet."""
        return asdict(self)
