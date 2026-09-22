"""Настройки проекта.

Запомни правило: числа, пути и список источников живут здесь,
а не размазаны по коду. Тогда пайплайн читается как история,
а не как квест «где спрятана константа».
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "news.parquet"

# Смесь EN и RU, чтобы шаг «определение языка» был не декоративным.
# Если один фид ляжет — остальные всё равно дадут датасет.
RSS_FEEDS = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("BBC Tech", "https://feeds.bbci.co.uk/news/technology/rss.xml"),
    ("The Guardian", "https://www.theguardian.com/world/rss"),
    ("Hacker News", "https://hnrss.org/frontpage"),
    ("Lenta", "https://lenta.ru/rss/news"),
    ("Habr", "https://habr.com/ru/rss/news/?fl=ru"),
]

# Слишком короткие тексты бесполезны и для чтения, и для RAG.
MIN_TEXT_LEN = 40

# Сколько символов берём, чтобы определить язык. Весь текст не нужен.
LANG_SAMPLE_LEN = 1000
