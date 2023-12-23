from ascii import from_ascii_codes, to_ascii_codes
from hypothesis import example, given, settings
from hypothesis.strategies import text


@given(text())
@example("")
@settings(max_examples=100)
def test_decode_inverts_encode(test_str: str) -> None:
    assert from_ascii_codes(to_ascii_codes(test_str)) == test_str


@given(text())
def test_input_length_equals_encode_length(test_str: str) -> None:
    encoded = to_ascii_codes(test_str)
    assert len(encoded) == len(test_str)
