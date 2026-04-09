import typer
from rich.console import Console
from rich.table import Table
from devos.daemon.manager import start_daemon, stop_daemon, is_running
from devos.storage.db import execute_query

app = typer.Typer(help="DevOS: Your productivity butler :)")
console = Console()

@app.command()
def start():
    """Start the DevOS tracking daemon"""
    start_daemon()

@app.command()
def stop():
    """Stop the DevOS tracking daemon"""
    stop_daemon()

@app.command()
def status():
    """Check if DevOS is currently watching you"""
    if is_running():
        console.print("[bold green]DevOS is active and tracking.[/bold green] :)")
    else:
        console.print("[bold red]DevOS is sleeping.[/bold red] :(")

@app.command()
def today():
    """Show today's productivity highlights"""
    # Placeholder for Phase 2
    console.print("[yellow]Analytics coming in Phase 2! Keep coding.[/yellow]")

if __name__ == "__main__":
    app()
