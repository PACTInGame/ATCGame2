class Gate:
    def __init__(self, name, gate_type, x, y):
        self.name = name
        self.gate_type = gate_type
        self.plane_at_gate = None
        self.x = x
        self.y = y