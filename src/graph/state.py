from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    user_input: str
    plan: str
    tool_result: str
    response: str
