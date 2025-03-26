import json
import requests
from typing import List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_offers(muid:str, hotel_ids: List[str], destination_ids: List[int]) -> Optional[dict]:

    BASE_URL = "https://www.holidayheroes.de/api_no_auth/holiday_finder/offers/"

    try:
        # Construct request payload
        payload = {
            "locale": "de",
            "currency": "EUR",
            "fromwhere": ['BER'],
            "engine": {
                "market": 1,
                "where": destination_ids,  # Default location ID
                "when": {
                    "months": {
                        "periods": [],
                        "min": None,
                        "max": None,
                        "nights": []
                    }
                },
                "who": {
                    "adult": 2,
                    "child": 0,
                    "room": 1,
                    "childAges": []
                },
                "what": [],
                "whereTxt": ["Paris"],
                "whatTxt": [],
                "destinationGroups": []
            },
            "filters": {
                "rating": [],
                "stops": [],
                "refundable": False,
                "board": [],
                "amenities": [],
                "amenitiesTxt": [],
                "luggage": {
                    "canAddTrolley": False,
                    "canAddCib": False
                },
                "flex": False
            },
            "sort": {"best": -1},
            "limit": 10,
            "offset": 0,
            "specificHotel": {
                "hotel_id": hotel_ids
            },
            "searchUserProfile": 0,
            "onlySpecificHotelIds": "true"
        }

        results = {}


        timestamp = int(datetime.now().timestamp() * 1000)
        api_params = {
                "data": json.dumps(payload),
                "muid": "77cb4fd097a64e27fa65d827fcc76b34",
                "t": timestamp
            }
        
        query_params = f"?data={json.dumps(payload)}&muid=77cb4fd097a64e27fa65d827fcc76b34&t={timestamp}"

        url = BASE_URL + query_params
        logger.info(f"Making OFFERS API request to: {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

        
    except requests.exceptions.RequestException as e:
        print(f"Error loading offers: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {str(e)}")
        return None
