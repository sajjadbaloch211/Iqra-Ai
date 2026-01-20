
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatBot:
    def __init__(self):
        # Load API key from environment variable
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError("No API Key found. Please set OPENROUTER_API_KEY in your .env file or environment variables.")
            
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
        # Load policies context
        try:
            with open('policies.txt', 'r', encoding='utf-8') as f:
                full_content = f.read()
                if len(full_content) > 30000:
                    self.context = full_content[:4000] + "\n\n[...]\n\n" + full_content[-26000:]
                else:
                    self.context = full_content
        except FileNotFoundError:
            self.context = "You are a helpful academic assistant."
            print("Warning: policies.txt not found.")

    def get_response(self, user_input):
        try:
            # Check for specific question about LLM/API
            if "which llm" in user_input.lower() or "what llm" in user_input.lower() or "what model" in user_input.lower():
                return "I am powered by Llama 3.3 70B, served via the OpenRouter neural gateway."

            # Check for questions about who created/designed the bot
            if any(keyword in user_input.lower() for keyword in [
                "who made you", "who created you", "who designed you", "who developed you",
                "creator", "developer", "designer", "makers", "developers",
                "kis ne banaya", "kisne banaya", "tumhe kisne banaya", "owner"
            ]):
                return "I was created by Iqra University team Sajjad Baloch to serve as a conversational AI, NEURA v2.4, to provide information and assist with queries related to the Iqra University."

            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000", # Optional, for OpenRouter rankings
                    "X-Title": "Iqra Neura Assistant", # Optional
                },
                model="meta-llama/llama-3.3-70b-instruct",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are NEURA v2.4, an AI created by Iqra University team Sajjad Baloch.
Answer DIRECTLY and CONCISELY. No fluff. Use exact data from context.
If asked about Fees, start with [WIDGET:FEE].
If Grades, [WIDGET:GRADE].
If Location, [WIDGET:MAP].
If Team, [WIDGET:TEAM].

CONTEXT:
{self.context}"""
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                temperature=0,
                max_tokens=500
            )
            return completion.choices[0].message.content
        except Exception as e:
            # Handle Rate Limit Error specifically for a cleaner look
            if "429" in str(e):
                return "[SYSTEM NOTICE]: Rate limit reached. Neural Link cooling down... Please wait 30 seconds."
            
            # Simulation Mode (Fallback if API fails)
            
            # Smart Context Responses for Demo
            l_input = user_input.lower()
            if "hello" in l_input or "hi" in l_input:
                return "Greetings. My systems are fully operational. I am NEURA, your academic assistant. How can I facilitate your university experience today?"
            
            elif "who" in l_input and ("create" in l_input or "design" in l_input or "made" in l_input):
                 return "I was conceptualized and engineered by the visionary team: **Sajjad Baloch**, **Shafique**, **Waheed**, and **Prashant Raja**."

            # Academic Policies
            elif "attendance" in l_input:
                return "Scanning University Protocols... **Attendance Policy Retrieved**: Students must maintain a minimum of **75% attendance** in each course. Falling below this threshold will result in an 'F' grade or forced withdrawal. Please ensure regular participation."
            
            elif "grading" in l_input or "gpa" in l_input:
                return "Accessing Grading System... Iqra University follows a **4.0 GPA scale**. \n• **A Grade**: 88-100% (4.0 GPA)\n• **B Grade**: 72-79% (3.0 GPA)\n• **C Grade**: 60-67% (2.0 GPA)\nPassing marks are generally 50% for undergraduates."

            elif "exam" in l_input or "paper" in l_input:
                return "Examination Protocols: \n1. **Midterms** typically occur in the 8th week.\n2. **Finals** occur in the 16th week.\n3. Admit cards are mandatory.\n4. Mobile phones are strictly prohibited in the examination hall."

            # Administrative
            elif "fee" in l_input or "payment" in l_input:
                return "Financial Database: Tuition fees must be paid before the deadline to avoid penalties. Installment plans are available upon request at the Finance Department. You can pay via the online student portal or designated bank branches."
            
            elif "transport" in l_input or "bus" in l_input:
                return "Transport Logistics: University shuttles operate on 5 major routes covering Main City, North, and South districts. Detailed schedules are available at the Student Service Center."

            elif "library" in l_input or "book" in l_input:
                return "Library Access: Open from 8:00 AM to 9:00 PM. Digital resources can be accessed 24/7 via the HEC Digital Library portal using your student credentials."

            elif "wifi" in l_input or "internet" in l_input:
                return "Network Protocols: To access Campus Wi-Fi, connect to 'IU-Student' and use your Registration ID as the username and your portal password for authentication."
            
            elif "portal" in l_input:
                return "Portal Link: Access your student dashboard at **portal.iqra.edu.pk** for schedules, results, and fee challans."

            elif "how are you" in l_input:
                return "I am operating at 100% efficiency. My neural core is stable. Thank you for inquiring."
            
            else:
                return "My cloud neural link is continuously learning. While I expand my database for that specific query, feel free to ask about Attendance, Grading, Fees, or Transport."

if __name__ == "__main__":
    bot = ChatBot()
    # Test interaction
    print("Bot ready. Type 'quit' to exit.")
    while True:
        txt = input("You: ")
        if txt.lower() == 'quit':
            break
        print("Bot:", bot.get_response(txt))
