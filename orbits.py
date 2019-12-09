class Satellite:
    def __init__(self, focus):
        self.focus = focus

    @property
    def focii(self):
        focus = self.focus
        while focus:
            yield focus
            focus = focus.focus

class OrbitalMap (dict):
    @classmethod
    def from_input(cls, input):
        m = cls(COM=Satellite(None))

        # Clean up the input
        names = []
        for rel in input.split('\n'):
            rel = rel.strip()
            fname, sname = rel.split(')')
            names.append((fname, sname))

        # First create all the satellites without a focus
        for fname, sname in names:
            m[sname] = Satellite(None)

        # Next, set the focus on the satellites
        for fname, sname in names:
            satellite = m[sname]
            focus = m[fname]
            satellite.focus = focus

        return m

    def count_orbits(self):
        orbits = 0
        for satellite in self.values():
            while satellite.focus:
                orbits += 1
                satellite = satellite.focus
        return orbits

    def count_orbital_transfers(self, sname1, sname2):
        sat1 = self[sname1]
        sat2 = self[sname2]

        focii1 = list(sat1.focii)
        transfers = 0
        for f in sat2.focii:
            if f in focii1:
                break
            transfers += 1
        transfers += focii1.index(f)
        return transfers

def parse_orbital_map(input):
    return OrbitalMap.from_input(input)

