
import shutil
import os

items_to_move = [
    "app", "config", "data", "logger", "logs", "notebooks", "utils",
    ".env", ".env.example", ".python-version", "pyproject.toml", "requirements.txt", "uv.lock",
    "README.md", "QUICKSTART.md", "BUILD_SUMMARY.md",
    "agent.py", "notion_client.py", "notion_run.py", "streamlit_app.py", "test_agent.py", "create_structure.py"
]

os.makedirs("backend", exist_ok=True)
os.makedirs("frontend", exist_ok=True)

for item in items_to_move:
    if os.path.exists(item):
        try:
            shutil.move(item, os.path.join("backend", item))
            print(f"Moved {item}")
        except Exception as e:
            print(f"Failed to move {item}: {e}")
            
print("Migration complete.")
