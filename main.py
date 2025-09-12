import typer
import connect_helper
import list_helper
import edit_helper
from typing_extensions import Annotated
app = typer.Typer()


@app.command()
def list(no_test: Annotated[bool, typer.Option("--no-test", "-nt")] = False):
    '''
    Lists current SSH aliases
    '''
    if no_test:
        list_helper.show_table()
    else:
        list_helper.show_table(test_connectivity=True)


@app.command()
def add(hostname, name: Annotated[str, typer.Option("-n", "--name")] = "", identity: Annotated[str, typer.Option("-i", "--identity")] = ""):
    '''
    Adds a new SSH alias
    '''
    edit_helper.add(name, hostname, identity)


@app.command()
def copy(name: str, new_name: str):
    '''
    Copies an SSH alias
    '''
    edit_helper.copy_host(name, new_name)


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
def edit(host: Annotated[str, typer.Argument()] = "", ip: Annotated[str, typer.Option("-i", "--ip")] = ""):
    '''
    Edits a new SSH alias
    '''
    if host == "":
        edit_helper.select(ip=ip)
    else:
        edit_helper.edit(host, ip=ip)


@app.command()
def remove(host: Annotated[str, typer.Argument()] = ""):
    '''
    Removes an SSH alias
    '''
    if host == "":
        edit_helper.remove_select()
    else:
        edit_helper.remove(host)


@app.command()
def export(
    format: Annotated[str, typer.Option("-f", "--format", help="Export format: json, yaml, raw")] = "json",
    output: Annotated[str, typer.Option("-o", "--output", help="Output filename")] = "",
    summary: Annotated[bool, typer.Option("-s", "--summary", help="Include configuration summary")] = False
):
    '''
    Export SSH configuration to various formats
    '''
    try:
        import export_helper
        output_file = None if output == "" else output
        exported_file = export_helper.export_config(format, output_file, summary)
        print(f"✅ SSH config exported successfully to: {exported_file}")
    except ImportError as e:
        print(f"❌ Export failed: {e}")
    except Exception as e:
        print(f"❌ Export failed: {e}")


if __name__ == '__main__':
    app()
