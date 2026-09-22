from steps.clean import clean_html


def test_strips_tags_and_entities():
    raw = "<p>Hello&nbsp;<a href='#'>world</a>!!!</p>"
    assert clean_html(raw) == "Hello world !!!"


def test_empty_stays_empty():
    assert clean_html("") == ""
    assert clean_html(None) == ""  # type: ignore[arg-type]


def test_collapses_whitespace():
    raw = "<div>one</div>\n\n   <div>two</div>"
    assert clean_html(raw) == "one two"


def test_plain_text_does_not_need_parser():
    assert clean_html("Just a title") == "Just a title"
