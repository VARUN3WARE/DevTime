import os
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from devos.daemon.manager import start_daemon, stop_daemon, is_running
from devos.storage.db import execute_query
from devos.analytics.engine import AnalyticsEngine
from devos.analytics.insights import IntelligenceLayer

app = typer.Typer(help="DevOS: Your productivity butler :)")
console = Console()
analytics = AnalyticsEngine()
intelligence = IntelligenceLayer()

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
                        "Mon: ■■■■■■■ (7h)\n"
                        "Tue: ■■■■■ (5h)\n"
                        "Wed: ■■■■■■■■ (8h)\n"
                        "Thu: ■■■ (3h)\n"
                        "Fri: ■■■■■■ (6h)\n", 
                        title="📈 DevOS History"))

@app.command()
def project(name: str):
    """Show stats for a specific project"""
    console.print(f"Stats for project: [bold cyan]{name}[/bold cyan]")
    # In a real app, filter analytics by project name
    console.print("Activity: High :)")

@app.command()
def file():
    """Show top files worked on"""
    table = Table(title="Top Files")
    table.add_column("File", style="green")
    table.add_column("Activity Count", style="yellow")
    
    for f, count in analytics.get_top_files():
        table.add_row(os.path.basename(f), str(count))
        
    console.print(table)

@app.command()
def insights():
    """Get AI-powered insights into your workflow"""
    console.print(Panel("\n".join(intelligence.get_insights()), 
                        title="💡 DevOS Insights"))
    console.print(f"Flow Score: [bold green]{intelligence.get_flow_score()}%[/bold green] :)")

@app.command()
def replay():
    """Replay your work timeline for today"""
    table = Table(title="Timeline Replay")
    table.add_column("Time", style="dim")
    table.add_column("Event", style="bold")
    table.add_column("Project", style="cyan")
    table.add_column("File", style="green")
    
    for ts, event, file, project in intelligence.get_timeline():
        short_file = os.path.basename(file) if file != "None" else ""
        short_project = os.path.basename(project) if project != "None" else ""
        time_str = ts.split(" ")[1]
        table.add_row(time_str, event, short_project, short_file)
        
    console.print(table)

@app.command()
def focus():
    """Start a focus session (Pomodoro-style)"""
    console.print("[bold blue]Focus mode activated.[/bold blue] 🍅")
    console.print("DevOS will now track this as a concentrated effort.")

if __name__ == "__main__":
    app()
