import typer
import connect_helper
import list_helper
import edit_helper
from typing_extensions import Annotated
app = typer.Typer()


@app.command()
def list(ls: Annotated[bool, typer.Option("--list", "-ls")] = False,
         json: Annotated[bool, typer.Option("--json", "-j")] = False):
    '''
    Lists current SSH aliases
    '''
    if ls:
        list_helper.show_host()
    elif json:
        list_helper.show_json()
    else:
        list_helper.show_table()


@app.command()
def add(hostname, name: Annotated[str, typer.Option("-n", "--name")] = "", identity: Annotated[str, typer.Option("-i", "--identity")] = ""):
    '''
    Adds a new SSH alias
    '''
    edit_helper.add(name, hostname, identity)


@app.command()
def copy(name: str, hostname, identity: Annotated[str, typer.Option("-i", "--identity")] = ""):
    '''
    Adds a new SSH alias
    '''
    edit_helper.add(name, hostname, identity)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, fzf: Annotated[bool, typer.Option("--fzf", "-f")] = False):
    if ctx.invoked_subcommand is None:
        if fzf:
            print("Run fssh script")
            connect_helper.fzf_connect()
        else:
            connect_helper.connect()


@app.command()
def connect(fzf: Annotated[bool, typer.Option("--fzf", "-f")] = False, host: Annotated[str, typer.Argument()] = ""):
    '''
    Connects to a host
    '''
    if fzf:
        print("Run fssh script")
        connect_helper.fzf_connect()
    else:
        if host == "":
            connect_helper.connect()
        else:
            connect_helper.direct_connect(host)


@app.command()
def edit(host: Annotated[str, typer.Argument()] = ""):
    '''
    Edits a new SSH alias
    '''
    if host == "":
        edit_helper.select()
    else:
        edit_helper.edit(host)


@app.command()
def remove(host: Annotated[str, typer.Argument()] = ""):
    '''
    Removes an SSH alias
    '''
    if host == "":
        edit_helper.remove_select()
    else:
        edit_helper.remove(host)


if __name__ == '__main__':
    app()
