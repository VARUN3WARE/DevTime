import subprocess
import os

def send_notification(title, message):
    """Whispering in your ear... digitally. :)"""
    try:
        # Check for notify-send (Linux)
        if subprocess.run(["which", "notify-send"], capture_output=True).returncode == 0:
            subprocess.run(["notify-send", title, message])
        else:
            # Fallback or silent
            pass
    except Exception:
        pass

def alert_if_stuck(file_name, edit_count):
    if edit_count > 50:
        send_notification("DevOS Alert", f"📌 You've made {edit_count} edits to {file_name}. Need a break?")

def alert_context_switch(project_count):
    if project_count > 3:
        send_notification("DevOS Alert", f"⚠️ High context switching! {project_count} projects active.")
