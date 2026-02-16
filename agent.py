"""
LangGraph Agent for Note Classification and Formatting
Uses 2 LLM nodes:
1. ContentFormatter - Classifies and formats the note content
2. PropertyCreator - Generates Notion properties dynamically
"""

import os
from typing import TypedDict, Literal
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
import json
from logger.custom_logging import CustomLogger
from utils.date_tools import get_current_context

load_dotenv()
logger = CustomLogger().get_logger(__name__)


# ==========================================
# STATE DEFINITION
# ==========================================
class NoteState(TypedDict):
    """State passed between nodes"""
    input_text: str
    category: str  # "Note", "Idea", "Task"
    title: str
    formatted_content: str  # Markdown formatted
    properties: dict  # Notion properties
    status: str
    target_date: str  # YYYY-MM-DD for task grouping
    tags: list[str]
    error: str | None


# ==========================================
# LLM INITIALIZATION
# ==========================================
def get_llm():
    """Initialize fast LLM - tries Google Gemini first, falls back to OpenAI"""
    
    # Fall back to OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=openai_key
        )
    
    raise ValueError("Neither GOOGLE_API_KEY nor OPENAI_API_KEY found in environment")


# ==========================================
# NODE 1: CONTENT FORMATTER
# ==========================================
def content_formatter_node(state: NoteState) -> NoteState:
    """
    Classifies the input and formats content as markdown.
    Also determines the target date for tasks.
    """
    logger.info("Node 1: ContentFormatter started")
    
    llm = get_llm()
    
    # Get current date context
    date_context = get_current_context()
    
    system_prompt = f"""You are a smart assistant for classifying notes and extracting dates.
{date_context}

Your Tasks:
1. Classify input as: "Note", "Idea", or "Task"
2. Extract/Generate a short Title.
3. **EXTRACT TARGET DATE (Crucial):**
   - Format: YYYY-MM-DD
   - **"Next Friday" logic:**
     - If today is Monday-Wednesday, "this Friday" = coming Friday.
     - "Next Friday" usually means the Friday of the *following* week.
     - BE CAREFUL: Calculate the exact date based on "Today" in context.
   - Example directly from context:
     - If Today is 2026-02-16 (Monday):
       - "This Friday" -> 2026-02-20
       - "Next Friday" -> 2026-02-27
   - Default: If no date specified, use Today's date.
4. **FORMAT CONTENT (Crucial):**
   - **IF TASK:** 
     - Format as a CHECKLIST: Start with `- [ ]`.
     - **REMOVE time words:** Strip "tomorrow", "next Friday", "today" from the content. The date is already in the target_date field.
     - Make it action-oriented (starts with Verb).
     - Example Input: "Tomorrow I need to update HR manager"
     - Example Output: "- [ ] Update HR manager that friend is going to be interviewed"
   - **IF NOTE/IDEA:** Standard Markdown.
5. Extract tags.

Output JSON only:
{{
    "category": "Note|Idea|Task",
    "title": "Title",
    "target_date": "YYYY-MM-DD",
    "formatted_content": "Markdown...",
    "tags": ["tag1"]
}}"""

    user_prompt = f"Input: {state['input_text']}"
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        # Parse JSON response
        # Extract JSON from markdown code blocks if present
        content = response.content.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
            
        result = json.loads(content)
        
        # Update state
        state["category"] = result["category"]
        state["title"] = result["title"]
        state["formatted_content"] = result["formatted_content"]
        state["target_date"] = result.get("target_date", datetime.now().strftime("%Y-%m-%d"))
        state["tags"] = result.get("tags", [])
        state["error"] = None
        
        logger.info(f"Node 1 complete: {result['category']} - {result['title']} ({state['target_date']})")
        
    except Exception as e:
        logger.error(f"Node 1 failed: {e}")
        state["error"] = f"ContentFormatter error: {str(e)}"
    
    return state


