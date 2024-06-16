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


    }

    # Get a random flight:
    planes = game.airport.airspace.planes_in_airspace + game.airport.planes_at_airport + game.airport.airspace.planes_about_to_enter_airspace
    random_flight = random.choice(list(flights.keys()))
    # TODO sometimes returns already existing flight
    while random_flight in [plane.callsign for plane in planes]:
        random_flight = random.choice(list(flights.keys()))
    return flights[random_flight]

