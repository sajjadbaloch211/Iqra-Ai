
from chatbot import ChatBot

def test_teacher_query():
    bot = ChatBot()
    
    queries = [
        "Falak Memon ki counseling timing kya hai?",
        "Sarang Ahmed Friday ko kahan hote hain?",
        "Umna Iftikhar Tuesday ko available hain?"
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        response = bot.get_response(query)
        print(f"Bot: {response}")

if __name__ == "__main__":
    test_teacher_query()
