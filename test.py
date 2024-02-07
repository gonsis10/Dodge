import random


# def random_of_ranges(*ranges):
#     all_ranges = sum(ranges, [])
#     return random.choice(all_ranges)


# a = list(range(1, 10)) + list(range(15, 25))
# print(random.choice(a))

a = random.choice([random.choice([1, 2, 3]), random.choice([4, 5, 6])])
print(a)

side = random.choice([0, 1])
pos_out = random.choice([random.choice([1, 2, 3]), random.choice([4, 5, 6])])
pos_in = random.randint(0, 800)
if side == 0:
    x = pos_out
    y = pos_in
else:
    y = pos_out
    x = pos_in
