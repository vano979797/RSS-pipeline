"""ШАГ 3. Определение языка.

Зачем: в RAG и поиске смешивать ru и en обычно плохо.
Фильтр по language='ru' — одна колонка в Parquet, без повторного анализа.
"""

from __future__ import annotations

from langdetect import LangDetectException, detect

from config import LANG_SAMPLE_LEN


def detect_language(text: str) -> str | None:
    """Вернуть код языка ('en', 'ru', ...) или None, если текста мало."""
    sample = (text or "").strip()
    if len(sample) < 20:
        return None
    try:
        return detect(sample[:LANG_SAMPLE_LEN])
    except LangDetectException:
        return None
