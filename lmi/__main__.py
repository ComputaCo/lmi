import typer

description = """\
                                               
     ▄            ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄     
    ▐░▌          ▐░░▌     ▐░░▌▐░░░░░░░░░░░▌    
    ▐░▌          ▐░▌░▌   ▐░▐░▌ ▀▀▀▀█░█▀▀▀▀     
    ▐░▌          ▐░▌▐░▌ ▐░▌▐░▌     ▐░▌         
    ▐░▌          ▐░▌ ▐░▐░▌ ▐░▌     ▐░▌         
    ▐░▌          ▐░▌  ▐░▌  ▐░▌     ▐░▌         
    ▐░▌          ▐░▌   ▀   ▐░▌     ▐░▌         
    ▐░▌          ▐░▌       ▐░▌     ▐░▌         
    ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌ ▄▄▄▄█░█▄▄▄▄     
    ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌    
     ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀     
                                               
     —————————————————————————————————————     
          LANGUAGE  MODEL  INTERFACE           
                                               
      Copyright (c) 2023 by ComputaCo Inc.
      Released under the MIT License (MIT)
                                               
     —————————————————————————————————————     
"""

app = typer.Typer(name="LMI", help=description)


@app.command()
def serve():
    typer.echo(description)
    typer.echo("Serving...")


@app.command()
def run():
    typer.echo(description)
    typer.echo("Running...")


@app.command()
def cli():
    typer.echo(description)
    typer.echo("Serving...")


@app.callback()
def main():
    typer.echo(description)
    typer.Exit(0)


if __name__ == "__main__":
    app()
