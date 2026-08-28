from typing import Any
from pydantic import ValidationError
from my_exceptions import ConfigError
from .validator import Validator


def read_maze_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()


def parse_to_dict(file_content: str) -> dict[str, Any]:
    lines = file_content.splitlines()
    result: dict[str, Any] = {}
    seen_keys = set()

    # Parse each line and validate syntax
    for line in lines:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        if '=' not in line or line.count('=') != 1:
            raise ConfigError(f"Invalid line: {line}")
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ConfigError(f"Invalid line: {line}")

        # Check for duplicate keys
        if key in seen_keys:
            raise ConfigError(f"Duplicate key: {key}")
        seen_keys.add(key)

        result[key] = value

    # ALlowed keys
    valid_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                  "OUTPUT_FILE", "PERFECT", "SEED"]

    # Check for missing or invalid keys
    for key in valid_keys:
        if key not in result.keys() and key != "SEED":
            raise ConfigError(f"Missing key: {key}")
    for key in result.keys():
        if key not in valid_keys:
            raise ConfigError(f"Invalid key: {key}")

    # Parse values
    try:
        result["WIDTH"] = int(result["WIDTH"])
        result["HEIGHT"] = int(result["HEIGHT"])

        if ',' not in result["ENTRY"] or result["ENTRY"].count(',') != 1:
            raise ConfigError(f"Invalid value for ENTRY: {result['ENTRY']}")

        result["ENTRY"] = tuple(map(int, result["ENTRY"].split(',')))

        if ',' not in result["EXIT"] or result["EXIT"].count(',') != 1:
            raise ConfigError(f"Invalid value for EXIT: {result['EXIT']}")

        result["EXIT"] = tuple(map(int, result["EXIT"].split(',')))

        if result["PERFECT"] not in ["True", "False"]:
            raise ConfigError(f"Invalid value for PERFECT: "
                              f"{result['PERFECT']}")
        elif result["PERFECT"] == "True":
            result["PERFECT"] = True
        else:
            result["PERFECT"] = False

        if "SEED" in result:
            result["SEED"] = int(result["SEED"])
    except ValueError:
        raise ConfigError(f"Invalid value for one of the fields: {result}")

    # Validate using Pydantic model
    try:
        Validator(
            width=result["WIDTH"],
            height=result["HEIGHT"],
            entry=result["ENTRY"],
            exit=result["EXIT"]
        )
    except ValidationError as error:
        raise ConfigError(f"Validator error: {error}")
    return result
