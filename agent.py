import google.generativeai as genai
import asyncio
import json
from google.api_core import exceptions

async def get_agent_response(user_prompt: str, api_key: str, chat_history: list):
    """
    Asynchronously generates a response using a robust, single-call approach.
    It instructs the model to decide the response format (code or data) internally.
    """
    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        
        context = ""
        # Limit history to the last 4 messages to keep the prompt efficient
        for message in chat_history[-4:]:
            role = "User" if message["role"] == "user" else "Agent"
            content = message["content"]
            if isinstance(content, dict):
                content = json.dumps(content)
            context += f"{role}: {content}\n"
            
        # A single, powerful prompt that lets the model decide the output structure
        prompt = f"""
        You are an intelligent assistant. Based on the chat history and new prompt,
        analyze the user's request and provide the most appropriate response.

        Respond with a single JSON object with a "response_type" key, which can be "data" or "code".

        1. If the user is asking for information, data, or an explanation, set "response_type" to "data".
           The JSON should also have a "payload" key containing the structured data.
           Example: {{ "response_type": "data", "payload": {{ "topic": "Photosynthesis", "summary": "..." }} }}

        2. If the user is asking for a code snippet, set "response_type" to "code".
           The JSON should also have a "payload" key containing an object with "language", "code", and "explanation" keys.
           Example: {{ "response_type": "code", "payload": {{ "language": "python", "code": "print('Hello')", "explanation": "..." }} }}

        --- CHAT HISTORY ---
        {context}
        --- NEW USER PROMPT ---
        {user_prompt}
        """
        
        # Use asyncio.wait_for to add a timeout, preventing indefinite hangs
        response = await asyncio.wait_for(
            model.generate_content_async(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            ),
            timeout=60.0  # 60-second timeout
        )

        # Robust check for content safety blocks
        if response.prompt_feedback.block_reason:
            return {"error": f"Your request was blocked by the safety policy: {response.prompt_feedback.block_reason.name}"}

        return json.loads(response.text)

    except asyncio.TimeoutError:
        return {"error": "The request timed out. The agent is taking too long to respond. Please try again."}
    except exceptions.PermissionDenied:
        return {"error": "Authentication failed: Your API key is invalid or has insufficient permissions."}
    except json.JSONDecodeError:
        return {"error": "The agent returned a malformed response. Please try rephrasing your prompt."}
    except Exception as e:
        print(f"An unexpected error occurred in get_agent_response: {e}")
        return {"error": "An unexpected critical error occurred. I am unable to respond at this moment."}

