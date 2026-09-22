"""Точка входа: python run.py

Сначала открой pipeline.py — там вся логика по шагам.
Этот файл только запускает пайплайн из командной строки.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from config import MIN_TEXT_LEN, OUTPUT_FILE
from pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        description="News ETL: RSS → clean HTML → language → dedup → Parquet",
    )
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE)
    parser.add_argument("--min-len", type=int, default=MIN_TEXT_LEN)
    args = parser.parse_args()
    run_pipeline(output=args.output, min_text_len=args.min_len)


if __name__ == "__main__":
    main()
