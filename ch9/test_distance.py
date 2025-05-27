from distance import distance

annapolis = (38.9784, 76.4922)
saint_michaels = (38.7854, 76.2233)
oxford = (38.6865, 76.1716)
cambridge = (38.5632, 76.0788)
print(round(distance(*annapolis, *saint_michaels), 9))

legs = [
    ("to st.michaels", annapolis, saint_michaels),
    ("to oxford", saint_michaels, oxford),
    ("to cambridge", oxford, cambridge),
    ("return", cambridge, annapolis),
]

speed = 5
fuel_per_hour = 2.2

for name, start, end in legs:
    d = distance(*start, *end)
    print(name, d, d / speed, d / speed * fuel_per_hour)
