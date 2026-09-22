from steps.language import detect_language


def test_english():
    text = (
        "Scientists have discovered a new method to store renewable energy "
        "using simple materials available in most countries around the world."
    )
    assert detect_language(text) == "en"


def test_russian():
    text = (
        "Учёные открыли новый способ хранить энергию из возобновляемых "
        "источников с помощью простых материалов, доступных во многих странах."
    )
    assert detect_language(text) == "ru"


def test_too_short():
    assert detect_language("hi") is None
