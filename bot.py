import os
import json
import asyncio
import logging
from typing import Dict, Any
from fastapi import FastAPI, WebSocket
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import mapping
import destination_group_mapping
import destination_theme_mapping
import hotel_facilities_mapping
import classes.HotelSearcher as HotelSearcher
import classes.OfferLoader as OfferLoader
import classes.Proposal as Proposal
import classes.HotelFilter as HotelFilter
from itertools import chain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Check for required environment variables
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store active conversations
active_conversations: Dict[str, Any] = {}

def validate_search_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean search parameters
    """
    validated_params = {}
    
    # Validate stars
    if "stars" in params:
        stars = params["stars"]
        if isinstance(stars, list):
            validated_params["stars"] = [star for star in stars if 1 <= star <= 5]
    
    # Validate destination names
    if "destinationNames" in params:
        destinations = params["destinationNames"]
        if isinstance(destinations, list):
            validated_params["destinationNames"] = destinations
    
    # Validate max price
    if "max_price_per_person" in params:
        price = params["max_price_per_person"]
        if isinstance(price, (int, float)) and 0 <= price <= 2000:
            validated_params["max_price_per_person"] = price
    
    # Validate weekend only
    if "weekendOnly" in params:
        validated_params["weekendOnly"] = bool(params["weekendOnly"])
    
    # Validate vacation type
    if "vacation_type" in params:
        vacation_types = params["vacation_type"]
        if isinstance(vacation_types, list):
            validated_params["vacation_type"] = vacation_types
    
    # Validate room board type
    if "room_board_type" in params:
        board_types = params["room_board_type"]
        if isinstance(board_types, list):
            validated_params["room_board_type"] = board_types
    
    # Validate hotel type and facilities
    if "hotel_type_and_facilities" in params:
        facilities = params["hotel_type_and_facilities"]
        if isinstance(facilities, list):
            validated_params["hotel_type_and_facilities"] = facilities
    
    # Validate travel month
    if "travelMonth" in params:
        months = params["travelMonth"]
        if isinstance(months, list):
            validated_params["travelMonth"] = [month for month in months if 1 <= month <= 12]
    
    # Validate number of nights
    if "number_of_nights" in params:
        nights = params["number_of_nights"]
        if isinstance(nights, list):
            validated_params["number_of_nights"] = nights
    
    # Validate vacation dates
    if "vacation_specific_dates" in params:
        dates = params["vacation_specific_dates"]
        if isinstance(dates, dict) and "start_date" in dates and "end_date" in dates:
            try:
                start_date = datetime.strptime(dates["start_date"], "%Y-%m-%d")
                end_date = datetime.strptime(dates["end_date"], "%Y-%m-%d")
                if start_date < datetime.now():
                    raise ValueError("Start date must be in the future")
                if end_date < start_date:
                    raise ValueError("End date must be after start date")
                validated_params["vacation_specific_dates"] = dates
            except ValueError as e:
                logger.error(f"Date validation error: {str(e)}")
    
    # Validate vacation date range
    if "vacation_date_range" in params:
        date_range = params["vacation_date_range"]
        if isinstance(date_range, dict) and "start_date" in date_range and "end_date" in date_range:
            try:
                start_date = datetime.strptime(date_range["start_date"], "%Y-%m-%d")
                end_date = datetime.strptime(date_range["end_date"], "%Y-%m-%d")
                if start_date < datetime.now():
                    raise ValueError("Start date must be in the future")
                if end_date < start_date:
                    raise ValueError("End date must be after start date")
                validated_params["vacation_date_range"] = date_range
            except ValueError as e:
                logger.error(f"Date range validation error: {str(e)}")
    
    # Validate adults and children capacity
    if "adults_children_capacity" in params:
        capacity = params["adults_children_capacity"]
        if isinstance(capacity, dict):
            validated_capacity = {}
            
            if "number_of_adults" in capacity:
                validated_capacity["number_of_adults"] = max(0, int(capacity["number_of_adults"]))
            
            if "number_of_children" in capacity:
                validated_capacity["number_of_children"] = max(0, int(capacity["number_of_children"]))
            
            if "children_ages" in capacity:
                ages = capacity["children_ages"]
                if isinstance(ages, list):
                    validated_capacity["children_ages"] = [
                        age for age in ages 
                        if isinstance(age, (int, float)) and 1 <= age <= 17
                    ]
            
            validated_params["adults_children_capacity"] = validated_capacity
    
    return validated_params

def make_search(json_data: str) -> str:
    """
    Function to handle holiday search requests
    """
    muid = "0c69129df16fc8e99d5975f10617a504"
    try:
        # Parse the JSON data
        search_data = json.loads(json_data)
        logger.info(f"Received search request with data: {search_data}")
        if "destination_anywhere" in search_data:
            search_data["destinationIds"] = []
            
        if "destination_names" in search_data:
            search_data["destinationIds"] = [mapping.map_destination(destination) for destination in search_data["destination_names"]]


        if "destination_theme_names" in search_data:
            mapped_ids = destination_theme_mapping.get_destination_ids_by_themes(search_data["destination_theme_names"])

            if "destinationIds" not in search_data:
                search_data["destinationIds"] = []
            search_data["destinationIds"].extend(mapped_ids)

        if "hotel_facilities" in search_data:
            mapped_ids = hotel_facilities_mapping.get_facilites_ids(search_data["hotel_facilities"])

            if "amenities" not in search_data:
                search_data["amenities"] = []
            search_data["amenities"].extend(mapped_ids)


        if "destination_group_names" in search_data:
            mapped_ids = list(chain.from_iterable(
                destination_group_mapping.get_group_destinations_ids(group_name)
                for group_name in search_data["destination_group_names"]
            ))

            if "destinationIds" not in search_data:
                search_data["destinationIds"] = []
            search_data["destinationIds"].extend(mapped_ids)


        search_data["destinationIds"] = [d for d in search_data["destinationIds"] if d is not None]


        logger.info("Finished Mapping")
        logger.info("#############")
        logger.info(f"Destinations ids: {search_data['destinationIds']}")
        logger.info("########")

        logger.info(f"Start to search for hotels")
        hotels = HotelSearcher.searchHotels(search_data)

        if "unknown_hotel_preferences" in search_data and search_data["unknown_hotel_preferences"]:
            assistant_id = os.getenv("ASSISTANT_HOTEL_FILTER_ID")
            logger.info(f"Start to search for hotels with assistant {assistant_id}")
            hotels = HotelFilter.searchHotelsWithAssistant(hotels,search_data['unknown_hotel_preferences'], assistant_id)


        logger.info(f"Hotels: {hotels}")
        # Extract hotel IDs from the search results
        hotel_ids = []
        if "result" in hotels:
            hotel_ids = [hotel["id"] for hotel in hotels["result"]]

        logger.info(f"Finished searching for hotels")


        logger.info(f"Start to load offers search data: {search_data}")
        offers = OfferLoader.load_offers(muid, hotel_ids, search_data)
        #logger.info(f"Offers: {offers}")
        logger.info(f"Finished loading offers")
        
        # Collect offer IDslo and capacities
        capacity_adult = 2
        capacity_child = 0
        offer_details = []
        if "data" in offers:
            if "offers" in offers["data"]:
                for offer_data in offers["data"]["offers"]:
                    if "offer" in offer_data:
                        offer = offer_data["offer"]
                        capacityString = f"{offer['capacity']['adult']}-{offer['capacity']['child']}"
                    offer_details.append({
                        "offerId": offer["hfOfferId"],
                        "capacity": {
                            "adult": offer["capacity"]["adult"],
                            "child": offer["capacity"]["child"],
                            "infant": offer["capacity"].get("infant", None)
                        }
                    })
        
        logger.info(f"Offer details: {offer_details}")
        
        
        logger.info(f"Start to create client")
        client_id = Proposal.create_client(muid,search_data['customer_first_name'], search_data['customer_last_name'],"drork@drorio.wearemove.io", 972542601022, "Mr")
        logger.info(f"Finished creating client {client_id}")

        logger.info(f"Start to create proposal")
        proposal_id = Proposal.createProposal(muid,client_id, search_data['proposal_name'], capacityString, '', '',search_data['proposal_details'])
        logger.info(f"Finished creating proposal {proposal_id}")

        logger.info(f"Start to add offer to proposal")
        totaloffers = 0
        for offer in offer_details:
            totaloffers += 1
            if totaloffers < 11:
                Proposal.add_offer_to_proposal(
                    muid,
                    proposal_id, 
                    offer["offerId"],
                    'BER',  # Default departure airport
                    offer["capacity"]["adult"],
                    offer["capacity"]["child"],
                    offer["capacity"].get("infant", 0),
                    []  # Empty list for child ages
                )
        #Proposal.add_offer_to_proposal(muid,proposal_id, "m1d248h4110365c20o210525i240525aBERst1", 'BER', 2, 0, 0, [])
        logger.info(f"Finished adding offer to proposal")


        return json.dumps({
            "status": "success",
            "message": f"those are the hotels {offer_details} and the proposal page is here https://agent.holidayheroes.com/holidayfinder/proposal/view/{proposal_id}??b2bcustomerview=true",
            "data": search_data
        })
    except json.JSONDecodeError:
        return json.dumps({
            "status": "error",
            "message": "Invalid JSON format"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

def get_or_create_assistant():
    """
    Get the assistant ID from environment or create a new assistant
    """
    assistant_id = os.getenv("ASSISTANT_ID")
    
    if assistant_id:
        try:
            # Try to retrieve the existing assistant
            assistant = client.beta.assistants.retrieve(assistant_id)
            logger.info(f"Found existing assistant: {assistant.name}")
            return assistant_id
        except Exception as e:
            logger.warning(f"Could not find assistant with ID {assistant_id}: {str(e)}")
    
    # Create a new assistant
    logger.info("Creating new assistant")
    assistant = client.beta.assistants.create(
        name="Holiday Search Assistant",
        instructions="""You are a helpful AI assistant that helps users find their perfect holiday.
        When a user asks about holiday options, use the makeSearch function with the appropriate parameters.
        Always try to understand the user's preferences and convert them into structured search parameters.
        If the user mentions a broad destination (like Europe), include all relevant cities in the destinationNames array.
        Make sure to validate dates and ensure they are in the future.
        Format all responses in a user-friendly way.""",
        model="gpt-4-turbo-preview",
        tools=[{
            "type": "function",
            "function": {
                "name": "makeSearch",
                "description": "Do a search for holidays based on the user search criteria",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "stars": {
                            "type": "array",
                            "description": "the star rating to apply",
                            "items": {
                                "type": "number",
                                "enum": [1, 2, 3, 4, 5]
                            }
                        },
                        "destinationNames": {
                            "type": "array",
                            "description": "The destination it's possible to search vacation at",
                            "items": {
                                "type": "string",
                                "enum": ["Paris", "Faro"]
                            }
                        },
                        "max_price_per_person": {
                            "type": "number",
                            "min": 0,
                            "max": 2000
                        },
                        "weekendOnly": {
                            "type": "boolean",
                            "description": "if the customer want trips only at weekend"
                        },
                        "vacation_type": {
                            "type": "array",
                            "description": "The theme of the vacation the customer is looking for",
                            "items": {
                                "type": "string",
                                "enum": ["Casino Trip", "Instagram Places"]
                            }
                        },
                        "room_board_type": {
                            "type": "array",
                            "description": "The room board type",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "room only",
                                    "with breakfast",
                                    "breakfast and dinner",
                                    "breakfast lunch and dinner",
                                    "all inclusive"
                                ]
                            }
                        },
                        "hotel_type_and_facilities": {
                            "type": "array",
                            "description": "The type of hotel and the facilities that the hotel have in it",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "Parking",
                                    "Close to beach",
                                    "All inclusive hotel",
                                    "hotel have Water park"
                                ]
                            }
                        },
                        "travelMonth": {
                            "type": "array",
                            "description": "the number that represent the month of his travel plans",
                            "items": {
                                "type": "number"
                            }
                        },
                        "number_of_nights": {
                            "type": "array",
                            "description": "The number of nights the customer want to travel",
                            "items": {
                                "type": "number"
                            }
                        },
                        "vacation_specific_dates": {
                            "type": "object",
                            "description": "The starting date and end date of the range of dates the customer is willing to travel",
                            "properties": {
                                "start_date": {
                                    "type": "string",
                                    "format": "date"
                                },
                                "end_date": {
                                    "type": "string",
                                    "format": "date"
                                }
                            }
                        },
                        "vacation_date_range": {
                            "type": "object",
                            "description": "The starting date and end date of the range of dates the customer is willing to travel",
                            "properties": {
                                "start_date": {
                                    "type": "string",
                                    "format": "date"
                                },
                                "end_date": {
                                    "type": "string",
                                    "format": "date"
                                }
                            }
                        },
                        "adults_children_capacity": {
                            "type": "object",
                            "description": "how much and who are the people that is traveling",
                            "properties": {
                                "number_of_adults": {
                                    "type": "number",
                                    "description": "the number of adults that is going to the vacation"
                                },
                                "number_of_children": {
                                    "type": "number",
                                    "description": "the number of children that is going to the vacation"
                                },
                                "children_ages": {
                                    "type": "array",
                                    "description": "The ages of the children, can be from age 1 to 17",
                                    "items": {
                                        "type": "number",
                                        "min": 1,
                                        "max": 17
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }]
    )
    
    # Save the new assistant ID to .env file
    with open('.env', 'a') as f:
        f.write(f"\nASSISTANT_ID={assistant.id}")
    
    logger.info(f"Created new assistant with ID: {assistant.id}")
    return assistant.id

# Get or create assistant at startup
ASSISTANT_ID = get_or_create_assistant()

async def process_message_with_assistant(message: str, conversation_id: str) -> str:
    """
    Process a message using the OpenAI assistant and return the response.
    """
    try:
        logger.info(f"Processing message for conversation {conversation_id}")
        
        # Get or create conversation thread
        if conversation_id not in active_conversations:
            logger.info("Creating new thread")
            thread = client.beta.threads.create()
            active_conversations[conversation_id] = thread.id
        else:
            logger.info("Retrieving existing thread")
            thread_id = active_conversations[conversation_id]
            thread = client.beta.threads.retrieve(thread_id)

        # Add message to thread
        logger.info("Adding message to thread")
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Run the assistant
        logger.info("Running assistant")
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            logger.info(f"Run status: {run_status.status}")
            
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                logger.error(f"Run failed: {run_status.last_error}")
                return f"Sorry, I encountered an error: {run_status.last_error}"
            elif run_status.status == 'expired':
                logger.error("Run expired")
                return "Sorry, the request timed out. Please try again."
            elif run_status.status == 'requires_action':
                # Handle function calls
                for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "makeSearch":
                        # Get the JSON parameter
                        args = json.loads(tool_call.function.arguments)
                        
                        # Call the function
                        result = make_search(json.dumps(args))
                        
                        # Submit the result back to the assistant
                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": result
                            }]
                        )
            
            await asyncio.sleep(1)

        # Get the assistant's response
        logger.info("Retrieving assistant response")
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0]
        
        return last_message.content[0].text.value

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        return f"Sorry, I encountered an error: {str(e)}"

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    logger.info(f"New WebSocket connection from client {client_id}")
    
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            logger.info(f"Received message from client {client_id}: {message}")
            
            # Process message with OpenAI assistant
            response = await process_message_with_assistant(message, client_id)
            
            # Send response back to client
            await websocket.send_text(response)
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
    finally:
        await websocket.close()
        logger.info(f"WebSocket connection closed for client {client_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 