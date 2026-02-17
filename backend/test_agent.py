"""
Quick test script for the agent without Streamlit
Tests the LangGraph workflow independently
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Check environment variables
print("="*60)
print("Environment Check")
print("="*60)

required_vars = {
    "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
    "NOTION_API_KEY": os.getenv("NOTION_API_KEY"),
    "NOTION_PAGE_ID": os.getenv("NOTION_PAGE_ID")
}

all_present = True
for var_name, var_value in required_vars.items():
    status = "[OK]" if var_value else "[MISSING]"
    print(f"{status} {var_name}: {'Set' if var_value else 'MISSING'}")
    if not var_value:
        all_present = False

if not all_present:
    print("\n[ERROR] Please configure missing environment variables in .env file")
    print("See .env.example for reference")
    sys.exit(1)

print("\n" + "="*60)
print("Testing Agent Workflow")
print("="*60)

try:
    from agent import NoteAgent
    
    agent = NoteAgent()
    print("[OK] Agent initialized successfully\n")
    
    # Test cases
    test_cases = [
        {
            "name": "Task Example",
            "input": "Remind me to submit the quarterly report by Friday at 5 PM. Need to include Q4 metrics and team feedback."
        },
        {
            "name": "Idea Example",
            "input": "App concept: 'Uber for Dog Walkers'. Features: Real-time GPS tracking, walker ratings, automatic scheduling, and poop bag tracking."
        },
        {
            "name": "Note Example",
            "input": """Meeting Quick Notes:
            - API response time is too slow (avg 500ms)
            - Need to add Redis caching layer
            - John suggested looking into database indexing
            - Next meeting: Friday 2 PM"""
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test['name']}")
        print(f"{'='*60}")
        print(f"Input: {test['input'][:80]}...")
        
        try:
            result = agent.process(test['input'])
            
            if result.get("error"):
                print(f"[ERROR] Error: {result['error']}")
                continue
            
            print(f"\n[SUCCESS] Processing successful!")
            print(f"   Category: {result['category']}")
            print(f"   Title: {result['title']}")
            print(f"   Target Date: {result.get('target_date', 'N/A')}")
            print(f"   Status: {result['status']}")
            print(f"   Tags: {', '.join(result['tags'])}")
            print(f"\n   Formatted Content Preview:")
            print(f"   {result['formatted_content'][:200]}...")
            
        except Exception as e:
            print(f"[ERROR] Test failed: {e}")
    
    print("\n" + "="*60)
    print("[SUCCESS] All tests completed! Agent is working.")
    print("="*60)
    print("\nReady to run: streamlit run streamlit_app.py")
    
except ImportError as e:
    print(f"\n[ERROR] Import error: {e}")
    print("\nPlease install dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
