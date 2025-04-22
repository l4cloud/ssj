from config import Host, ConfigLine
import shutil
import os
import json
import list_helper
from typer import prompt
from config import get_config


def select():
    list_helper.show_hosts()
    answer = prompt("Choose a host to edit")
    edit(answer)


def edit(input):
    config = get_config()
    valid = False
    for host in config:
        if (host.name == input):
            valid = True
            new = edit_host(host, input)
            config.remove(host)
            config.append(new)
    if (valid is False):
        print(f"Host of name {input} not found")
    else:
        update_config(config)


def edit_host(host, hostname):
    print(f"editing host {host.name}")
    new_host = Host(host.name)

    print("Leave blank if you want to keep the value the same [value]")
    for line in host.config:
        value = prompt(f"{line.key}", default=f"{line.value}")
        new_host.add_config(ConfigLine(host.name, line.key, value))

    return new_host


def update_config(config):
    path = os.path.expanduser("~/.ssh/config")
    shutil.move(path, f"{path}.bak")
    with open(path, 'a') as new_config:
        for host in config:
            new_config.write(f"Host {host.name}\n")
            for line in host.config:
                new_config.write(f"  {line.key} {line.value}\n")
