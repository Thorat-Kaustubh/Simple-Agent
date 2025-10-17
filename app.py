import streamlit as st
import asyncio
from agent import get_agent_response

# --- Page Configuration ---
st.set_page_config(page_title="Dynamic Agent", layout="centered")

# --- Custom CSS for a cleaner, dark-themed UI ---
st.markdown("""
<style>
    /* General Body Styles */
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    /* Heading Alignment */
    h1 {
        text-align: left !important;
        padding-left: 0.5rem;
    }
    /* Code Block Styles */
    .code-header {
        background-color: #3c3c3c;
        padding: 8px 12px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        color: #fff;
        font-family: monospace;
        font-size: 0.9rem;
    }
    .stCodeBlock div[data-testid="stCodeBlock"] {
        background-color: #2d2d2d;
        border-radius: 0 0 8px 8px;
        margin-top: -8px;
    }
    .stCodeBlock button[data-testid="stCopyButton"] {
        background-color: #4a4a4a !important;
        color: white !important;
        border-color: #fff !important;
    }
    .explanation {
        padding-top: 1rem;
    }
    /* Example Prompt Card Styles */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-top: 4px solid #4a90e2; /* Default top border color */
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease-in-out;
        height: 100%;
    }
    /* Assign unique top border colors to each card */
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(1) > div[data-testid="stVerticalBlock"] { border-top-color: #4a90e2; } /* Blue */
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(2) > div[data-testid="stVerticalBlock"] { border-top-color: #50e3c2; } /* Teal */
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) > div:nth-child(1) > div[data-testid="stVerticalBlock"] { border-top-color: #f5a623; } /* Orange */
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) > div:nth-child(2) > div[data-testid="stVerticalBlock"] { border-top-color: #bd10e0; } /* Purple */

    div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"]:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] h3 {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stVerticalBlock"] p {
        font-size: 0.95rem;
        color: #666;
    }
    /* Style for the agent's response card */
    div[data-testid="stChatMessage"][data-testid-chat-role="assistant"] > div {
        background-color: #f8f9fa;
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        padding: 1rem;
        color: black; /* Ensure text is readable */
    }
    /* Style for the user's response card */
    div[data-testid="stChatMessage"][data-testid-chat-role="user"] > div {
        background-color: #e7f5ff; /* A light blue for the user */
        border: 1px solid #d0ebff;
        border-radius: 10px;
        padding: 1rem;
        color: black;
    }
    /* Improved Button Styling */
    div[data-testid="stButton"] > button {
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        background-color: #ffffff;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: #f8f9fa;
        border-color: #adb5bd;
    }
</style>
""", unsafe_allow_html=True)

# --- API Key Handling (from secrets.toml only) ---
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Gemini API Key not found. Please add it to your .streamlit/secrets.toml file.")
    st.stop()

# --- Core Functions ---
def handle_prompt_submission(prompt):
    """
    Adds the user prompt to the chat, gets the agent's response,
    and adds that to the chat as well.
    """
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("🧠 Agent is thinking..."):
        response_data = asyncio.run(get_agent_response(prompt, GEMINI_API_KEY, st.session_state.messages))
    st.session_state.messages.append({"role": "assistant", "content": response_data})

def display_structured_data(data):
    """Recursively displays structured data in a user-friendly way."""
    if isinstance(data, dict):
        for key, value in data.items():
            title = key.replace('_', ' ').replace('-', ' ').title()
            if isinstance(value, dict):
                with st.expander(title, expanded=True):
                    display_structured_data(value)
            elif isinstance(value, list):
                with st.expander(title, expanded=True):
                    display_structured_data(value)
            else:
                st.markdown(f"**{title}:** {value}")
    elif isinstance(data, list):
        if not data: return
        if all(isinstance(item, (str, int, float, bool, type(None))) for item in data):
            st.markdown("\n".join([f"- {item}" for item in data]))
        else:
            for item in data:
                 if isinstance(item, dict):
                     display_structured_data(item)
                     st.markdown("---")
                 else:
                     st.markdown(f"- {item}")
    else:
        st.markdown(str(data))

def display_code_response(payload):
    """Displays the code block and its explanation."""
    language = payload.get("language", "plaintext").lower()
    code = payload.get("code", "")
    st.markdown(f"<div class='code-header'>{language}</div>", unsafe_allow_html=True)
    st.code(code, language=language)
    
    explanation = payload.get("explanation")
    if explanation:
        st.markdown("<div class='explanation'></div>", unsafe_allow_html=True)
        if isinstance(explanation, list):
             for point in explanation:
                 st.markdown(f"- **{point.get('concept')}:** {point.get('description')}")
        else:
            st.markdown(explanation)

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

if not st.session_state.messages:
    st.markdown("<h1>What can I help with?</h1>", unsafe_allow_html=True)
    
    # --- New 2x2 Grid for Example Prompts ---
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Explain a concept")
        st.write("Understand complex topics like Object-Oriented Programming.")
        if st.button("Try this example", use_container_width=True, key="oop_card_button"):
            handle_prompt_submission("Explain the main concepts of Object-Oriented Programming (OOP)")
            st.rerun()
    with col2:
        st.subheader("Generate Code")
        st.write("Create a Python script for a simple countdown timer.")
        if st.button("Try this example", use_container_width=True, key="timer_card_button"):
            handle_prompt_submission("Generate a simple Python script for a countdown timer")
            st.rerun()

    st.write("") # Spacer

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Compare two things")
        st.write("Get a structured breakdown of differences between two items.")
        if st.button("Try this example", use_container_width=True, key="compare_card_button"):
            handle_prompt_submission("Compare Python lists and tuples, explaining their key differences.")
            st.rerun()

    with col4:
        st.subheader("Solve a problem")
        st.write("Generate a function to check if a word is a palindrome.")
        if st.button("Try this example", use_container_width=True, key="palindrome_card_button"):
            handle_prompt_submission("Write a Python function to check if a string is a palindrome.")
            st.rerun()
    st.write("---")

else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            content = message["content"]
            if isinstance(content, dict):
                response_type = content.get("response_type")
                payload = content.get("payload")
                if response_type == "code":
                    display_code_response(payload)
                elif response_type == "data":
                    display_structured_data(payload)
                else:
                    st.markdown(str(content))
            else:
                st.markdown(str(content))

if prompt := st.chat_input("Ask for data or code..."):
    handle_prompt_submission(prompt)
    st.rerun()

