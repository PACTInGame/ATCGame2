class Airport:
    def __init__(self, name, gates, runway, airspace):
        self.name = name
        self.gates = gates
        self.planes_at_airport = []
        self.runway = runway
        self.airspace = airspace
        self.wind = "260° 9kn gusting 15kn. QNH 1011"
        # TODO multiple wind options

    def add_gate(self, gate):
        self.gates.append(gate)

