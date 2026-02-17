
from datetime import datetime

def get_current_context():
    """Returns detailed date context for LLM"""
    now = datetime.now()
    return f"""Current Date Context:
- Today: {now.strftime('%Y-%m-%d')} ({now.strftime('%A')})
- Current Time: {now.strftime('%H:%M')}
- Week Number: {now.strftime('%W')}
- Year: {now.strftime('%Y')}"""
