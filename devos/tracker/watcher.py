import os
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from devos.storage.db import execute_query
from devos.models.events import Event
import sqlite3

from devos.storage.db import execute_query
from devos.models.events import Event
from devos.utils.config import get_config
from devos.analytics.engine import AnalyticsEngine
from devos.utils.notifications import alert_if_stuck, alert_context_switch
import sqlite3

class DevosHandler(FileSystemEventHandler):
    """Watches your files so you don't have to (but you should, you're the dev)"""
    
    def __init__(self, idle_timeout=300):
        self.idle_timeout = idle_timeout
        self.last_activity = time.time()
        self.last_alert_check = time.time()
        self.is_idle = False
        self.config = get_config()
        self.analytics = AnalyticsEngine()

    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Check ignore patterns
        path_str = str(event.src_path)
        for pattern in self.config.get("ignore_patterns", []):
            if pattern in path_str:
                return
                
        self.record_activity(event.src_path, "file_edit")

    def get_git_root(self, path):
        """Finds where the git lives (it's usually in a .git folder)"""
        path = Path(path).resolve()
        for parent in [path] + list(path.parents):
            if (parent / ".git").is_dir():
                try:
                    result = subprocess.run(
                        ["git", "-C", str(parent), "branch", "--show-current"],
                        capture_output=True, text=True, check=True
                    )
                    branch = result.stdout.strip()
                    if branch:
                        return f"{parent} ({branch})"
                    return str(parent)
                except Exception:
                    return str(parent)
        return "Not a Project"

    def record_activity(self, file_path, event_type):
        now = time.time()
        
        # Idle detection logic
        if self.is_idle:
            self.log_event("idle_end", "None", "None")
            self.is_idle = False
        
        self.last_activity = now
        project = self.get_git_root(file_path)
        self.log_event(event_type, str(file_path), project)

    def log_event(self, event_type, file_path, project):
        """Writing history, one line at a time"""
        query = "INSERT INTO events (event_type, file, project) VALUES (?, ?, ?)"
        execute_query(query, (event_type, file_path, project))

    def check_idle(self):
        """Checks if you've gone to grab a coffee... or a nap"""
        if not self.is_idle and (time.time() - self.last_activity > self.idle_timeout):
            self.is_idle = True
            self.log_event("idle_start", "None", "None")

    def check_alerts(self):
        """Keeping you sharp with periodic nudges"""
        now = time.time()
        # Check every 30 minutes to avoid annoying the user
        if now - self.last_alert_check > 1800:
            self.last_alert_check = now
            
            # Context switch check
            switches = self.analytics.get_context_switches()
            alert_context_switch(switches)
            
            # Stuck detection
            top_file_data = self.analytics.get_top_files(limit=1)
            if top_file_data:
                file_path, count = top_file_data[0]
                alert_if_stuck(os.path.basename(file_path), count)

def start_watching(path_to_watch, idle_timeout=300):
    handler = DevosHandler(idle_timeout=idle_timeout)
    observer = Observer()
    observer.schedule(handler, path_to_watch, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
            handler.check_idle()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
