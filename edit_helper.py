from config import Host, ConfigLine, known_params
import shutil
import os
import json
import list_helper
from typer import prompt, confirm
from config import get_config


def select():
    list_helper.show_table()
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
    new_host = Host(host.name)
    for line in host.config:
        value = prompt(f"{line.key}", default=f"{line.value}")
        new_host.add_config(ConfigLine(host.name, line.key, value))
    new = True
    while (new):
        add_new = confirm(
            f"Do you want to add or remove an option from {host.name}?")
        if not add_new:
            new = False
        else:
            key = prompt("Enter an option you want to add")
            if (key.lower() in known_params):
                value = prompt(f"Enter the value of option {
                               key}", default="Remove")
                print(value)
                if (value == "Remove"):
                    print("Removing config line")
                    new_host.remove_config(key)
                else:
                    print("Adding config line")
                    c = ConfigLine(host.name, key, value)
                    new_host.add_config(c)

    return new_host


def remove_select():
    list_helper.show_hosts()
    answer = prompt("Choose a host to remove")
    remove(answer)


def remove(input):
    config = get_config()
    valid = False
    for host in config:
        if (host.name == input):
            valid = True
            config.remove(host)
    if (valid is False):
        print(f"Host of name {input} not found")
    else:
        update_config(config)


def update_config(config):
    path = os.path.expanduser("~/.ssh/config")
    shutil.move(path, f"{path}.bak")
    with open(path, 'a') as new_config:
        for host in config:
            new_config.write(f"Host {host.name}\n")
            for line in host.config:
                new_config.write(f"  {line.key} {line.value}\n")
