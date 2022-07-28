from modules.mics.main import (
    read_file,
    write_json,
    write_json_as_yaml,
    write_dict_to_excel,
    raise_exception_continue,
)


from rich import print
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel

console = Console()


import os
import shutil
import openpyxl
import click
from pathlib import Path


from ttp import ttp


script_path = Path(__file__).parent


def parse_configuration(configuration: str, template: str) -> dict:
    try:
        parser = ttp(data=configuration, template=template)
        parser.parse()
        return parser.result()[0][0]
    except Exception as e:
        raise_exception_continue(e)


def pre_tasks(dir_path: str) -> None:
    console.print("[yellow]Performing cleanup...", end="\r")
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    console.print("[green]Performing cleanup... [OK]")

    console.print("[yellow]Creating output directory...", end="\r")
    os.mkdir(dir_path)
    wb = openpyxl.Workbook()
    wb.save(f"{dir_path}/configuration.xlsx")
    console.print("[green]Creating output directories... [OK]")


def generate_output_files(dir_path: str, configuration: dict) -> None:
    write_json(f"{dir_path}/configuration.json", configuration)
    write_json_as_yaml(f"{dir_path}/configuration.yaml", configuration)
    for config_item, config_data in configuration.items():
        if "data" in config_data:
            write_dict_to_excel(
                f"{dir_path}/configuration.xlsx", config_data["data"], config_item
            )
    wb = openpyxl.load_workbook(f"{dir_path}/configuration.xlsx")
    wb.remove(wb["Sheet"])
    wb.save(filename=f"{dir_path}/configuration.xlsx")


@click.command()
@click.option("--configuration", "-c", required=True)
def main(configuration):

    template_file = script_path / "templates" / "template.ttp"
    output_dir = script_path.parent / "output"

    if Confirm.ask(
        "[yellow]This will delete any previous output files. Continue?",
    ):
        console.print("[yellow]Running pre-tasks...", end="\r")
        pre_tasks(output_dir)
        console.print("[green]Running pre-tasks... [OK]", end="\r")
    else:
        SystemExit("User aborted...")

    configuration = read_file(configuration)
    template = read_file(template_file)

    console.print("[yellow]Parsing Configuration...", end="\r")
    parsed_config = parse_configuration(configuration, template)
    console.print("[green]Parsing Configuration... [OK]")

    console.print("[yellow]Generating Output files...", end="\r")
    generate_output_files(output_dir, parsed_config)
    console.print("[green]Generating Output files...", end="\r")

    print(Panel.fit(f"[green]{output_dir}", title="Output Directory"))


if __name__ == "__main__":
    main()
