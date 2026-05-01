# devos

DevOS is a lightweight, local-first developer productivity tool that automatically tracks your activity, understands your workflow patterns, and generates actionable insights. It stays completely on your machine, ensuring your data remains private and local.

## Core Features
* **Background Tracking**: Silently monitors file edits and project switches using Git root detection.
* **Idle Detection**: Automatically pauses tracking when you step away.
* **Flow Analysis**: Calculates "Flow Scores" based onw uninterrupted deep work.
* **Intelligent Insights**: Detects context switching, stuck patterns, and peak productivity hours.
* **Timeline Replay**: Visualize your day with a step-by-step history of your work.
* **Exportable Data**: Take your data anywhere with JSON export support.

## 📸 Previews in Action

### Daily Dashboard (`devos today`)
```text
╭────────────────────────────── 📊 DevOS Summary ──────────────────────────────╮
│ Today's Coding Stats                                                         │
│                                                                              │
│ ⏱️  Total Time: 5.42h                                                        │
│ 🔄  Context Switches: 86                                                     │
│ ☕  Idle Breaks: 10                                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
     Language Breakdown      
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Language ┃ Activity Count ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ py       │ 100            │
│ md       │ 2              │
└──────────┴────────────────┘
            Top Projects             
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Project          ┃ Activity Count ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ DevTime          │ 2894           │
│ DevOS            │ 88             │
└──────────────────┴────────────────┘
```

### Productivity Heatmap (`devos heatmap`)
```text
╭────────────────────────────── 🔥 DevOS Heatmap ──────────────────────────────╮
│ Activity Heatmap (Last 30 Days)                                              │
│                                                                              │
│ Apr 01: ■■■ (3h)                                                             │
│ Apr 02: ■■■■■ (5h)                                                           │
│ Apr 03: ■ (1h)                                                               │
│ Apr 04: ■■■■■■■ (7h)                                                         │
│ Apr 05: ■■■ (3h)                                                             │
│ Apr 06: ■■ (2h)                                                              │
│ Apr 07: ■■■■■■ (6h)                                                          │
│ ... [More data in database] ...                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### AI Workflow Insights (`devos insights`)
```text
╭───────────────────────────── 💡 DevOS Insights ──────────────────────────────╮
│ ⚠️ High context switching detected. Try to focus on one project at a time.   │
│ 🔥 Your peak productivity time is around 10:00                               │
╰──────────────────────────────────────────────────────────────────────────────╯
Flow Score: 85% :)
```

## Installation
```bash
# Clone the repository
cd DevTime

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and the tool
pip install -r requirements.txt
pip install -e .
```

## Usage Guide
* `devos start`: Start the background tracking daemon.
* `devos status`: Check if the tool is currently active.
* `devos today`: Overview of today's coding time and top projects.
* `devos week`: Productivity trends with ASCII charts.
* `devos insights`: AI-powered workflow observations.
* `devos replay`: Timeline of recent activity.
* `devos export [FILE]`: Save all data to JSON.
* `devos config [KEY] [VALUE]`: View or update settings.
    * Example: `devos config idle_timeout 600` (sets idle timeout to 10 minutes).
    * Example: `devos config watch_paths '["/home/user/code", "/home/user/projects"]'` (sets multiple watch paths).
* `devos reset`: Clear all database events and sessions (requires confirmation).
* `devos export [FILE]`: Save all data to JSON (default: `devos_export.json`).
* `devos logs`: View recent activity logs from the background daemon.
* `devos stop`: Safely stop the tracking daemon.

## Configuration Options
- `watch_paths`: List of directories to monitor for activity.
- `ignore_patterns`: List of strings (files/folders) to ignore during tracking.
- `idle_timeout`: Time in seconds before marking activity as "idle" (default: 300).

## Design Philosophy
DevOS is built on the principle of minimal overhead and maximum insight. It uses a modular architecture (Daemon, Tracker, Analytics, CLI) following SOLID principles to ensure high maintainability and performance.

Have fun coding and stay in the flow! :)
