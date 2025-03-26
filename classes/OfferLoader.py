import json
import requests
from typing import List, Optional
from datetime import datetime
import logging
import calendar

#const script = document.createElement('script');
#   script.src = 'https://bot.local/chat-panel.js';
#   document.body.appendChild(script);
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_offers(muid:str, hotel_ids: List[str], search_data: dict) -> Optional[dict]:


    BASE_URL = "https://www.holidayheroes.de/api_no_auth/holiday_finder/offers/"

    if search_data["dates_type"] == "month":
        periods = search_data["dates_month"]
        year = 2025
        periods_array = [
            {
                "start": f"01/{month:02d}/{year}",
                "end": f"{calendar.monthrange(year, month)[1]:02d}/{month:02d}/{year}"
            }
            for month in periods
        ]

        logger.info(f"Maor 1\n")
        minLos = 3
        maxLos = 10

        if "dates_los" in search_data and len(search_data["dates_los"]) > 0:
            minLos = search_data["dates_los"][0]
            maxLos = minLos

        
        if "dates_los" in search_data and len(search_data["dates_los"]) > 1:
            maxLos = search_data["dates_los"][1]
        

        whenObj = {
            "months": {
                "periods": periods_array,
                "min": minLos,
                "max": maxLos,
                "nights": [minLos, maxLos]
            }
        }
        logger.info(f"Maor 2\n")
    elif search_data["dates_type"] == "specific":
        # Convert date format from YYYY-MM-DD to DD/MM/YYYY
        start_date = datetime.strptime(search_data["dates_specific"]['dates_start'], '%Y-%m-%d')
        end_date = datetime.strptime(search_data["dates_specific"]['dates_end'], '%Y-%m-%d')
        formatted_start = start_date.strftime('%d/%m/%Y')
        formatted_end = end_date.strftime('%d/%m/%Y')
        whenObj = {
            "specific": {
                "start": formatted_start,
                "end": formatted_end
            }
        }
    logger.info(f"Maor 3\n")
    starRating = []
    if "rating" in search_data:
        starRating = search_data["rating"]

    childAges = []
    if "capacity_children_ages" in search_data:
        childAges = search_data["capacity_children_ages"]

    logger.info(f"Maor 5\n")
    boardType = []
    if "hotel_board_type" in search_data:
        if isinstance(search_data["hotel_board_type"], list) and "all inclusive" in search_data["hotel_board_type"]:
            boardType = ["AI"]
        if isinstance(search_data["hotel_board_type"], list) and "breakfast and dinner" in search_data["hotel_board_type"]:
            boardType = ["HB"]
        if isinstance(search_data["hotel_board_type"], list) and "breakfast lunch and dinner" in search_data["hotel_board_type"]:
            boardType = ["FB"]
        if isinstance(search_data["hotel_board_type"], list) and "with breakfast" in search_data["hotel_board_type"]:
            boardType = ["BB"]


    adults = 2
    if "capacity_adults_num" in search_data:
        adults= search_data['capacity_adults_num']

    children = 0
    if "capacity_children_num" in search_data:
        children= search_data['capacity_children_num']


    logger.info(f"Maor 6\n")
    logger.info(f"minLos: {minLos}, maxLos: {maxLos}, boardType: {boardType}, whenObj: {whenObj}, periods: {periods}, periods_array: {periods_array}, childAges: {childAges}, starRating: {starRating}, search_data: {search_data} \n")
    try:
        # Construct request payload
        payload = {
            "locale": "de",
            "currency": "EUR",
            "fromwhere": search_data['from_airport_codes'],
            "engine": {
                "market": 1,
                "where": search_data["destinationIds"],  # Default location ID
                "when": whenObj,
                "who": {
                    "adult": adults,
                    "child": children,
                    "room": 1,
                    "childAges": childAges
                },
                "what": [],
                "whereTxt": [],
                "whatTxt": [],
                "destinationGroups": []
            },
            "filters": {
                "rating": starRating,
                "stops": [],
                "refundable": False,
                "board": boardType,
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
        logger.info(f"Maor 7 {payload}\n")
        results = {}


        timestamp = int(datetime.now().timestamp() * 1000)
        api_params = {
                "data": json.dumps(payload),
                "muid": "77cb4fd097a64e27fa65d827fcc76b34",
                "t": timestamp
            }
        
        query_params = f"?data={json.dumps(payload)}&muid=77cb4fd097a64e27fa65d827fcc76b34&t={timestamp}"
        logger.info(f"Maor 8 {query_params}\n")

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
