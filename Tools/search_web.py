"""
Simple Web Search with Brave Browser
Directly opens Brave browser and searches user's query
"""

import webbrowser
import urllib.parse
from livekit.agents import function_tool

@function_tool()
async def search_web(query: str) -> str:
    """
    Opens Brave Browser and searches the user's query directly in the browser.
    
    Args:
        query: User's search question or terms
        
    Returns:
        str: Confirmation message that search has been opened
    """
    try:
        # Encode the query for URL
        encoded_query = urllib.parse.quote_plus(query)
        
        # Create search URL
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        # Open Microsoft Edge with the search
        webbrowser.register('brave', None, webbrowser.BackgroundBrowser("C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"))
        webbrowser.get('brave').open_new_tab(search_url)
        
        return f"✅ मैंने Brave Browser में आपकी query '{query}' के लिए search open कर दिया है। ब्राउज़र में results देखें!"
        
    except Exception as e:
        # Fallback - use default browser
        try:
            search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
            webbrowser.open_new_tab(search_url)
            return f"✅ मैंने आपकी query '{query}' के लिए browser में search open कर दिया है।"
        except Exception as e2:
            return f"❌ Browser में search open करने में problem आई: {e2}"

