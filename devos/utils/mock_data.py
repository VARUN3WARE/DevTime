import random
from datetime import datetime, timedelta
from devos.storage.db import execute_query

def generate_mock_data():
    """Giving your database a fake social life... :)"""
    
    projects = ["DevOS", "StockBot", "GameEngine", "Portfolio"]
    files = ["main.py", "utils.py", "db.py", "test_core.py", "ui.py"]
    event_types = ["file_edit", "file_open"]
    
    now = datetime.now()
    
    print("Generating 100 mock events for today...")
    
    for i in range(100):
        # Activity spread over 8 hours
        offset = random.randint(0, 8 * 3600)
        ts = (now - timedelta(seconds=offset)).strftime("%Y-%m-%d %H:%M:%S")
        
        project = random.choice(projects)
        file = f"/home/user/projects/{project}/{random.choice(files)}"
        event_type = random.choice(event_types)
        
        execute_query(
            "INSERT INTO events (timestamp, event_type, file, project) VALUES (?, ?, ?, ?)",
            (ts, event_type, file, project)
        )
        
    # Add some idle blocks
    for i in range(10):
        offset = random.randint(0, 8 * 3600)
        ts = (now - timedelta(seconds=offset)).strftime("%Y-%m-%d %H:%M:%S")
        execute_query(
            "INSERT INTO events (timestamp, event_type, file, project) VALUES (?, ?, ?, ?)",
            (ts, "idle_start", "None", "None")
        )
        
    print("Done! You look busy now. :)")
