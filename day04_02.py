#!/usr/bin/env python3

def is_valid(pw):
    pw = str(pw)
    d1 = pw[0]
    invalid_repeat = None
    locked_in_repeat = False
    found_repeat = False
    for d2 in pw[1:]:
        if d2 < d1:
            return False
        elif not found_repeat and d2 == d1 and d2 != invalid_repeat:
            found_repeat = True
        elif found_repeat and not locked_in_repeat and d2 == d1:
            found_repeat = False
            invalid_repeat = d2
        elif found_repeat and d1 != d2:
            locked_in_repeat = True
        d1 = d2
    if found_repeat:
        print(pw)
    return found_repeat

def count_passwords(low, high):
    valid_count = 0
    for pw in range(low, high + 1):
        if is_valid(pw):
            valid_count += 1
    return valid_count

print(is_valid(112233))
print(is_valid(123444))
print(is_valid(111122))
print(count_passwords(136760, 595730))