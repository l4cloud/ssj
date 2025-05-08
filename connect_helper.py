import list_helper
from typer import prompt
import subprocess

fzf_ssh = """#!/bin/bash
if type tmux >/dev/null 2>/dev/null; then
  selected=$(awk '/^Host / { print $2 }' ~/.ssh/config | fzf)
  clear
  if [ "$TERM_PROGRAM" = tmux ]; then
    tmux rename-window $selected
  else
    echo 'Not in tmux'
  fi
  ssh $(echo "$selected" | tr -d '\r')
else
    echo 'fzf not installed please install fzf to use the -f flag'
fi
"""


def connect():
    hosts = list_helper.show_numbered_grid()
    ans = prompt("What host # do you want to connect to")
    if ans in hosts.keys():
        subprocess.run(["ssh", hosts[ans]])


def direct_connect(host):
    subprocess.run(["ssh", host])


def fzf_connect():
    subprocess.run(["bash", "-c", fzf_ssh])
