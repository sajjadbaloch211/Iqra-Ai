
import os
import requests
import json
from dotenv import load_dotenv
from knowledge_base_engine import KnowledgeBaseEngine

# Load environment variables
load_dotenv()

class ChatBot:
    def __init__(self):
        # Load Groq API key
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("No GROQ_API_KEY found. Please set it in your .env file.")
            
        # Initialize RAG Engine (Iqra Virtual Brain)
        self.kb = KnowledgeBaseEngine()
        
        # Auto-ingest if index is missing but data exists
        if self.kb.index is None and os.path.exists('knowledge_base'):
            print("No index found. Ingesting knowledge_base for the first time...")
            self.kb.ingest_directory('knowledge_base')
        
        # CONVERSATION MEMORY: Keep track of history like ChatGPT
        self.history = []

    def get_response(self, user_input):
        try:
            # Check for specific questions about LLM/API
            if any(k in user_input.lower() for k in ["which llm", "what llm", "what model"]):
                return "I am powered by Llama 3.1 8B via Groq ultra-fast inference engine."

            # Check for creator questions
            if any(keyword in user_input.lower() for keyword in [
                "who made you", "who created you", "who designed you", "who developed you",
                "creator", "developer", "designer", "makers", "developers",
                "kis ne banaya", "kisne banaya", "tumhe kisne banaya", "owner"
            ]):
                return "I was created by Iqra University team Sajjad Baloch to serve as a conversational AI assistant for students."

            # 1. RETRIEVE context from knowledge base (RAG)
            search_k = 5
            person_keywords = ["teacher", "faculty", "staff", "lecturer", "professor", "list", "who is", "about", "info", "information", "how many", "total", "count", "all", "schedule", "free", "time", "when", "class", "shadule"]
            if any(k in user_input.lower() for k in person_keywords) or len(user_input.split()) < 5:
                # Increase context size for lists (12*600 = 7.2k chars ~ 1.8k tokens) - Safe for Groq
                search_k = 12
                
            dynamic_context = self.kb.search(user_input, top_k=search_k)

            # SPECIAL TRIGGER: If asking for full teacher list/count, inject the full directory file
            # This fixes the issue where RAG only returns a few chunks (e.g. 15 teachers instead of 55)
            if any(k in user_input.lower() for k in ["how many", "count", "list", "all", "total"]) and \
               any(k in user_input.lower() for k in ["teacher", "faculty", "staff", "professor"]):
                try:
                    with open(os.path.join('knowledge_base', 'iqra_faculty_directory.txt'), 'r', encoding='utf-8') as f:
                        full_directory = f.read()
                        dynamic_context += f"\n\n=== FULL FACULTY DIRECTORY ===\n{full_directory}\n"
                except Exception as e:
                    print(f"Error reading directory file: {e}")
            
            # 2. CALL GROQ API via requests
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            system_prompt = f"""You are NEURA v2.4, an ultra-intelligent and helpful AI assistant for Iqra University. 
Your goal is to behave like ChatGPT but with specialized knowledge of Iqra University.

GUIDELINES:
1. ANSWER ONLY WHAT IS ASKED. Do not provide extra context unless requested.
2. If the user asks "When is [Teacher] free?", ONLY list the specific days and times they are free. Do NOT show their full busy schedule.
3. Keep answers SHORT and PRECISE.
4. If the user asks for a list (teachers, programs), THEN provide a complete list.
5. Be polite but strictly to the point.
6. Answer in the same language the user is using.

UNIVERSITY CONTEXT:
{dynamic_context}

CRITICAL INSTRUCTION:
If the answer is found in the UNIVERSITY CONTEXT above, use it.
If the answer is NOT in the context, use your general knowledge to answer helpfuly, but state "Based on general knowledge...". 
NEVER say "I don't have information" unless it's a very specific private query (like a student's personal phone number).
For teachers/courses not in context, give a general polite response about checking the official portal."""

            # Construct messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add history
            for h in self.history[-8:]:
                messages.append(h)
                
            # Add current user input
            messages.append({"role": "user", "content": user_input})

            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": messages,
                "temperature": 0.4,
                "max_tokens": 1024
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                bot_response = result['choices'][0]['message']['content']
                
                # Update history
                self.history.append({"role": "user", "content": user_input})
                self.history.append({"role": "assistant", "content": bot_response})
                
                return bot_response
            else:
                return f"Error from Groq API: {response.status_code} - {response.text[:200]}"

        except Exception as e:
            return f"Error: {str(e)[:50]}..."

if __name__ == "__main__":
    bot = ChatBot()
    print("Bot ready (Groq Enabled). Type 'quit' to exit.")
    while True:
        txt = input("You: ")
        if txt.lower() == 'quit':
            break
        print("Bot:", bot.get_response(txt))
