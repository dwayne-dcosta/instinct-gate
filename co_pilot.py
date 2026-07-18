import os
import sys
import google.generativeai as genai

# Verify API Key is fully registered inside the active environment shell profiles
if not os.environ.get("GEMINI_API_KEY"):
    print("❌ Error: GEMINI_API_KEY environment variable not found.")
    print("Please run: export GEMINI_API_KEY='your_key'")
    sys.exit(1)

# Initialize the generative environment framework
genai.configure()

# Initialize the high-capacity, enterprise-grade systems infrastructure model
model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

print("\n" + "="*60)
print("🛡️ INSTINCT GATE SYSTEMS CO-PILOT ENGAGED (TERMINAL CORE)")
print("Status: Active | Context Window: Uncapped | Exit: Type 'exit'")
print("="*60)

while True:
    try:
        user_prompt = input("\nLead Architect > ")
        if user_prompt.strip().lower() in ['exit', 'quit']:
            print("\n👋 Disconnecting system co-pilot. Core environment secured.")
            break
            
        if not user_prompt.strip():
            continue
            
        print("\n⚙️ Processing pipeline evaluation...")
        response = chat.send_message(user_prompt)
        print(f"\n[SYSTEM RESPONSE]:\n{response.text}")
        print("-" * 60)
        
    except KeyboardInterrupt:
        print("\n\n👋 Forced session break executed. Core environment secured.")
        break
    except Exception as e:
        print(f"\n❌ Pipeline Error: {str(e)}")
