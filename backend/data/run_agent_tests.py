from src.agent.simple_agent import Agent
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

def run_tests():
    print("🤖 Initializing Agent...")
    try:
        agent = Agent()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return

    test_cases = [
        {
            "expected_type": "Task",
            "input": "Remind me to submit the quarterly report by Friday at 5 PM. Also need to email the client."
        },
        {
            "expected_type": "Idea",
            "input": "App concept: 'Uber for Dog Walkers'. Use geolocation to find nearby walkers. Features: Real-time tracking, rating system, poop bag usage stats."
        },
        {
            "expected_type": "Note",
            "input": "Meeting Quick Notes:\n- The API response time is too slow (avg 500ms).\n- We need to add Redis caching.\n- John suggested looking into database indexing."
        }
    ]

    print("\n🚀 Running Agent Classification Tests...\n")

    for i, case in enumerate(test_cases, 1):
        print(f"📋 Test Case {i}: Expected [{case['expected_type']}]")
        print(f"   Input: '{case['input'][:70]}...'")
        
        try:
            result = agent.process(case['input'])
            
            if not result:
                print("   ❌ Agent returned None")
                continue

            # Verification
            is_match = result.category == case['expected_type']
            icon = "✅" if is_match else "⚠️"
            
            print(f"   {icon} Detected Category: {result.category}")
            print(f"      Title: {result.title}")
            print(f"      Tags: {result.tags}")
            print(f"      Status: {result.status}")
            print("-" * 50)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            print("-" * 50)

if __name__ == "__main__":
    run_tests()
