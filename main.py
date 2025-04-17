import typer
import list_helper
from typing_extensions import Annotated
app = typer.Typer()


@app.command()
def list(table: Annotated[bool, typer.Option("-t")] = False):
    if table:
        list_helper.show_table()
    else:
        list_helper.show_hosts()


@app.command()
def add(name: str, hostname, identity: str = ""):
    print(f"Add: {name} with hostname: {hostname} to ssh file")
    print(identity)


@app.command()
def remove(name: str = ""):
    print("Remove command")


if __name__ == '__main__':
    app()
