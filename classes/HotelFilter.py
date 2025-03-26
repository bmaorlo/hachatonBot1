import json
import requests
from typing import List, Optional
from datetime import datetime
import logging
from openai import OpenAI
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def searchHotelsWithAssistant(hotels: List[dict], unknown_preferences: str, assistant_id: str) -> List[dict]:
    """
    Filter hotels using OpenAI assistant based on unknown preferences.
    
    Args:
        hotels (List[dict]): List of hotel objects to filter
        unknown_preferences (str): Natural language description of hotel preferences
        assistant_id (str): OpenAI assistant ID to use for filtering
        
    Returns:
        List[dict]: Filtered list of hotels based on assistant's analysis
    """
    logger.info(f"Filter hotels in assistant {hotels}")
    try:
        logger.info(f"Starting hotel filtering with assistant {assistant_id}")
        
        # Create a thread for this filtering session
        thread = client.beta.threads.create()
        
        request_body = {
            "hotels": hotels,
            "additional_preferences": unknown_preferences
        }
        # Prepare the message for the assistant
        message_content = json.dumps(request_body)
        logger.info(f"Message content: {message_content}")
        
        # Add the message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message_content
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        
        loops = 0
        # Wait for the run to complete
        while True:
            loops += 1
            if loops > 10:
                logger.error("Assistant run failed to complete")
                return hotels  # Return original hotels if assistant fails
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if run_status.status == 'completed':
                break
            elif run_status.status in ['failed', 'expired']:
                logger.error(f"Assistant run {run_status.status}: {run_status.last_error if hasattr(run_status, 'last_error') else 'Unknown error'}")
                return hotels  # Return original hotels if assistant fails
                
            # Add a small delay before checking again
            import time
            time.sleep(1)
        
        # Get the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0]
        responseText = last_message.content[0].text.value
        
        responseText = responseText.replace("```json", "").replace("```", "")
        logger.info(f"Last message: {responseText}")
        try:
            # Parse the assistant's response as JSON
            filtered_hotel_ids = json.loads(responseText)
            logger.info(f"Filtered hotel ids: {filtered_hotel_ids}")
            return filtered_hotel_ids
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse assistant response as JSON: {str(e)}")
            return hotels  # Return original hotels if parsing fails
            
    except Exception as e:
        logger.error(f"Error in searchHotelsWithAssistant: {str(e)}")
        return hotels  # Return original hotels if any error occurs
