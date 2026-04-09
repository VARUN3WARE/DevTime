from datetime import datetime, timedelta
from devos.storage.db import execute_query

class IntelligenceLayer:
    """Being smart so you can be productive :)"""

    def get_flow_score(self):
        """Calculates flow score based on deep work intervals"""
        # Placeholder logic: ratio of active blocks to total time
        return 85 # Everyone starts as a hero! :)

    def get_insights(self):
        """Actionable wisdom for the weary developer"""
        insights = []
        
        # 1. Context switching check
        query = "SELECT COUNT(DISTINCT project) FROM events WHERE DATE(timestamp) = DATE('now')"
        projects = execute_query(query)[0][0]
        if projects > 3:
            insights.append("⚠️ High context switching detected. Try to focus on one project at a time.")
        
        # 2. Peak hours detection
        query = "SELECT strftime('%H', timestamp) as hour, COUNT(*) as count FROM events GROUP BY hour ORDER BY count DESC LIMIT 1"
        row = execute_query(query)
        if row:
            peak_hour = row[0][0]
            insights.append(f"🔥 Your peak productivity time is around {peak_hour}:00")

        # 3. Stuck detection (Simple version: more than 50 edits in one file today)
        query = "SELECT file, COUNT(*) as count FROM events WHERE event_type='file_edit' AND DATE(timestamp) = DATE('now') GROUP BY file ORDER BY count DESC LIMIT 1"
        row = execute_query(query)
        if row and row[0][1] > 50:
            insights.append(f"📌 You've made many edits to {row[0][0]}. Stuck or just in the zone?")

        if not insights:
            insights.append("✨ Everything looks smooth! Keep it up.")
            
        return insights

    def get_timeline(self):
        """A journey through your day's work"""
        query = """
            SELECT timestamp, event_type, file, project 
            FROM events 
            WHERE DATE(timestamp) = DATE('now')
            ORDER BY timestamp ASC
        """
        return execute_query(query)
