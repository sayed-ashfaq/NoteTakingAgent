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
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .badge-task { background-color: #fef3c7; color: #92400e; }
    .badge-idea { background-color: #ddd6fe; color: #5b21b6; }
    .badge-note { background-color: #dbeafe; color: #1e40af; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🤖 Smart Note Taker</div>', unsafe_allow_html=True)
st.markdown("**AI-powered note classification** • Notion integration • LangGraph workflow")

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Debug info
    if st.checkbox("Show Debug Info"):
        st.write(f"✅ Notion Key: {'✓' if os.getenv('NOTION_API_KEY') else '✗'}")
        st.write(f"✅ Notion DB: {'✓' if os.getenv('NOTION_PAGE_ID') else '✗'}")
        st.write(f"✅ Google API: {'✓' if os.getenv('GOOGLE_API_KEY') else '✗'}")
    
    st.divider()
    
    # VOICE INPUT SECTION
    st.markdown("### 🎙️ Voice Input")
    
    # 1. Mic Recorder
    st.write("Click to record:")
    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹️ Stop Recording",
        key='recorder'
    )
    
    # 2. File Upload
    uploaded_audio = st.file_uploader("Or upload audio", type=['wav', 'mp3', 'm4a'])
    
    # Process Audio
    if audio or uploaded_audio:
        with st.spinner("🎧 Transcribing audio..."):
            try:
                if audio:
                    audio_bytes = audio['bytes']
                else:
                    audio_bytes = uploaded_audio.read()
                
                # Transcribe
                transcribed_text = transcribe(audio_bytes)
                if transcribed_text:
                    st.session_state.main_input = transcribed_text
                    st.success("✅ Transcription complete!")
                
            except Exception as e:
                st.error(f"Transcription failed: {str(e)}")

    st.divider()
    
    st.markdown("""
    ### 🔄 Workflow
    
    **Node 1: Content Formatter**
    - Classifies input (Note/Idea/Task)
    - Generates title
    - Formats as markdown
    - Extracts tags
    
    **Node 2: Property Creator**
    - Generates Notion properties
    - Determines status
    - Adds metadata
    
    **Node 3: Notion Updater**
    - Saves to Notion
    - Handles deduplication
    """)
    
    st.divider()
    
    st.markdown("""
    ### 📚 Examples
    
    **Task:**
    "Remind me to submit the report by Friday at 5 PM"
    
    **Idea:**
    "App concept: Real-time collaboration tool for remote teams"
    
    **Note:**
    "Meeting notes: API is slow, need caching"
    """)

# ==========================================
# INITIALIZE AGENT
# ==========================================
if 'agent' not in st.session_state:
    with st.spinner("🤖 Initializing AI Agent..."):
        try:
            st.session_state.agent = NoteAgent()
            st.session_state.notion_client = NotionClient()
            st.toast("✅ Agent ready!", icon="🤖")
        except Exception as e:
            st.error(f"❌ Failed to initialize: {e}")
            st.stop()

# ==========================================
# MAIN INPUT
# ==========================================
st.markdown("### 📝 Enter your thought, note, or task")

# Initialize session state for input
if 'main_input' not in st.session_state:
    st.session_state.main_input = ""

input_text = st.text_area(
    label="Input",
    key="main_input",
    height=150,
    placeholder="Type here or use voice recording from sidebar...",
    label_visibility="collapsed"
)

col1, col2 = st.columns([3, 1])
with col1:
    process_btn = st.button("🚀 Process & Save", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if clear_btn:
    st.session_state.main_input = ""
    st.rerun()

# ==========================================
# PROCESSING
# ==========================================
if process_btn and input_text:
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: AI Processing
        status_text.text("🤖 AI Agent analyzing...")
        progress_bar.progress(20)
        
        result = st.session_state.agent.process(input_text)
        
        if result.get("error"):
            st.error(f"❌ Processing error: {result['error']}")
            st.stop()
        
        progress_bar.progress(60)
        
        # Show AI Analysis
        status_text.text("✅ AI Analysis complete")
        
        with st.expander("🔍 AI Analysis Results", expanded=True):
            # Category badge
            badge_class = f"badge-{result['category'].lower()}"
            st.markdown(f"""
            <div>
                <span class="status-badge {badge_class}">{result['category']}</span>
                <span class="status-badge" style="background-color: #f3f4f6; color: #374151;">{result['status']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Title:** {result['title']}")
            st.markdown(f"**Target Date:** {result.get('target_date', 'N/A')}")
            st.markdown(f"**Tags:** {', '.join(result['tags'])}")
            
            st.markdown("**Formatted Content:**")
            st.markdown(result['formatted_content'])
        
        # Step 2: Save to Notion
        status_text.text("💾 Saving to Notion...")
        progress_bar.progress(80)
        
        # Convert markdown to Notion blocks
        children = markdown_to_notion_blocks(content=result['formatted_content'])
        
        # 3. Execution Logic
        category = result['category']
        target_date = result.get('target_date')
        
        # CASE 1: Daily Note (Append)
        if category == "Note":
            page_title = f"Daily Note - {target_date}"
            existing_page = st.session_state.notion_client.find_page_by_title(page_title)
            
            if existing_page:
                st.session_state.notion_client.append_blocks(existing_page["id"], children)
                st.success(f"✅ Appended to **{page_title}**")
            else:
                st.session_state.notion_client.add_note(result['properties'], children)
                st.success(f"✅ Created **{page_title}**")
                
        # CASE 2: Tasks (Group by Date)
        elif category == "Task":
            page_title = f"Tasks - {target_date}"
            existing_page = st.session_state.notion_client.find_page_by_title(page_title)
            
            if existing_page:
                # Append to existing daily task page
                st.session_state.notion_client.append_blocks(existing_page["id"], children)
                st.success(f"✅ Appended to **{page_title}**")
            else:
                # Create specific properties for the Container Page
                task_page_props = result['properties'].copy()
                task_page_props["Name"] = {"title": [{"text": {"content": page_title}}]}
                
                st.session_state.notion_client.add_note(task_page_props, children)
                st.success(f"✅ Created new task list: **{page_title}**")
        
        # CASE 3: Ideas (Individual Pages)
        else:
            st.session_state.notion_client.add_note(result['properties'], children)
            st.success(f"✅ Created **{result['title']}** as {result['category']}")
        
        progress_bar.progress(100)
        status_text.text("✅ Complete!")
        
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.exception(e)
    
    finally:
        progress_bar.empty()
        status_text.empty()

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.875rem;">
    Built with LangGraph • Notion API • Gemini Flash<br>
    Fast MVP for Smart Note Taking
</div>
""", unsafe_allow_html=True)
