import json
import pytest
from unittest.mock import patch, mock_open
from utils import merge, read_json_file

def test_merge_empty_dict():
    assert merge({}, {}) == {}

def test_merge_non_overlapping_dict():
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    assert merge(dict1, dict2) == {"a": 1, "b": 2, "c": 3, "d": 4}

def test_merge_overlapping_dict():
    dict1 = {"a": 1, "b": 1}
    dict2 = {"a": 0, "c": 2}
    assert merge(dict1, dict2) == {"a": 0, "b": 1, "c": 2}

    
def test_read_json_file_of_valid_file():
    mock_data = {"a": 1, "b": 2}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        data = read_json_file("filepath", "test.json")
    assert data == mock_data

def test_read_json_file_of_invalid_file():
    with patch("builtins.open", mock_open(read_data="not a valid JSON string")):
        with pytest.raises(json.JSONDecodeError):
            data = read_json_file("filepath", "test.json")
