from qobuz_dj.downloader import _safe_get


def test_safe_get_nested():
    d = {"a": {"b": {"c": 1}}}
    # Pass keys as separate arguments
    assert _safe_get(d, "a", "b", "c") == 1


def test_safe_get_missing():
    d = {"a": {}}
    assert _safe_get(d, "a", "b", default="default") == "default"


def test_safe_get_non_dict_intermediate():
    """Test fix for 'get on None' or 'get on str' error."""
    # Case 1: Intermediate is None
    d = {"a": None}
    assert _safe_get(d, "a", "b", default="default") == "default"

    # Case 2: Intermediate is string (has __getitem__ but not get)
    d = {"a": "string_value"}
    assert _safe_get(d, "a", "b", default="default") == "default"
