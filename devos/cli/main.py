import os
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from devos.daemon.manager import start_daemon, stop_daemon, is_running
from devos.storage.db import execute_query
from devos.analytics.engine import AnalyticsEngine

app = typer.Typer(help="DevOS: Your productivity butler :)")
console = Console()
analytics = AnalyticsEngine()

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
    total_time = analytics.get_today_total_time()
    switches = analytics.get_context_switches()
    
    console.print(Panel(f"[bold blue]Today's Coding Stats[/bold blue]\n\n"
                        f"⏱️  Total Time: {total_time:.2f}h\n"
                        f"🔄  Context Switches: {switches}\n"
                        f"☕  Idle Breaks: {analytics.get_idle_vs_active()}", 
                        title="📊 DevOS Summary"))
    
    table = Table(title="Top Projects")
    table.add_column("Project", style="cyan")
    table.add_column("Activity Count", style="magenta")
    
    for p, count in analytics.get_top_projects():
        table.add_row(os.path.basename(p), str(count))
        
    console.print(table)

@app.command()
def week():
    """Show this week's productivity trends"""
    console.print(Panel("[bold green]Weekly Trends[/bold green]\n\n"
                        "Coming soon: ASCII charts and daily breakdowns! :)", 
                        title="📈 DevOS History"))

@app.command()
def project(name: str):
    """Show stats for a specific project"""
    console.print(f"Stats for project: [bold cyan]{name}[/bold cyan]")
    # Placeholder for more detailed filtering

@app.command()
def file():
    """Show top files worked on"""
    table = Table(title="Top Files")
    table.add_column("File", style="green")
    table.add_column("Activity Count", style="yellow")
    
    for f, count in analytics.get_top_files():
        table.add_row(os.path.basename(f), str(count))
        
    console.print(table)

if __name__ == "__main__":
    app()
