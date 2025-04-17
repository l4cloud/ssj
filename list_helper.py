import os.path
import parser
import json
from rich import print
from rich.table import Table
from rich.console import Console

console = Console()


def show_hosts():
    config = get_config()
    for host in config:
        for line in host.config:
            print(json.dumps(line.content, indent=4, default=str))


def show_table():
    table = Table("Name", "Hostname")
    config = get_config()
    for host in config:
        for line in host.config:
            if ("Hostname" in line.content):
                table.add_row(line.host, line.content["Hostname"])
    console.print(table)


def get_config():
    path = os.path.expanduser("~/.ssh/config")
    if os.path.isfile(path):
        return parser.parse_file(open(path, "r"))
    else:
        raise Exception("SSH config is not present")
