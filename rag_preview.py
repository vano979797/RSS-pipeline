"""Как этот Parquet потом идёт в RAG.

RAG = Retrieval Augmented Generation.
Модель не «помнит» новости. Мы кладём тексты в индекс, по вопросу
достаём куски, и уже их отдаём модели как контекст.

Этот файл не ходит в OpenAI и не поднимает векторную БД.
Он только показывает границу: датасет готов, дальше его режут на чанки.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import OUTPUT_FILE

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Режем текст окном с перекрытием, чтобы смысл не обрывался на границе."""
    if not text:
        return []
    if len(text) <= size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


def preview(path: Path = OUTPUT_FILE) -> None:
    if not path.exists():
        raise SystemExit(f"Сначала собери датасет: python run.py\nНет файла: {path}")

    df = pd.read_parquet(path)
    print(f"строк: {len(df)}")
    print(f"колонки: {list(df.columns)}")
    print(f"языки:\n{df['language'].value_counts(dropna=False).to_string()}\n")

    total_chunks = 0
    for _, row in df.iterrows():
        total_chunks += len(chunk_text(row["text"]))
    print(f"чанков по ~{CHUNK_SIZE} символов: {total_chunks}")
    print("дальше: эмбеддинги этих чанков → векторная БД → поиск по вопросу")


if __name__ == "__main__":
    preview()
