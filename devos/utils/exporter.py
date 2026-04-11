import json
from devos.storage.db import execute_query

def export_all_data(output_path):
    """Packing your bags... where are we going? :)"""
    
    data = {}
    
    # Export events
    events = execute_query("SELECT * FROM events")
    data["events"] = [
        {"id": r[0], "timestamp": r[1], "file": r[2], "project": r[3], "type": r[4]} 
        for r in events
    ]
    
    # Export sessions
    sessions = execute_query("SELECT * FROM sessions")
    data["sessions"] = [
        {"id": r[0], "start": r[1], "end": r[2], "project": r[3]} 
        for r in sessions
    ]
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
        
    return len(events)
