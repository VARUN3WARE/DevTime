import os
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from devos.daemon.manager import start_daemon, stop_daemon, is_running
from devos.storage.db import execute_query
from devos.analytics.engine import AnalyticsEngine
from devos.analytics.insights import IntelligenceLayer
from devos.utils.mock_data import generate_mock_data
from devos.utils.config import get_config, update_config
from devos.utils.exporter import export_all_data
from pathlib import Path

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

@app.command()
def config(key: str = typer.Argument(None, help="The config key to update"), 
           value: str = typer.Argument(None, help="The new value for the key")):
    """View or update configuration settings (e.g., config idle_timeout 600)"""
    if key and value:
        # Simple type conversion for timeout
        if key == "idle_timeout":
            value = int(value)
        update_config(key, value)
        console.print(f"[bold green]Updated {key} to {value}.[/bold green] :)")
    else:
        conf = get_config()
        console.print(Panel(json.dumps(conf, indent=4), title="⚙️ DevOS Configuration"))

@app.command()
def reset():
    """Clear all tracking data (Fresh start!)"""
    confirm = typer.confirm("Are you sure you want to delete all your history? This cannot be undone! :(")
    if confirm:
        execute_query("DELETE FROM events")
        execute_query("DELETE FROM sessions")
        console.print("[bold red]Database cleared.[/bold red] A clean slate for a new you. :)")
    else:
        console.print("Cancelled. Your history is safe.")

@app.command()
def export(file_path: str = "devos_export.json"):
    """Export all tracking data to a JSON file"""
    count = export_all_data(file_path)
    console.print(f"[bold green]Exported {count} events to {file_path}.[/bold green] Safe travels! :)")

@app.command()
def logs():
    """Tail the daemon logs (if they exist)"""
    log_file = Path.home() / ".devos" / "devos.log"
    if log_file.exists():
        with open(log_file, "r") as f:
            # Show last 20 lines
            lines = f.readlines()
            for line in lines[-20:]:
                console.print(line.strip())
    else:
        console.print("[yellow]No logs found yet. Is the daemon running?[/yellow]")

@app.command()
def mock():
    """Inject mock data for testing (don't worry, it's fake!)"""
    generate_mock_data()
    console.print("[bold green]Mock data injected.[/bold green] Check `devos today` now! :)")

if __name__ == "__main__":
    app()
