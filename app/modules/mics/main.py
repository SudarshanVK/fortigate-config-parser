import pandas

import json
import yaml


from rich.console import Console

console = Console()


def raise_exception_exit(message: str) -> None:
    """
    Raises an exception and exits the program
    """
    console.print_exception(show_locals=True)
    raise SystemExit(message)


def raise_exception_continue(message: str) -> None:
    """
    Raises an exception and continues the program
    """
    console.print_exception(show_locals=True)


def read_file(file_path: str) -> str:
    """
    Reads a file and returns its contents
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        raise_exception_exit(e)


def write_json(filename: str, data: dict) -> None:
    """
    Writes the data to a json file
    """
    try:
        with open(filename, "w") as outfile:
            json.dump(data, outfile, indent=4)
    except Exception as e:
        raise_exception_exit(e)


def write_json_as_yaml(filename: str, data: dict) -> None:
    """
    Writes the data to a json file
    """
    try:
        with open(filename, "w") as outfile:
            yaml.dump(data, outfile)
    except Exception as e:
        raise_exception_exit(e)


def write_dict_to_excel(filename: str, data: dict) -> None:
    """
    Writes the data to an excel file
    """
    try:
        df = pandas.DataFrame(data)
        df.to_excel(filename, index=False)
    except Exception as e:
        raise_exception_exit(e)
