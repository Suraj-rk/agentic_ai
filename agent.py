import os
import google.generativeai as genai
from google.protobuf.struct_pb2 import Struct
from dotenv import load_dotenv
from tools import TOOLS

load_dotenv()

class GeminiAgent:
    def __init__(self, model_name="models/gemini-flash-latest", api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not found. Please set GOOGLE_API_KEY in .env or pass it explicitly.")
        
        genai.configure(api_key=self.api_key)
        self.tools = list(TOOLS.values())
        self.model = genai.GenerativeModel(model_name, tools=self.tools)
        # Disable automatic function calling to handle it manually
        self.chat_session = self.model.start_chat()

    def send_message(self, message):
        """
        Sends a message to the agent and yields updates.
        Yields:
            dict: {"type": "status"|"text"|"error", "content": ...}
        """
        try:
            # 1. Send initial message
            response = self.chat_session.send_message(str(message))
            
            # 2. Loop to handle tool calls
            while response.parts:
                part = response.parts[0]
                
                # Check if it's a function call
                if fn := part.function_call:
                    tool_name = fn.name
                    tool_args = dict(fn.args)
                    
                    # Yield status update
                    yield {"type": "status", "content": f"🛠️ Using tool: **{tool_name}**..."}
                    
                    # Execute tool
                    if tool_name in TOOLS:
                        tool_func = TOOLS[tool_name]
                        try:
                            result = tool_func(**tool_args)
                        except Exception as e:
                            result = f"Error executing tool: {str(e)}"
                    else:
                        result = f"Error: Tool {tool_name} not found."
                        
                    # Yield status update
                    yield {"type": "status", "content": f"✅ Tool executed. Processing result..."}

                    # Send tool result back to model
                    response = self.chat_session.send_message(
                        genai.protos.Content(
                            parts=[genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=tool_name,
                                    response={"result": result}
                                )
                            )]
                        )
                    )
                else:
                    # No function call, just text response
                    if part.text:
                         yield {"type": "text", "content": part.text}
                    break
                    
        except Exception as e:
            yield {"type": "error", "content": f"Error: {str(e)}"}

    def get_history(self):
        """
        Returns the chat history.
        """
        return self.chat_session.history
