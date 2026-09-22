"""ШАГ 2. Очистка HTML.

RSS часто приносит не текст, а разметку:
    <p>Новость <a href="...">тут</a>&nbsp;&nbsp;</p>

Моделям и поиску теги не нужны. Нам нужен обычный человеческий текст.
"""

from __future__ import annotations

import html
import re

from bs4 import BeautifulSoup

WHITESPACE = re.compile(r"\s+")


def clean_html(raw: str) -> str:
    """HTML → одна строка без тегов и лишних пробелов."""
    if not raw:
        return ""

    # &nbsp; &amp; и компания → обычные символы
    unescaped = html.unescape(raw)

    # Нет угловых скобок — это уже текст, BeautifulSoup не нужен.
    if "<" in unescaped:
        soup = BeautifulSoup(unescaped, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        # separator=" " чтобы соседние теги не слиплись в «словослово»
        unescaped = soup.get_text(separator=" ")

    return WHITESPACE.sub(" ", unescaped).strip()
