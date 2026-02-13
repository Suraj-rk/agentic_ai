# Agentic AI Chatbot

A smart chatbot powered by Google Gemini and equipped with web search capabilities. Built with Streamlit.

## Features
- **Agentic Capabilities**: Can reason and use tools (Web Search) to answer complex queries.
- **Powered by Gemini**: Uses Google's latest Gemini 1.5 models.
- **Streamlit interface**: Clean and responsive chat UI.
- **Customizable**: Select models and input API keys via the sidebar.

## Setup

1.  **Clone/Download the repository**.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**:
    -   Create a `.env` file in the root directory.
    -   Add your Google API Key: `GOOGLE_API_KEY=your_key_here`
    -   *Alternatively, you can enter the key in the app sidebar.*

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

## Tools
-   **Web Search**: Uses DuckDuckGo to find real-time information.
-   **Conversation**: Maintains context for follow-up questions.
