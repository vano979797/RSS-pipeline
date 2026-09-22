"""ШАГ 5. Parquet.

Parquet — колоночный файл. Его любят pandas, Spark, DuckDB и RAG-пайплайны:
сжимается, быстро читает нужные колонки, не разъезжается как CSV с запятыми в тексте.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from models import Article


def save_parquet(articles: list[Article], path: Path) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame([article.to_row() for article in articles])
    frame.to_parquet(path, index=False)
    return frame
