# Smart Note taking AI agent

An agent that can activate on my voice command, Take notes of whatever i say and segregate them and store them in the designated places.

Here's the brief: 
For storing data: Notion
AI Agent: Langchain

- I have to create and append data accordingly
- Primary focus to build for mobile

Tech Stack:
- Langchain
- Notion
- VAD
- Langgraph


## First step
- Connecting notion with the python so that it can read, write and update the data.

Below is a simple, focused **README.md** you can keep in your project folder.
It’s designed to stop you from drifting into “agent chaos” and keep you on the correct journey.

---


# Notion Notes MVP (Python)

A minimal foundation project:

**AI Agent → Notion API → Store Notes**

This is NOT a full AI agent yet.  
This is Step 0: reliable note storage.

---

## Goal

Build a simple pipeline:

- Capture a note
- Classify using AI agent (Idea / Task / Note)
- Create properties
- Format content 
- Save it into one Notion database
    - Append if page is existing like ideas, and tasks
    - Create new page and add - For notes

Once this works, we can later add:

- Voice input (Whisper)
- Auto-classification (LLM)
- FastAPI backend (multi-user)

---
