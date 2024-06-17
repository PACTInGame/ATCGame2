import random


def get_random_flight(game):
    # Dictionary with all flights:
    flights = {
        1: ["EW521", "Barcelona"],
        2: ["EW583", "Palma de Mallorca"],
        3: ["DE9171", "Rom"],
        4: ["FR7211", "Palma de Mallorca"],
        5: ["IR729", "Teheran"],
        6: ["LH1980", "Muenchen"],
        7: ["OS195", "Wien"],
        8: ["TK1675", "Istanbul"],
        9: ["EW763", "Zuerich"],
        10: ["FR7213", "Palma de Mallorca"],
        11: ["KL1793", "Amsterdam"],
        12: ["LH1982", "Muenchen"],
        13: ["OS197", "Wien"],
        14: ["KL151", "New York"],
        15: ["AA145", "New Orleans"],
        16: ["AA247", "Los Angeles"],
        17: ["AA345", "Chicago"],
        18: ["AA543", "Miami"],
        19: ["AA645", "Dallas"],
        20: ["AA745", "Houston"],
        21: ["AA845", "San Francisco"],
        22: ["AA945", "Las Vegas"],
        23: ["AA1045", "Seattle"],
        24: ["AA1145", "Denver"],
        25: ["LH915", "Frankfurt"],
        26: ["LH925", "Munich"],
        27: ["LH935", "Berlin"],
        28: ["LH945", "Hamburg"],
        29: ["LH955", "Cologne"],
        30: ["LH965", "Dusseldorf"],
        31: ["LH975", "Stuttgart"],


    }

    # Get a random flight:
    planes = game.airport.airspace.planes_in_airspace + game.airport.planes_at_airport + game.airport.airspace.planes_about_to_enter_airspace
    random_flight = random.choice(list(flights.keys()))

    while flights[random_flight][0] in [plane.callsign for plane in planes]:
        random_flight = random.choice(list(flights.keys()))
    return flights[random_flight]

