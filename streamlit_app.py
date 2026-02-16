"""
Streamlit MVP for Smart Note Taking Agent
Uses LangGraph for AI-powered classification and Notion integration
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv
from agent import NoteAgent
from notion_client import NotionClient
from utils.data_parsing import markdown_to_notion_blocks
from streamlit_mic_recorder import mic_recorder
from utils.voice_module import transcribe

# Load environment variables
load_dotenv()

sys.path.append(os.getcwd())

# Page config
st.set_page_config(
    page_title="Smart Note Taker",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    /* Global Cleanliness */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Modern Text Area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        font-size: 1.1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.2s;
        min-height: 120px;
    }
    .stTextArea textarea:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Action Bar Styling */
    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: transform 0.1s;
    }
    .stButton button:hover {
        transform: translateY(-1px);
    }
    
    /* Header Styling */
    .hero-header {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #4f46e5 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    /* Result Card */
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #f3f4f6;
        margin-top: 1rem;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .badge-task { background-color: #fffbeb; color: #b45309; border: 1px solid #fcd34d; }
    .badge-idea { background-color: #f5f3ff; color: #7c3aed; border: 1px solid #ddd6fe; }
    .badge-note { background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown('<div class="hero-header">Smart Writer AI</div>', unsafe_allow_html=True)
st.caption("Auto-organize your thoughts into Notion with voice or text.")

# ---------------------------------------------------------
# INITIALIZE AGENT (Silent)
# ---------------------------------------------------------
if 'agent' not in st.session_state:
    try:
        st.session_state.agent = NoteAgent()
        st.session_state.notion_client = NotionClient()
    except Exception as e:
        st.error(f"⚠️ Initialization Error: {e}")
        st.stop()

# Initialize input state
if 'main_input' not in st.session_state:
    st.session_state.main_input = ""

# ---------------------------------------------------------
# UNIFIED INPUT GRID
# ---------------------------------------------------------

# 1. Create a container for the text input (to be filled later)
# This allows us to process audio and update state BEFORE rendering the text area
input_container = st.container()

# 2. Control Bar (Grid) - Rendered below via code order, but logic runs first
col_mic, col_process, col_clear = st.columns([1, 2, 0.5])

with col_mic:
    # Mic returns audio immediately
    audio = mic_recorder(
        start_prompt="🎤 Record",
        stop_prompt="⏹️ Stop",
        key='recorder'
    )

with col_process:
    # Primary Action
    process_btn = st.button("✨ Save to Notion", type="primary", use_container_width=True)

with col_clear:
    # Secondary Action
    if st.button("🗑️", help="Clear Input", use_container_width=True):
        st.session_state.main_input = ""
        st.rerun()

# ---------------------------------------------------------
# LOGIC: HANDLE VOICE
# ---------------------------------------------------------
if audio:
    with st.spinner("🎧 Transcribing..."):
        try:
            text = transcribe(audio['bytes'])
            if text:
                st.session_state.main_input = text
                # We don't need st.rerun() here because we haven't rendered the text_area yet!
                # The container below will pick up the new state immediately.
        except Exception as e:
            st.error(f"❌ Audio Error: {e}")

# 3. Render Text Input inside the container (NOW safe to use state)
with input_container:
    input_text = st.text_area(
        "What's on your mind?",
        key="main_input",
        height=140,
        placeholder="Type here or use the microphone below...",
        label_visibility="collapsed"
    )
if process_btn:
    if not input_text:
        st.warning("Please enter some text first!")
    else:
        # Minimal Progress UI
        progress_bar = st.progress(0)
        status = st.empty()
        
        try:
            # Step 1: Analyze
            status.markdown("🧠 **AI is thinking...**")
            progress_bar.progress(30)
            
            result = st.session_state.agent.process(input_text)
            
            if result.get("error"):
                st.error(f"❌ Error: {result['error']}")
                st.stop()
            
            progress_bar.progress(60)
            
            # Step 2: Save to Notion
            status.markdown("💾 **Syncing to Notion...**")
            progress_bar.progress(80)
            
            # Convert & Save
            children = markdown_to_notion_blocks(content=result['formatted_content'])
            category = result['category']
            target_date = result.get('target_date')
            
            # Notion Save Logic
            saved_msg = ""
            if category == "Note":
                page_title = f"Daily Note - {target_date}"
                existing_page = st.session_state.notion_client.find_page_by_title(page_title)
                if existing_page:
                    st.session_state.notion_client.append_blocks(existing_page["id"], children)
                    saved_msg = f"Appended to **{page_title}**"
                else:
                    st.session_state.notion_client.add_note(result['properties'], children)
                    saved_msg = f"Created **{page_title}**"
                    
            elif category == "Task":
                page_title = f"Tasks - {target_date}"
                existing_page = st.session_state.notion_client.find_page_by_title(page_title)
                if existing_page:
                    st.session_state.notion_client.append_blocks(existing_page["id"], children)
                    saved_msg = f"Appended to **{page_title}**"
                else:
                    props = result['properties'].copy()
                    props["Name"] = {"title": [{"text": {"content": page_title}}]}
                    st.session_state.notion_client.add_note(props, children)
                    saved_msg = f"Created task list **{page_title}**"
            
            else: # Idea
                st.session_state.notion_client.add_note(result['properties'], children)
                saved_msg = f"Created **{result['title']}**"
            
            progress_bar.progress(100)
            status.empty()
            progress_bar.empty()
            
            # ---------------------------------------------------------
            # RESULT CARD
            # ---------------------------------------------------------
            st.balloons()
            
            badge_class = f"badge-{result['category'].lower()}"
            
            st.markdown(f"""
            <div class="result-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div class="status-badge {badge_class}">{result['category']}</div>
                    <div style="color: #6b7280; font-size: 0.9rem;">{target_date}</div>
                </div>
                <h3 style="margin: 0 0 0.5rem 0; color: #111827;">{result['title']}</h3>
                <div style="font-size: 0.95rem; color: #374151; line-height: 1.5;">
                    ✅ {saved_msg}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Show Details"):
                st.markdown(result['formatted_content'])

        except Exception as e:
            st.error(f"Something went wrong: {e}")
