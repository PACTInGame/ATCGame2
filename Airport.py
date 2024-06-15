class Airport:
    def __init__(self, name, gates, runway):
        self.name = name
        self.gates = gates
        self.planes_at_airport = []
        self.runway = runway

    def add_gate(self, gate):
        self.gates.append(gate)

