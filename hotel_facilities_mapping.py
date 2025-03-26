import json
from typing import Dict, List

# Create mapping of English names to IDs
hotel_facilities_mapping = {
    "Parking": "6",
    "Pool": "8",
    "Pet friendly": "9",
    "Room with Kitchen": "10",
    "Free WI-FI": "11",
    "Air conditioning": "12",
    "Restaurant": "13",
    "Room service": "14",
    "Spa": "18",
    "Kids Club": "22",
    "Private beach": "23",
    "Casino": "24",
    "Family friendly": "25",
    "Water park": "36"
}


def get_facilites_ids(facility_names: List[str]) -> List[str]:
    """
    Convert facility names to their corresponding IDs.

    Args:
        facility_names: List of facility names in English

    Returns:
        List of facility IDs as strings
    """
    facility_ids = []
    for name in facility_names:
        if name in hotel_facilities_mapping:
            facility_ids.append(hotel_facilities_mapping[name])
    return facility_ids