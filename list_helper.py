import os.path
import parser
import json
from config import get_config
from rich import print
from rich.table import Table
from rich.console import Console

console = Console()


def show_hosts():
    config = get_config()
    for host in config:
        for line in host.config:
            if (line.key.lower() == "hostname"):
                print(f"{line.host}: {line.value}")


def show_numbered_grid():
    config = get_config()
    columns = 4
    index = 1
    host_strings = []
    output_hosts = {}
    grid = Table.grid(expand=False)
    for host in config:
        host_strings.append(f"[{index}] [green]{host.name} ")
        output_hosts[str(index)] = host.name
        index += 1

    for i in range(columns):
        grid.add_column()

    for i in range(0, len(host_strings), columns):
        row = host_strings[i:i + columns]
        if len(row) < columns:
            row.extend([""] * (columns - len(row)))
        grid.add_row(*row)

    print(grid)
    return (output_hosts)


def show_json():
    config = get_config()
    hosts = []
    for host in config:
        new = {"host": host.name}
        for line in host.config:
            new[line.key] = line.value
        hosts.append(new)
    print(json.dumps(hosts, indent=4, default=str))


def show_table():
    table = Table("Name", "Hostname", "User",
                  "IdentityFile", title="Hosts :rocket:")
    config = get_config()
    for host in config:
        hostname = ""
        user = ""
        identity = ""

        for line in host.config:
            match line.key.lower():
                case "hostname":
                    hostname = line.value
                case "user":
                    user = line.value
                case "identityfile":
                    identity = line.value

        table.add_row(f"[green]{line.host}", hostname, user, identity)

    console.print(table)
