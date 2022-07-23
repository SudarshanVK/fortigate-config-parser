from modules.mics.main import (
    read_file,
    write_json,
    write_json_as_yaml,
    write_dict_to_excel,
    raise_exception_exit
)
from rich.console import Console
from rich.prompt import Prompt

console = Console()


from ttp import ttp


def parse_configuration(configuration: str, template_file: str) -> dict:
    template = read_file(f"./templates/{template_file}.ttp")
    try:
        parser = ttp(data=configuration, template=template)
        parser.parse()
        parsed_configuration = parser.result()[0][0]
        write_json(f"./outputs/json/{template_file}.json", parsed_configuration)
        write_json_as_yaml(f"./outputs/yaml/{template_file}.yaml", parsed_configuration)
        write_dict_to_excel(f"./outputs/excel/{template_file}.xlsx", parsed_configuration)
    except Exception as e:
        raise_exception_exit(e)


def main():

    ttp_template_file_list = [
        "interfaces",
    ]

    configuration = read_file("./data/configuration.cfg")

    for template in ttp_template_file_list:
        console.print(f"[yellow]Parsing {template}...", end="\r")
        parse_configuration(configuration, template)
        console.print(f"[green]Parsing {template}... [OK]")


if __name__ == "__main__":
    main()
