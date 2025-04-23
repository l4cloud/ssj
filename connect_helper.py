import list_helper
from typer import prompt
import subprocess

fzf_ssh = """#!/bin/bash
selected=$(awk '/^Host / { print $2 }' ~/.ssh/config | fzf)
clear
ssh $(echo "$selected" | tr -d '\r')
"""


def connect():
    hosts = list_helper.show_numbered_grid()
    ans = prompt("What host # do you want to connect to")
    if ans in hosts.keys():
        subprocess.run(["ssh", hosts[ans]])


def fzf_connect():
    subprocess.run(["bash", "-c", fzf_ssh])
