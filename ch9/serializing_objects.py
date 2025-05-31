import pickle
from pprint import pprint

some_data = ["a list", "containing", 5, "items", {"including": ["str", "int", "dict"]}]

with open("pickled_list", "wb") as file:
    pickle.dump(some_data, file)

with open("pickled_list", "rb") as file:
    loaded_data = pickle.load(file)


pprint(loaded_data)


assert loaded_data == some_data
