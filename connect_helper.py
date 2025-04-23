import list_helper
from typer import prompt
import subprocess


def connect():
    hosts = list_helper.show_numbered_grid()
    ans = prompt("What host # do you want to connect to")
    if ans in hosts.keys():
        subprocess.run(["ssh", hosts[ans]])


def fzf_connect():
    subprocess.run(["sh", "./fssh.sh"])
