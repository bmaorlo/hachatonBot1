import json
from typing import Dict
from mapping import map_destination

destination_group_mapping = {
    "Metropolises": 33,
    "East Europe": 35,
    "Spain": 36,
    "Scandinavia": 37,
    "Italy": 39,
    "Greece": 40,
    "Turkey": 41,
    "Egypt": 42,
    "Cyprus": 46,
    "Baltic States": 47,
    "Alpine countries": 48,
    "Mallorca": 54,
    "Long haul": 55,
    "Mediterranean Sea": 56,
    "Indian Ocean": 57,
    "Western Europe": 58,
    "United Arab Emirates": 60,
    "Canary Islands": 61,
    "Balearic Islands": 62,
    "Caribbean": 63,
    "France": 64,
    "Africa": 65,
    "Asia": 66,
    "Northern Europe": 67,
    "Bulgaria": 68,
    "Portugal": 69,
    "Europe": 70,
    "Spanish beaches": 72,
    "More beaches in Europe": 73,
    "Turkish beaches": 75,
    "Greek beaches": 76,
    "Italian beaches": 77,
    "Bulgaria Und Georgia": 79,
    "Italian cities": 81,
    "French cities": 82,
    "Cyclades": 84,
    "Ionian islands": 85,
    "Discovery": 86,
    "Balkans": 87
}


