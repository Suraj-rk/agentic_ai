import streamlit as st
import os
from agent import GeminiAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Agentic AI Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #f0f2f6;
    }
    .stChatMessage.assistant {
        background-color: #e8f0fe;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.title("🤖 Agent Configuration")
    
    # API Key handling
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Google API Key", type="password")
    
    model_name = st.selectbox(
        "Select Model",
        ["models/gemini-flash-latest", "models/gemini-pro-latest","models/gemini-flash-lite-latest","models/gemini-2.5-flash"],
        index=0
    )
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.agent = None
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize agent if not already done, but only if API key is present
# We re-initialize if model changes could be handled here, but for simplicity:
if api_key:
    if "agent" not in st.session_state or st.session_state.get("current_model") != model_name:
        try:
             st.session_state.agent = GeminiAgent(model_name=model_name, api_key=api_key)
             st.session_state.current_model = model_name
        except Exception as e:
             st.error(f"Failed to initialize agent: {str(e)}")

# Main chat interface
st.title("Agentic AI Chatbot")
st.caption("Powered by Google Gemini & DuckDuckGo Search")

if not api_key:
    st.warning("Please enter your Google API Key in the sidebar or .env file to continue.")
else:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to state and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        if st.session_state.agent:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Container for tool status updates
                status_container = st.status("Thinking...", expanded=True)
                
                try:
                    # Iterate through the generator
                    for update in st.session_state.agent.send_message(prompt):
                        if update["type"] == "status":
                            status_container.write(update["content"])
                        elif update["type"] == "text":
                            full_response += update["content"]
                            message_placeholder.markdown(full_response)
                        elif update["type"] == "error":
                            st.error(update["content"])
                    
                    status_container.update(label="Complete", state="complete", expanded=False)
                    
                    # Add final response to history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    status_container.update(label="Error", state="error")
        else:
            st.error("Agent not initialized. Please check your API key.")
