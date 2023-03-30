import json
import os
import click

def read_json_file(filepath, filename):
    """load multi-environment definition file"""
    with open(f"{filepath}/{filename}", encoding="utf-8") as f:
      return json.load(f)

def merge(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def write_json_file(file, contents):
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(contents, f, indent=2)

def validate_filepath(filepath, flag):
    """Validate filepath exists"""
    if not os.path.exists(filepath):
        raise click.UsageError(f"Invalid {flag} provided: {filepath}")
