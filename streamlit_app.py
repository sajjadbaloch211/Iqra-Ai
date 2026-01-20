import streamlit as st
import time
from chatbot import ChatBot

# Page Config
st.set_page_config(
    page_title="NEURA v2.4 | Iqra University AI",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9ff;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    h1 {
        color: #1e293b;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .st-emotion-cache-janfss {
        background-color: #4ecdc4;
        color: white;
    }
    .st-emotion-cache-1ghh6y {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize ChatBot
if "bot" not in st.session_state:
    st.session_state.bot = ChatBot()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Greetings. I am NEURA v2.4, created by Sajjad Baloch and his team. How can I assist you with Iqra University information today?"}
    ]

# Header
st.title("Your ✨ Smart Assistant")
st.subheader("Iqra University Information Hub")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about Fees, Attendance, or Faculty..."):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Bot Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Show thinking pulse
            with st.spinner("Analyzing neural link..."):
                raw_response = st.session_state.bot.get_response(prompt)
                
            # Clean response from internal widgets if any
            clean_res = raw_response.replace("[WIDGET:FEE]", "").replace("[WIDGET:GRADE]", "").replace("[WIDGET:MAP]", "").replace("[WIDGET:TEAM]", "").replace("[WIDGET:AURA]", "").replace("**", "").strip()
            
            # Simulate streaming
            for chunk in clean_res.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Neural Link Failure: {str(e)}")
            full_response = "I encountered a synchronization error. Please try again."

    # Add Bot Message to History
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar Info
with st.sidebar:
    st.image("https://iqra.edu.pk/wp-content/uploads/2021/04/iqra-logo.png", width=150)
    st.markdown("---")
    st.write("### About NEURA")
    st.info("NEURA v2.4 is a highly advanced conversational AI designed specifically for Iqra University students and faculty.")
    st.write("**Developed by:**")
    st.success("Sajjad Baloch & Team")
    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
