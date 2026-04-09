import sqlite3
from datetime import datetime, date, timedelta
from devos.storage.db import execute_query

class AnalyticsEngine:
    """Crunching numbers while you crunch code... :)"""
    
    def get_today_total_time(self):
        """Estimate total coding time for today based on event spans"""
        # A simple estimation: group events within 10 minutes of each other as active blocks
        query = """
            SELECT timestamp FROM events 
            WHERE DATE(timestamp) = DATE('now')
            ORDER BY timestamp ASC
        """
        rows = execute_query(query)
        if not rows:
            return 0
            
        timestamps = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in rows]
        total_seconds = 0
        if not timestamps:
            return 0
            
        # Grouping logic: if next event is within 10 mins, add the diff
        for i in range(len(timestamps) - 1):
            diff = (timestamps[i+1] - timestamps[i]).total_seconds()
            if diff < 600: # 10 minutes gap
                total_seconds += diff
                
        return total_seconds / 3600 # hours

    def get_top_projects(self, limit=5):
        """Who's winning the most of your time?"""
        query = """
            SELECT project, COUNT(*) as activity_count 
            FROM events 
            WHERE project != 'Not a Project' AND project != 'None'
            GROUP BY project 
            ORDER BY activity_count DESC 
            LIMIT ?
        """
        return execute_query(query, (limit,))

    def get_top_files(self, limit=5):
        """The files where the bugs (and the logic) live"""
        query = """
            SELECT file, COUNT(*) as activity_count 
            FROM events 
            WHERE file != 'None'
            GROUP BY file 
            ORDER BY activity_count DESC 
            LIMIT ?
        """
        return execute_query(query, (limit,))

    def get_context_switches(self):
        """How many times did you jump between projects today?"""
        query = """
            SELECT project FROM events 
            WHERE DATE(timestamp) = DATE('now')
            ORDER BY timestamp ASC
        """
        rows = execute_query(query)
        switches = 0
        current_project = None
        for row in rows:
            p = row[0]
            if p != current_project:
                if current_project is not None:
                    switches += 1
                current_project = p
        return switches

    def get_idle_vs_active(self):
        """Idle hands are... well, probably just grabbing coffee. :)"""
        query = """
            SELECT event_type, timestamp FROM events 
            WHERE DATE(timestamp) = DATE('now')
            ORDER BY timestamp ASC
        """
        # Simplified: count idle_start to idle_end duration
        # For now, let's just return idle event counts as a placeholder
        rows = execute_query(query)
        idle_starts = len([r for r in rows if r[0] == 'idle_start'])
        return idle_starts
