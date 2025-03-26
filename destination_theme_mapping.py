import json
from typing import Dict, List, Set
from mapping import map_destination

destination_theme_names = {
    "All city trips": 20,
    "Family beach holidays": 32,
    "Beach holidays": 35,
    "City trips with kids": 46,
    "Romantic break": 47,
    "All Inclusive beach holidays": 49,
    "Insider tips": 51,
    "Adults only": 53,
    "Long-haul": 55,
    "Cities with beaches": 56,
    "Budget friendly cities": 63,
    "Cities with short flights": 66,
    "Instagrammable hotels": 73,
    "All Inclusive family holidays": 74,
    "Sustainable hotels": 76,
    "Water park fun": 87,
    "Up to 400": 88
}

theme_to_destinations = {
    "All city trips": ["Barcelona", "Paris", "Budapest", "Rome", "Milan", "Madrid", "London", "Lisbon", "Amsterdam",
                       "Prague", "Venice", "Riga", "Porto", "Vienna", "Bucharest", "Istanbul", "Dubai", "Dubrovnik",
                       "Stockholm", "Oslo", "Varna", "Warsaw", "Abu Dhabi", "Copenhagen", "Valencia", "Marseille",
                       "Nice", "Faro", "Vilnius", "Seville", "Tbilisi", "Baku", "Bari"],

    "Family beach holidays": ["Barcelona", "Paris", "Madrid", "London", "Amsterdam", "Prague", "Tenerife",
                              "Fuerteventura", "Gran Canarias", "Lanzarote", "Crete", "Chania, Crete ", "Halkidiki",
                              "Calabria", "Corsica", "Sardinia", "Turkish Riviera", "Cala Millor", "Cala Ratjada",
                              "Playa de Palma", "Puerto De Alcudia", "Magaluf", "Peguera", "Can Picafort",
                              "Santa Ponsa", "Platja de Muro"],

    "Beach holidays": ["Barcelona", "Paris", "Madrid", "London", "Ibiza", "Athens Beaches", "Amsterdam", "Naples",
                       "Venice", "Porto", "Dubrovnik", "Antalya", "Varna", "Zanzibar", "Crete", "The Maldives", "Corfu",
                       "Phuket", "Malta", "Ayia Napa", "Burgas", "Mauritius", "Hurghada", "Fuerteventura",
                       "Gran Canarias", "Lanzarote", "Madeira", "Valencia", "Montenegro", "Cancun", "Koh Samui",
                       "Punta Cana", "Seychelles", "Albanian beaches", "Sicily", "Calabria", "Corsica", "Sardinia",
                       "Turkish Riviera", "Cala Millor", "Cala Ratjada", "Playa de Palma", "Puerto De Alcudia",
                       "Magaluf", "Peguera", "Can Picafort", "Santa Ponsa", "Platja de Muro", "Agadir", "Zakynthos",
                       "Algarve", "Cala d'Or", "Bari", "Halkidiki"],

    "City trips with kids": ["Barcelona", "Paris", "Rome", "Madrid", "London", "Amsterdam", "Prague", "Dubai",
                             "Stockholm", "Varna", "Abu Dhabi", "Valencia", "Vilnius", "Bari"],

    "Romantic break": ["Paris", "Budapest", "Rome", "Milan", "Venice", "Vienna", "Porto", "Dubrovnik", "Stockholm",
                       "Oslo", "Warsaw", "Malta", "Batumi", "Nice", "Madeira", "Corsica", "Sardinia"],

    "All Inclusive beach holidays": ["Ibiza", "Palma de Mallorca", "Athens Beaches", "Mykonos", "Paphos", "Rhodes",
                                     "Kos ", "Chania, Crete ", "Santorini", "Malaga", "Limassol", "Crete", "Corfu",
                                     "Malta", "Ayia Napa", "Burgas", "Sharm El-Sheikh", "Hurghada", "Fuerteventura",
                                     "Gran Canarias", "Lanzarote", "Madeira", "Montenegro", "Cancun", "Turkish Riviera",
                                     "Cala Millor", "Cala Ratjada", "Playa de Palma", "Puerto De Alcudia", "Magaluf",
                                     "Peguera", "Can Picafort", "Santa Ponsa", "Platja de Muro", "Agadir", "Zakynthos",
                                     "Algarve"],

    "Insider tips": ["Budapest", "Prague", "Riga", "Porto", "Bucharest", "Marrakesh", "Krakow", "Sofia", "Belgrade",
                     "Stockholm", "Oslo", "Varna", "Warsaw", "Batumi", "Burgas", "Tbilisi", "Nice", "Faro", "Vilnius",
                     "Montenegro"],

    "Adults only": ["Barcelona", "Paris", "Budapest", "Rome", "Milan", "Madrid", "London", "Ibiza", "Amsterdam",
                    "Mykonos", "Naples", "Paphos", "Prague", "Venice", "Riga", "Tenerife", "Vienna", "Istanbul",
                    "Antalya", "Dubai", "Dubrovnik", "Rhodes", "Kos ", "Santorini", "Malaga", "Stockholm", "Limassol",
                    "Oslo", "Warsaw", "Abu Dhabi", "Zanzibar", "The Maldives", "Phuket", "Malta", "Ayia Napa",
                    "Mauritius", "New York", "Hurghada", "Fuerteventura", "Gran Canarias", "Lanzarote", "Madeira",
                    "Copenhagen", "Valencia", "Montenegro", "Cancun", "Koh Samui", "Punta Cana", "Seychelles",
                    "Albanian beaches", "Sicily", "Calabria", "Corsica", "Sardinia", "Turkish Riviera", "Cala Millor",
                    "Cala Ratjada", "Playa de Palma", "Puerto De Alcudia", "Magaluf", "Peguera", "Palma City",
                    "Can Picafort", "Santa Ponsa", "Platja de Muro", "Agadir", "Zakynthos", "Bari", "Halkidiki"],

    "Long-haul": ["Dubai", "Abu Dhabi", "Zanzibar", "The Maldives", "Phuket", "New York", "Cancun", "Koh Samui",
                  "Punta Cana", "Seychelles"],

    "Cities with beaches": ["Barcelona", "Athens Beaches", "Naples", "Thessaloniki", "Venice", "Porto", "Malaga",
                            "Varna", "Dubai", "Abu Dhabi", "Valencia", "Montenegro", "Baku", "Albanian beaches",
                            "Sicily", "Marseille", "Nice", "Faro", "Bari"],

    "Budget friendly cities": ["Budapest", "Bucharest", "Riga", "Krakow", "Sofia", "Belgrade", "Varna", "Warsaw",
                               "Batumi", "Burgas", "Tbilisi", "Vilnius", "Skopje"],

    "Cities with short flights": ["Barcelona", "Paris", "Budapest", "Rome", "Milan", "Madrid", "London", "Amsterdam",
                                  "Prague", "Venice", "Riga", "Vienna", "Stockholm", "Oslo", "Warsaw", "Copenhagen",
                                  "Valencia", "Nice", "Vilnius", "Seville"],

    "Instagrammable hotels": ["Barcelona", "Paris", "Budapest", "Rome", "Milan", "Madrid", "London", "Ibiza",
                              "Palma de Mallorca", "Amsterdam", "Mykonos", "Naples", "Paphos", "Prague", "Thessaloniki",
                              "Venice", "Riga", "Porto", "Tenerife", "Vienna", "Istanbul", "Antalya", "Dubai",
                              "Dubrovnik", "Rhodes", "Kos ", "Chania, Crete ", "Santorini", "Malaga", "Stockholm",
                              "Limassol", "Oslo", "Varna", "Warsaw", "Abu Dhabi", "Zanzibar", "Crete", "The Maldives",
                              "Corfu", "Phuket", "Malta", "Ayia Napa", "Batumi", "Burgas", "Mauritius", "New York",
                              "Athens", "Hurghada", "Fuerteventura", "Gran Canarias", "Lanzarote", "Madeira",
                              "Copenhagen", "Valencia", "Montenegro", "Cancun", "Koh Samui", "Punta Cana", "Seychelles",
                              "Tbilisi", "Baku", "Albanian beaches", "Sicily", "Marseille", "Nice", "Faro",
                              "Costa Blanca", "Vilnius", "Calabria", "Seville", "Corsica", "Sardinia",
                              "Turkish Riviera", "Cala Millor", "Cala Ratjada", "Playa de Palma", "Puerto De Alcudia",
                              "Magaluf", "Peguera", "Palma City", "Can Picafort", "Santa Ponsa", "Platja de Muro",
                              "Agadir", "Zakynthos", "Algarve", "Cala d'Or", "Skopje", "Bari", "Halkidiki"],

    "All Inclusive family holidays": ["Tenerife", "Crete", "Chania, Crete ", "Hurghada", "Fuerteventura",
                                      "Gran Canarias", "Lanzarote", "Turkish Riviera", "Cala Millor", "Cala Ratjada",
                                      "Playa de Palma", "Puerto De Alcudia", "Magaluf", "Peguera", "Can Picafort",
                                      "Santa Ponsa", "Platja de Muro"],

    "Sustainable hotels": ["Bari"],

    "Water park fun": ["New York", "Gran Canarias", "Lanzarote", "Corsica", "Sardinia"],

    "Up to 400": ["Barcelona", "Paris", "Budapest", "Rome", "Milan", "Madrid", "London", "Ibiza", "Palma de Mallorca",
                  "Amsterdam", "Mykonos", "Naples", "Paphos", "Prague", "Thessaloniki", "Venice", "Riga", "Porto",
                  "Tenerife", "Vienna", "Istanbul", "Antalya", "Dubai", "Dubrovnik", "Rhodes", "Kos ", "Chania, Crete ",
                  "Santorini", "Malaga", "Stockholm", "Limassol", "Oslo", "Varna", "Warsaw", "Abu Dhabi", "Zanzibar",
                  "Crete", "The Maldives", "Corfu", "Phuket", "Malta", "Ayia Napa", "Batumi", "Burgas", "Mauritius",
                  "New York", "Athens", "Hurghada", "Fuerteventura", "Gran Canarias", "Lanzarote", "Madeira",
                  "Copenhagen", "Valencia", "Montenegro", "Cancun", "Koh Samui", "Punta Cana", "Seychelles", "Tbilisi",
                  "Baku", "Albanian beaches", "Sicily", "Marseille", "Nice", "Faro", "Costa Blanca", "Vilnius",
                  "Calabria", "Seville", "Corsica", "Sardinia", "Turkish Riviera", "Cala Millor", "Cala Ratjada",
                  "Playa de Palma", "Puerto De Alcudia", "Magaluf", "Peguera", "Palma City", "Can Picafort",
                  "Santa Ponsa", "Platja de Muro", "Agadir", "Zakynthos", "Algarve", "Cala d'Or", "Skopje", "Bari",
                  "Halkidiki"]
}


def map_destination_theme(theme_name: str) -> int:
    return destination_theme_names.get(theme_name, None)


def get_destination_ids_by_themes(themes: List[str]) -> Set[int]:
    """
    Returns a set of destination IDs that match all given themes.

    Args:
        themes: List of theme names to filter by

    Returns:
        Set of destination IDs that belong to all specified themes
    """
    if not themes:
        return set()

    # Get destinations that belong to the first theme
    matching_destinations = set(theme_to_destinations.get(themes[0], []))

    # Intersect with destinations from other themes
    for theme in themes[1:]:
        theme_destinations = set(theme_to_destinations.get(theme, []))
        matching_destinations &= theme_destinations

    # Convert destination names to IDs using map_destination
    destination_ids = {map_destination(dest) for dest in matching_destinations}
    # Remove None values if any destination wasn't found
    destination_ids.discard(None)

    return destination_ids