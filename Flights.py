import random


def get_random_flight_cologne(game):
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
        9: ["EW763", "Zuerich"]
    }

    # Get a random flight:
    random_flight = random.choice(list(flights.keys()))
    while random_flight in game.airport.airspace.planes_in_airspace or random_flight in game.airport.planes_at_airport:
        random_flight = random.choice(list(flights.keys()))
    return flights[random_flight]

