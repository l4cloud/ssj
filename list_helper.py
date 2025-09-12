import os.path
from concurrent.futures import ThreadPoolExecutor
import connection_tester
import parser
import json
from config import get_config
from rich import print
from rich.table import Table
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

console = Console()

def show_table(test_connectivity: bool = False):
    config = get_config()
    
    if not test_connectivity:
        table = Table("Name", "Hostname", "User",
                      "IdentityFile", title="Hosts :rocket:")
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
            
            table.add_row(f"[green]{host.name}", hostname, user, identity)
        console.print(table)
        return [host.name for host in config]

    table = Table("Name", "Hostname", "User",
                  "IdentityFile", "Status", title="Hosts :rocket:")
    hosts = list(config)
    
    host_data = []
    for host in hosts:
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
        
        host_data.append({
            "name": host.name,
            "hostname": hostname,
            "user": user,
            "identity": identity,
            "status": Spinner("dots", "Pinging...")
        })

    for data in host_data:
        table.add_row(f"[green]{data['name']}", data['hostname'], data['user'], data['identity'], data['status'])

    with Live(table, console=console, screen=False, refresh_per_second=10) as live:
        with ThreadPoolExecutor() as executor:
            host_names = []
            for host in hosts:
                hostname = host.name
                for line in host.config:
                    if line.key.lower() == "hostname":
                        hostname = line.value
                        break
                host_names.append(hostname)
            results = executor.map(connection_tester.test_connection, host_names)

            for i, is_online in enumerate(results):
                status = "[green]Online[/green]" if is_online else "[red]Offline[/red]"
                host_data[i]['status'] = status
                
                table = Table("Name", "Hostname", "User",
                              "IdentityFile", "Status", title="Hosts :rocket:")
                
                for data in host_data:
                    if isinstance(data['status'], Spinner):
                         table.add_row(f"[green]{data['name']}", data['hostname'], data['user'], data['identity'], data['status'])
                    else:
                        table.add_row(f"[green]{data['name']}", data['hostname'], data['user'], data['identity'], data['status'])
                live.update(table)
    return [host.name for host in config]