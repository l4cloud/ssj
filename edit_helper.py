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
                value = prompt(f"Enter the value of option {key}",
                               default="Remove")
                if (value == "Remove"):
                    new_host.remove_config(key)
                else:
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


def add(name, hostname, identity):
    config = get_config()
    valid = True
    for host in config:
        if (host.name == name):
            valid = False
    if valid is True:
        conf = []
        conf.append(ConfigLine(name, "HostName", hostname))
        if identity != "":
            conf.append(ConfigLine(name, "IdentityFile", identity))
        newHost = Host(name)
        newHost.config = conf
        config.append(newHost)
        add_parameters(newHost)
        update_config(config)
    else:
        print(f"Host exists with name: {name}")


def add_parameters(host):
    new = True
    while (new):
        add_new = confirm(
            "Do you want to add any additional paramers?")
        if not add_new:
            new = False
        else:
            key = prompt("Enter an option you want to add")
            if (key.lower() in known_params):
                value = prompt(f"Enter the value of option {key}",
                               default="Remove")
                if (value == "Remove"):
                    host.remove_config(key)
                else:
                    c = ConfigLine(host.name, key, value)
                    host.add_config(c)


def update_config(config):
    path = os.path.expanduser("~/.ssh/config")
    shutil.move(path, f"{path}.bak")
    with open(path, 'a') as new_config:
        for host in config:
            new_config.write(f"Host {host.name}\n")
            for line in host.config:
                new_config.write(f"  {line.key} {line.value}\n")
