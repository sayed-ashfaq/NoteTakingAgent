from datetime import datetime, timedelta
import calendar

def get_current_context():
    """Returns detailed date context for LLM"""
    now = datetime.now()
    return f"""Current Date Context:
- Today: {now.strftime('%Y-%m-%d')} ({now.strftime('%A')})
- Current Time: {now.strftime('%H:%M')}
- Week Number: {now.strftime('%W')}
- Year: {now.strftime('%Y')}"""

def get_date_from_relative(text_date: str) -> str:
    """
    Simple helper to interpret relative dates if needed.
    For now, we will rely on the LLM to do the heavy lifting of natural language date parsing,
    as LLMs are very good at this when given the current date context.
    This function returns today's date as a fallback.
    """
    return datetime.now().strftime("%Y-%m-%d")
