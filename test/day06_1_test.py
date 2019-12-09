import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from orbits import parse_orbital_map

def test_example():
    m = parse_orbital_map(
        '''COM)B
            B)C
            C)D
            D)E
            E)F
            B)G
            G)H
            D)I
            E)J
            J)K
            K)L''')

    count = m.count_orbits()
    assert count == 42
