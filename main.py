import typer
import list_helper
from typing_extensions import Annotated
app = typer.Typer()


@app.command()
def list(table: Annotated[bool, typer.Option("--table", "-t")] = False,
         json: Annotated[bool, typer.Option("--json", "-j")] = False):
    '''
    Lists current SSH aliases
    '''
    if table:
        list_helper.show_table()
    elif json:
        list_helper.show_json()
    else:
        list_helper.show_hosts()


@app.command()
def add(name: str, hostname, identity: str = ""):
    '''
    Adds a new SSH alias
    '''
    print(f"Add: {name} with hostname: {hostname} to ssh file")
    print(identity)


@app.command()
def remove(name: str = ""):
    '''
    Removes an SSH alias
    '''
    print("Remove command")


if __name__ == '__main__':
    app()