group_to_destinations = {
    "Metropolises": ["Barcelona", "Paris", "Budapest", "Rome", "Milan", "Madrid", "London", "Lisbon", "Amsterdam", "Prague", "Venice", "Vienna", "Istanbul", "Dubai", "Stockholm", "Copenhagen", "Valencia"],
    "East Europe": ["Budapest", "Prague", "Bucharest", "Krakow", "Sofia", "Belgrade", "Varna", "Warsaw", "Batumi", "Burgas", "Tbilisi", "Baku", "Vilnius", "Skopje"],
    "Spain": ["Barcelona", "Madrid", "Ibiza", "Palma de Mallorca", "Malaga", "Valencia", "Costa Blanca", "Seville", "Cala Millor", "Cala Ratjada", "Playa de Palma", "Puerto De Alcudia", "Magaluf", "Peguera", "Palma City", "Can Picafort", "Santa Ponsa", "Platja de Muro", "Cala d'Or"],
    "Scandinavia": ["Stockholm", "Oslo", "Copenhagen"],
    "Italy": ["Rome", "Milan", "Naples", "Venice", "Calabria", "Sardinia", "Bari"],
    "Greece": ["Athens Beaches", "Mykonos", "Thessaloniki", "Rhodes", "Kos ", "Chania, Crete ", "Santorini", "Crete", "Corfu", "Athens", "Zakynthos", "Halkidiki"],
    "Turkey": ["Istanbul", "Antalya"],
    "Egypt": ["Sharm El-Sheikh", "Hurghada"],
    "Cyprus": ["Paphos", "Limassol", "Ayia Napa"],
    "Baltic States": ["Riga", "Vilnius"],
    "Alpine countries": [],
    "Mallorca": [],
    "Long haul": ["Dubai", "Zanzibar", "The Maldives", "Phuket", "New York", "Cancun", "Koh Samui", "Punta Cana"],
    "Mediterranean Sea": ["Ibiza", "Palma de Mallorca", "Athens Beaches", "Mykonos", "Naples", "Paphos", "Thessaloniki", "Rhodes", "Kos ", "Chania, Crete ", "Santorini", "Malaga", "Limassol", "Crete", "Corfu", "Malta", "Ayia Napa", "Montenegro", "Sicily", "Marseille", "Nice", "Faro", "Costa Blanca", "Corsica", "Cala Millor", "Cala Ratjada", "Playa de Palma", "Puerto De Alcudia", "Magaluf", "Peguera", "Can Picafort", "Santa Ponsa", "Platja de Muro", "Zakynthos", "Cala d'Or", "Bari", "Halkidiki"],
    "Indian Ocean": ["Zanzibar", "The Maldives", "Mauritius", "Seychelles"],
    "Western Europe": ["Barcelona", "Paris", "Rome", "Milan", "Madrid", "Lisbon", "Amsterdam", "Venice", "Costa Blanca", "Calabria", "Seville", "Corsica", "Cala Millor", "Cala Ratjada", "Playa de Palma", "Puerto De Alcudia", "Magaluf", "Peguera", "Can Picafort", "Santa Ponsa", "Platja de Muro", "Cala d'Or"],
    "United Arab Emirates": ["Dubai", "Abu Dhabi"],
    "Canary Islands": ["Tenerife", "Fuerteventura", "Gran Canarias", "Lanzarote"],
    "Balearic Islands": ["Ibiza", "Palma de Mallorca"],
    "Caribbean": ["Cancun", "Punta Cana"],
    "France": ["Paris", "Disneyland Paris", "Marseille", "Nice", "Corsica"],
    "Africa": ["Sharm El-Sheikh", "Zanzibar", "Mauritius", "Hurghada", "Seychelles", "Agadir"],
    "Asia": ["Dubai", "Abu Dhabi", "The Maldives", "Phuket", "Koh Samui"],
    "Northern Europe": ["London", "Riga", "Stockholm", "Oslo", "Copenhagen"],
    "Bulgaria": ["Sofia", "Varna", "Burgas"],
    "Portugal": ["Lisbon", "Madeira", "Faro", "Algarve"],
    "Europe": ["Barcelona", "Paris", "Rome", "Milan", "Madrid", "London", "Ibiza", "Palma de Mallorca", "Lisbon", "Amsterdam", "Naples", "Prague", "Venice", "Dubrovnik", "Krakow", "Sofia", "Belgrade", "Malaga", "Stockholm", "Oslo", "Varna", "Warsaw", "Batumi", "Burgas", "Madeira", "Copenhagen", "Valencia", "Montenegro", "Costa Blanca", "Seville", "Corsica"],
    "Spanish beaches": ["Ibiza", "Palma de Mallorca", "Malaga", "Costa Blanca", "Cala Millor", "Cala Ratjada", "Playa de Palma", "Puerto De Alcudia", "Magaluf", "Peguera", "Can Picafort", "Santa Ponsa", "Platja de Muro", "Cala d'Or"],
    "More beaches in Europe": ["Barcelona", "Paris", "Budapest", "Rome", "Milan", "Madrid", "London", "Lisbon", "Amsterdam", "Naples", "Prague", "Dubrovnik", "Malaga", "Batumi", "Burgas", "Madeira", "Valencia", "Montenegro", "Sicily", "Marseille", "Nice", "Faro", "Costa Blanca", "Corsica"],
    "Turkish beaches": ["Antalya", "Turkish Riviera"],
    "Greek beaches": ["Athens Beaches", "Mykonos", "Thessaloniki", "Rhodes", "Kos ", "Chania, Crete ", "Santorini", "Crete", "Corfu", "Zakynthos", "Halkidiki"],
    "Italian beaches": ["Naples", "Sicily", "Calabria", "Sardinia"],
    "Bulgaria Und Georgia": ["Ibiza", "Palma de Mallorca", "Mykonos", "Antalya", "Kos ", "Varna", "Batumi", "Burgas"],
    "Italian cities": ["Naples", "Bari"],
    "French cities": ["Disneyland Paris"],
    "Cyclades": ["Mykonos", "Santorini"],
    "Ionian islands": ["Corfu", "Zakynthos"],
    "Discovery": ["Prague", "Dubai", "New York", "Phuket", "Madeira", "Montenegro", "Algarve"],
    "Balkans": ["Dubrovnik", "Belgrade", "Varna", "Montenegro", "Skopje"]
}


def map_destination_group(destination: str) -> int:
    return destination_group_mapping.get(destination, None)

def  get_group_destinations_ids(group: str) -> list[int]:
    destinations = group_to_destinations.get(group, [])
    return [map_destination(destination) for destination in destinations]