# ==========================================
# NODE 2: PROPERTY CREATOR
# ==========================================
def property_creator_node(state: NoteState) -> NoteState:
    """
    Generates Notion-compatible properties based on category
    Returns: properties dict ready for Notion API
    """
    logger.info("Node 2: PropertyCreator started")
    
    llm = get_llm()
    
    category = state.get("category", "Note")
    title = state.get("title", "Untitled")
    target_date = state.get("target_date")  # Use extracted date
    tags = state.get("tags", [])
    
    system_prompt = """You are a Notion properties generator.

Based on the category, generate appropriate properties.

Status rules:
- "Task" → "To Do", "In Progress", or "Done"
- "Idea" → "Draft", "Under Review", or "Approved"  
- "Note" → "Active" or "Archived"

Return ONLY valid JSON matching this structure:
{
    "status": "appropriate status based on category and content",
    "additional_tags": ["tag1", "tag2"]
}

Keep it minimal and fast."""

    user_prompt = f"""Category: {category}
Title: {title}
Target Date: {target_date}
Existing tags: {tags}
Content preview: {state.get('formatted_content', '')[:200]}

Generate status and any additional relevant tags."""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        # Parse JSON
        content = response.content.strip()
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
            
        result = json.loads(content)
        
        # Merge tags and add Category as a tag
        all_tags = list(set(tags + result.get("additional_tags", []) + [category]))
        
        # Build Notion properties
        properties = {
            "Name": {
                "title": [{"text": {"content": title}}]
            },
            # "Type" property removed as it doesn't exist in user's database
            "Date": {
                "date": {"start": target_date}  # Use target_date
            },
            "Status": {
                "select": {"name": result.get("status", "Active")}
            },
            "Tags": {
                "multi_select": [{"name": tag} for tag in all_tags[:5]]  # Max 5 tags
            }
        }
        
        state["properties"] = properties
        state["status"] = result.get("status", "Active")
        state["tags"] = all_tags
        state["error"] = None
        
        logger.info(f"Node 2 complete: Status={result.get('status')}, Tags={all_tags}")
        
    except Exception as e:
        logger.error(f"Node 2 failed: {e}")
        state["error"] = f"PropertyCreator error: {str(e)}"
        
        # Fallback properties
        all_fallback_tags = list(set(tags + [category]))
        state["properties"] = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Date": {"date": {"start": target_date}},
            "Status": {"select": {"name": "Active"}},
            "Tags": {"multi_select": [{"name": tag} for tag in all_fallback_tags[:3]]}
        }
    
    return state


# ==========================================
# GRAPH BUILDER
# ==========================================
def create_agent_graph():
    """Build the LangGraph workflow"""
    
    workflow = StateGraph(NoteState)
    
    # Add nodes
    workflow.add_node("content_formatter", content_formatter_node)
    workflow.add_node("property_creator", property_creator_node)
    
    # Define edges
    workflow.set_entry_point("content_formatter")
    workflow.add_edge("content_formatter", "property_creator")
    workflow.add_edge("property_creator", END)
    
    return workflow.compile()


# ==========================================
# MAIN INTERFACE
# ==========================================
class NoteAgent:
    """Main agent interface for Streamlit"""
    
    def __init__(self):
        logger.info("Initializing NoteAgent with LangGraph")
        self.graph = create_agent_graph()
    
    def process(self, input_text: str) -> NoteState:
        """
        Process input text through the LangGraph workflow
        
        Args:
            input_text: Raw user input
            
        Returns:
            Final state with category, title, formatted_content, and properties
        """
        logger.info(f"Processing input: {input_text[:100]}...")
        
        initial_state: NoteState = {
            "input_text": input_text,
            "category": "",
            "title": "",
            "formatted_content": "",
            "properties": {},
            "status": "",
            "tags": [],
            "error": None
        }
        
        try:
            final_state = self.graph.invoke(initial_state)
            
            if final_state.get("error"):
                logger.error(f"Processing failed: {final_state['error']}")
            else:
                logger.info(f"Processing complete: {final_state['category']} - {final_state['title']}")
            
            return final_state
            
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            raise


# ==========================================
# TESTING
# ==========================================
if __name__ == "__main__":
    agent = NoteAgent()
    
    test_input = """
    Meeting with design team:
    - Need to redesign the login page
    - John suggested adding social auth
    - Deadline: Next Friday
    """
    
    result = agent.process(test_input)
    
    print("\n" + "="*50)
    print("RESULT:")
    print("="*50)
    print(f"Category: {result['category']}")
    print(f"Title: {result['title']}")
    print(f"Status: {result['status']}")
    print(f"Tags: {result['tags']}")
    print("\nFormatted Content:")
    print(result['formatted_content'])
    print("\nNotion Properties:")
    print(json.dumps(result['properties'], indent=2))
