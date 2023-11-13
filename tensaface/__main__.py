import typer

app_title = """\
TODO: Add ASCII art
"""

app = typer.Typer()


@app.command()
def serve():
    typer.echo("Serving...")


@app.command()
def run():
    typer.echo("Running...")


@app.command()
def cli():
    typer.echo("Serving...")


@app.callback()
def main():
    typer.echo("Tensaface")


if __name__ == "__main__":
    app()
