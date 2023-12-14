import typer
import langchain
from langchain.base_language import BaseLanguageModel
from langchain.llms.openai import OpenAI
from langchain.agents.agent import Agent
from lmi.app import App

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

cli_app = typer.Typer(name="LMI", help=description)


def load_app(path: str) -> App:
    if ':' in path:
        path, app_object_name = path.split(':')
    else:
        app_object_name = None
    module = __import__(path)
    if not app_object_name:
        return next(
            module.__dict__[name]
            for name in module.__dict__
            if isinstance(module.__dict__[name], App)
        )
    else:
        if not app_object_name in module.__dict__:
            raise ValueError(f"Object {app_object_name} not found in module {path}")
        app = module.__dict__[app_object_name]
        if not isinstance(app, App):
            raise ValueError(f"Object {app_object_name} in module {path} is not an App")
        return app


def load_llm(llm: str, llm_config = {}) -> BaseLanguageModel:
    match llm.lower().strip():
        case "openai":
            llm = OpenAI(model_name="gpt-4-1106", **llm_config)
        case r"openai:([a-zA-Z0-9\-_]+)":
            llm = OpenAI(model_name=llm.split(':')[1], **llm_config)
        case _:
            raise ValueError(f"LLM {llm} not found")
    return llm


@cli_app.command()
def serve(
    app: str = typer.Argument(help="Path to the app to serve, optionally with a \":app_object_name\" suffix to specify the app object to serve"),
    port: int = typer.Option(..., help="The port to serve on"),
):
    typer.echo(description)
    
    app: App = load_app(app)
    app.serve(port=port)
    
    typer.echo("Serving...")


@cli_app.command()
def cli():
    typer.echo(description)
    
    app: App = load_app(app)
    app.cli()
    
    typer.echo("Serving...")


@cli_app.command()
def run(
    app: str = typer.Argument(..., help="Path to the app to run, optionally with a \":app_object_name\" suffix to specify the app object to run"),
    agent: str = typer.Option(..., help="Serialized langchain agent to run the app against"),
    llm: str = typer.Argument(..., help="LLM to run the app against"),
):
    typer.echo(description)
    
    app: App = load_app(app)
    llm = load_llm(llm)
    agent = Agent.from_llm_and_tools(
        llm=llm,
        tools=app.llm_tools,
    )
    
    app.run(agent=agent)
    
    typer.echo("Running...")


@cli_app.callback()
def main():
    typer.echo(description)
    typer.Exit(0)


if __name__ == "__main__":
    cli_app()
