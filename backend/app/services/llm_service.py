
import os
import json
from typing import TypedDict, Any
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from app.core.config import settings
from app.utils.date_tools import get_current_context
from app.schemas.note import ProcessedNote

class NoteState(TypedDict):
    input_text: str
    category: str
    title: str
    formatted_content: str
    properties: dict
    status: str
    target_date: str
    tags: list[str]
    error: str | None

class LLMService:
    def __init__(self):
        self.llm = self._get_llm()
        self.graph = self._create_graph()

    def _get_llm(self):
        # 1. Try Google Gemini
        if settings.GOOGLE_API_KEY:
            try:
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0.1,
                    google_api_key=settings.GOOGLE_API_KEY
                )
            except Exception:
                pass
        
        # 2. Try OpenAI
        if settings.OPENAI_API_KEY:
             return ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.1,
                api_key=settings.OPENAI_API_KEY
            )

        # 3. Try Local/Custom Endpoint (Ollama/Compatible)
        if settings.OLLAMA_BASE_URL: # e.g. http://localhost:11434/v1
             return ChatOpenAI(
                base_url=settings.OLLAMA_BASE_URL,
                api_key="ollama", # placeholder
                model="llama3", # default or config
                temperature=0.1
            )
            
        raise ValueError("No LLM provider configured (Gemini/OpenAI/Ollama)")

    def _content_formatter_node(self, state: NoteState) -> NoteState:
        date_context = get_current_context()
        system_prompt = f"""You are a smart assistant for classifying notes and extracting dates.
{date_context}

Your Tasks:
1. Classify input as: "Note", "Idea", or "Task"
2. Extract/Generate a short Title.
3. **EXTRACT TARGET DATE (Crucial):**
   - Format: YYYY-MM-DD
   - Default: Today's date.
4. **FORMAT CONTENT (Crucial):**
   - **IF TASK:** Format as CHECKLIST `- [ ]`. Remove time words like "tomorrow". Start with Verb.
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
        
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Input: {state['input_text']}")
            ])
            
            content = response.content.strip()
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            
            state.update({
                "category": result["category"],
                "title": result["title"],
                "formatted_content": result["formatted_content"],
                "target_date": result.get("target_date", datetime.now().strftime("%Y-%m-%d")),
                "tags": result.get("tags", []),
                "error": None
            })
        except Exception as e:
            state["error"] = f"Formatter error: {str(e)}"
        
        return state

    def _property_creator_node(self, state: NoteState) -> NoteState:
        if state.get("error"): return state
        
        system_prompt = """Generate Notion-compatible status and tags.
Return JSON only: {"status": "Active|To Do|Draft", "additional_tags": []}"""
        
        user_prompt = f"""Category: {state['category']}
Title: {state['title']}
Target Date: {state['target_date']}
Tags: {state['tags']}"""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            content = response.content.strip()
            if "```" in content:
                content = content.split("```")[1].replace("json", "").strip()
            
            result = json.loads(content)
            
            all_tags = list(set(state["tags"] + result.get("additional_tags", []) + [state["category"]]))
            
            state["properties"] = {
                "Name": {"title": [{"text": {"content": state["title"]}}]},
                "Date": {"date": {"start": state["target_date"]}},
                "Status": {"select": {"name": result.get("status", "Active")}},
                "Tags": {"multi_select": [{"name": tag} for tag in all_tags[:5]]}
            }
            state["status"] = result.get("status", "Active")
            state["tags"] = all_tags
            
        except Exception as e:
             # Fallback
            state["properties"] = {
                "Name": {"title": [{"text": {"content": state["title"]}}]},
                "Date": {"date": {"start": state["target_date"]}},
                "Status": {"select": {"name": "Active"}},
                "Tags": {"multi_select": [{"name": t} for t in state["tags"]]}
            }
            state["status"] = "Active"

        return state

    def _create_graph(self):
        workflow = StateGraph(NoteState)
        workflow.add_node("formatter", self._content_formatter_node)
        workflow.add_node("enricher", self._property_creator_node)
        workflow.set_entry_point("formatter")
        workflow.add_edge("formatter", "enricher")
        workflow.add_edge("enricher", END)
        return workflow.compile()

    def process_text(self, text: str) -> ProcessedNote:
        initial_state = {
            "input_text": text,
            "category": "",
            "title": "",
            "formatted_content": "",
            "properties": {},
            "status": "",
            "tags": [],
            "error": None,
             "target_date": ""
        }
        
        result = self.graph.invoke(initial_state)
        
        if result.get("error"):
            raise Exception(result["error"])
            
        return ProcessedNote(
            category=result["category"],
            title=result["title"],
            formatted_content=result["formatted_content"],
            properties=result["properties"],
            status=result["status"],
            target_date=result["target_date"],
            tags=result["tags"]
        )
