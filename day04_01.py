#!/usr/bin/env python3

def is_valid(pw):
    pw = str(pw)
    d1 = pw[0]
    found_repeat = False
    for d2 in pw[1:]:
        if d2 < d1:
            return False
        elif d2 == d1:
            found_repeat = True
        d1 = d2
    return found_repeat

def count_passwords(low, high):
    valid_count = 0
    for pw in range(low, high + 1):
        if is_valid(pw):
            valid_count += 1
    return valid_count

print(is_valid(111111))
print(is_valid(223450))
print(is_valid(123789))
print(count_passwords(136760, 595730))