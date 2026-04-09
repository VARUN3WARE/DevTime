import os
import signal
import sys
import daemon
from pathlib import Path
from devos.tracker.watcher import start_watching
from devos.storage.db import init_db

PID_FILE = Path.home() / ".devos" / "devos.pid"

def get_pid():
    if PID_FILE.exists():
        with open(PID_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return None
    return None

def is_running():
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    return False

def start_daemon():
    """Giving birth to a background process (it's a quiet child)"""
    if is_running():
        print("DevOS is already running. Monitoring your every keystroke... :)")
        return

    init_db()
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # We use a simple daemonization for now
    # In a real tool, we'd use python-daemon or similar
    # But for this CLI, a simple nohup-like approach is often preferred for visibility
    
    print("Starting DevOS daemon...")
    pid = os.fork()
    if pid > 0:
        # Parent process
        with open(PID_FILE, "w") as f:
            f.write(str(pid))
        print(f"DevOS started in background (PID: {pid})")
        sys.exit(0)
    else:
        # Child process
        # Detach from terminal
        os.setsid()
        os.umask(0)
        
        # Track the user's projects (defaulting to home directory for discovery)
        # In practice, usually dev folders are better, but we'll watch a broad path
        # or have a config. For now, let's watch the current project parent
        watch_path = str(Path.home() / "Desktop") # Watching Desktop as a default dev area for this user
        
        # Redirect stdout/stderr to a log file
        log_file = Path.home() / ".devos" / "devos.log"
        with open(log_file, "a") as f:
            sys.stdout = f
            sys.stderr = f
            start_watching(watch_path)

def stop_daemon():
    """Putting the daemon to sleep. Rest well, hero."""
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            PID_FILE.unlink()
            print("DevOS stopped. Go enjoy the real world! :)")
        except OSError:
            print("Failed to stop DevOS. Maybe it's immortal?")
    else:
        print("DevOS is not running. Feel free to slack off.")
