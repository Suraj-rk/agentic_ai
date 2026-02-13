import time
from duckduckgo_search import DDGS
import sys
from io import StringIO
import datetime

def web_search(query: str) -> str:
    """
    Performs a web search using DuckDuckGo and returns the top results.
    
    Args:
        query (str): The search query.
        
    Returns:
        str: A formatted string containing the titles and URLs of the top search results.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}")
        
        if not results:
            return "No results found."
            
        return "\n\n".join(results)
    except Exception as e:
        return f"Error performing search: {str(e)}"

def python_repl(code: str) -> str:
    """
    Executes Python code and returns the output.
    Use this for math, data analysis, or logic problems.
    
    Args:
        code (str): The Python code to execute.
        
    Returns:
        str: The output of the executed code (stdout) or error message.
    """
    old_stdout = sys.stdout
    redirected_output = StringIO()
    sys.stdout = redirected_output
    
    try:
        # Wrap code to print the last expression if it's not a statement
        # This is a simple heuristic; a full REPL is more complex
        exec(code, globals())
        output = redirected_output.getvalue()
        if not output:
             return "Check your code. Did you forget to print() the result?"
        return output
    except Exception as e:
        return f"Error executing code: {str(e)}"
    finally:
        sys.stdout = old_stdout

def get_system_time() -> str:
    """
    Returns the current system date and time.
    Use this when asked about the current time or date.
    
    Returns:
        str: Current date and time as a string.
    """
    current_time = datetime.datetime.now().astimezone()
    return current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")

# Registry of available tools
TOOLS = {
    'web_search': web_search,
    'python_repl': python_repl,
    'get_system_time': get_system_time
}
