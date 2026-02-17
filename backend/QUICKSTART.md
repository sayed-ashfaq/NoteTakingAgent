# 🤖 Smart Note Taking Agent - MVP

An AI-powered personal assistant that classifies, formats, and stores your notes in Notion using LangGraph.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or using uv (faster):
```bash
uv pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required keys:
- `NOTION_API_KEY` - Your Notion integration token
- `NOTION_PAGE_ID` - Your Notion database ID
- `GOOGLE_API_KEY` - Your Google AI (Gemini) API key

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

## 🏗️ Architecture

### LangGraph Workflow (2 LLM Nodes)

```
User Input
    ↓
┌─────────────────────────┐
│  Node 1: Content        │
│  Formatter              │
│  - Classify (Task/Idea) │
│  - Generate title       │
│  - Format as markdown   │
│  - Extract tags         │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Node 2: Property       │
│  Creator                │
│  - Generate status      │
│  - Create Notion props  │
│  - Add metadata         │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Notion API             │
│  - Save to database     │
│  - Handle deduplication │
└─────────────────────────┘
```

## 📁 Project Structure

```
VA_NoteTaking/
├── agent.py              # LangGraph workflow with 2 LLM nodes
├── streamlit_app.py      # UI interface
├── notion_client.py      # Notion API wrapper
├── utils/
│   └── data_parsing.py   # Markdown to Notion blocks
├── logger/
│   ├── custom_logging.py # Structured logging
│   └── __init__.py
├── logs/                 # Application logs
├── .env                  # Environment variables (git-ignored)
└── requirements.txt      # Dependencies
```

## 🎯 Features

✅ **Fast AI Classification** - Uses Gemini Flash for speed  
✅ **Smart Property Generation** - LLM generates Notion properties dynamically  
✅ **Structured Logging** - Track what's happening under the hood  
✅ **Markdown Formatting** - Clean, readable content  
✅ **Deduplication** - Daily notes are appended, not duplicated  

## 📝 Usage Examples

### Task
```
Input: "Remind me to submit the quarterly report by Friday at 5 PM"

Output:
- Category: Task
- Title: "Submit quarterly report"
- Status: "To Do"
- Tags: ["deadline", "report"]
```

### Idea
```
Input: "App concept: Uber for Dog Walkers with real-time GPS tracking"

Output:
- Category: Idea
- Title: "Uber for Dog Walkers App"
- Status: "Draft"
- Tags: ["app", "concept", "gps"]
```

### Note
```
Input: "Meeting notes: API is slow (500ms avg). Need Redis caching."

Output:
- Category: Note
- Title: "Daily Note - 2026-02-16"
- Status: "Active"
- Tags: ["meeting", "performance"]
```

## 🔧 Configuration

### Notion Database Schema

Your Notion database should have these properties:

| Property | Type         | Options                          |
|----------|--------------|----------------------------------|
| Name     | Title        | -                                |
| Type     | Select       | Note, Idea, Task                 |
| Status   | Select       | To Do, In Progress, Done, etc.   |
| Date     | Date         | -                                |
| Tags     | Multi-select | Auto-generated                   |

## 🐛 Debugging

Enable debug mode in the Streamlit sidebar to see:
- API key status
- Detailed logs
- LLM responses

Check logs in `logs/` directory for structured JSON logs.

## 🚧 Future Enhancements

- [ ] Voice input (Whisper API)
- [ ] Multi-user support
- [ ] Custom templates
- [ ] Browser extension
- [ ] Mobile app

## 📄 License

MIT License - Feel free to use and modify!
