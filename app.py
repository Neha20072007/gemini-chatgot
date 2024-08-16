import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Gemini Bro!",
    page_icon="💎",  # Favicon emoji
    layout="centered",  # Page layout option
    initial_sidebar_state="collapsed",
)

# Load custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #e5ddd5; /* Background color like WhatsApp */
    }
    .stButton button {
        background-color: #25D366; /* WhatsApp green for buttons */
        color: white;
        border-radius: 20px; /* Rounded corners for button */
        padding: 10px 20px;
        margin-top: 10px;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #128C7E; /* Darker green for hover effect */
    }
    .chat-bubble {
        border-radius: 15px; /* Rounded corners for chat bubbles */
        padding: 10px 15px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 70%;
        animation: fadeIn 0.5s;
        font-size: 16px; /* Adjust font size for readability */
    }
    .chat-bubble.you {
        background-color: #DCF8C6; /* Light green for user messages */
        color: black;
        align-self: flex-end;
    }
    .chat-bubble.bro {
        background-color: #FFFFFF; /* White for AI messages */
        color: black;
        align-self: flex-start;
    }
    .chat-title {
        font-family: 'Arial', sans-serif;
        color: #25D366; /* WhatsApp green for title */
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Retrieve the Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "ai"
    else:
        return "human"

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("💎 Gemini Bro", anchor=None)
st.markdown("<h3 class='chat-title'>Your AI-powered assistant</h3>", unsafe_allow_html=True)

# Display the chat history
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    bubble_class = "chat-bubble you" if role == "you" else "chat-bubble bro"
    with st.chat_message(role):
        st.markdown(f"<div class='{bubble_class}'>{message.parts[0].text}</div>", unsafe_allow_html=True)

# Input field for user's message
user_prompt = st.chat_input("Type your message here...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("human").markdown(f"<div class='chat-bubble you'>{user_prompt}</div>", unsafe_allow_html=True)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("ai"):
        st.markdown(f"<div class='chat-bubble bro'>{gemini_response.text}</div>", unsafe_allow_html=True)
