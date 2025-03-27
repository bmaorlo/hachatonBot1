import json
import requests
from typing import List, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_client(muid:str,first_name:str,last_name:str, client_email:str,client_phone:str,client_gender:str) -> int:
    logger.info(f"Creating Client")
    try:
        url = f"https://agent.holidayheroes.com/api/v-6/v6-release/b2b/client?muid={muid}&locale=en"
        
        payload = {
            "genderType": client_gender,
            "firstName": first_name,
            "lastName": last_name,
            "email": client_email,
            "phone": client_phone
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        logger.info(f"Payload: {payload}")
        logger.info(f"Headers: {headers}")
        logger.info(f"URL: {url}")

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        client_data = response.json()
        logger.info(f"Successfully created client with ID: {client_data['id']}")
        
        return client_data["id"]

    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating client: {response}")
        raise
    except KeyError as e:
        logger.error(f"Missing expected field 'id' in response: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating client: {str(e)}")
        raise

def add_offer_to_proposal(muid:int, proposal_id:int, offer_id:int, airport:str, adults:int, children:int, infants:int,  child_ages:List[int]) -> int:

    logger.info(f"Adding offer {offer_id} to proposal {proposal_id}")
    try:
        url = f"https://agent.holidayheroes.com/api/v-6/v6-release/b2b/proposal/{proposal_id}/offer?muid={muid}&locale=en"
        payload = {
            "proposalId": proposal_id,
            "offerId": offer_id,
            "airports":[airport],
            "originalPrice":650,
            "capacity":{
                "adult":adults,
                "child":children,
                "infant":0,
                "room":1,
                "childAges":child_ages
            }
        }
        logger.info(f"Payload: {payload}")
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        response_data = response.json()
        logger.info(f"Successfully added offer to proposal")
        
        return 0

    except requests.exceptions.RequestException as e:
        logger.error(f"Error adding offer to proposal: {str(e)}")
        raise
    except KeyError as e:
        logger.error(f"Missing expected field 'id' in response: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating client: {str(e)}")
        raise


def createProposal(muid:int, client_id:int, proposal_name:str, searchCapacity:str, searchContext:str, searchDuration:str,description:str) -> int:
    logger.info(f"Creating Proposal for client {client_id}")
    try:
        url = f"https://agent.holidayheroes.com/api/v-6/v6-release/b2b/proposal?muid={muid}&locale=en"
        
        payload = {
            "clientId": client_id,
            "name": proposal_name,
            "searchCapacity": searchCapacity,
            "searchContext": searchContext,
            "searchDuration": searchDuration,
            "description": description
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        proposal_data = response.json()
        logger.info(f"Successfully created proposal with ID: {proposal_data['id']}")
        
        return proposal_data["id"]

    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating proposal: {str(e)}")
        raise
    except KeyError as e:
        logger.error(f"Missing expected field 'id' in response: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating client: {str(e)}")
        raise