from modules.mics.main import (
    read_file,
    write_json,
    write_json_as_yaml,
    write_dict_to_excel,
    raise_exception_continue,
)
from rich.console import Console
from rich.prompt import Prompt
import os
import shutil
import openpyxl
import click

console = Console()


from ttp import ttp


def parse_configuration(configuration: str, template: str) -> dict:
    try:
        parser = ttp(data=configuration, template=template)
        parser.parse()
        return parser.result()[0][0]
    except Exception as e:
        raise_exception_continue(e)


def pre_tasks():
    console.print("[yellow]Performing cleanup...", end="\r")
    if os.path.exists("./outputs"):
        shutil.rmtree("./outputs")
    console.print("[green]Performing cleanup... [OK]")

    console.print("[yellow]Creating output directory...", end="\r")
    os.mkdir("./outputs")
    wb = openpyxl.Workbook()
    wb.save("./outputs/configuration.xlsx")
    console.print("[green]Creating output directories... [OK]")

@click.command()
@click.option("--configuration", "-c", required=True)
def main(configuration):

    script_path = os.path.dirname(__file__)

    cont = Prompt.ask(
        "This will delete any previous output files. Continue?",
        choices=["y", "n"],
        default="n",
    )
    if cont == "y":
        console.print("[yellow]Running pre-tasks...", end="\r")
        pre_tasks()
        console.print("[green]Running pre-tasks... [OK]", end="\r")
    else:
        SystemExit("User aborted...")

    configuration = read_file(configuration)
    template_file = os.path.join(script_path, "templates", "template.ttp")
    template = read_file(template_file)

    console.print("[yellow]Parsing Configuration...", end="\r")
    parsed_config = parse_configuration(configuration, template)
    console.print("[green]Parsing Configuration... [OK]")

    console.print("[yellow]Generating Output files...", end="\r")
    write_json("./outputs/configuration.json", parsed_config)
    write_json_as_yaml("./outputs/configuration.yaml", parsed_config)
    for config_item, config_data in parsed_config.items():
        write_dict_to_excel(
            "./outputs/configuration.xlsx", config_data["data"], config_item
        )
    console.print("[green]Generating Output files...", end="\r")


if __name__ == "__main__":
    main()
