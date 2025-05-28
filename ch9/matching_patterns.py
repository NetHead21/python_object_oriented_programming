import re

search_string = "hello world"
pattern = r"hello world"

if match := re.match(pattern, search_string):
    print("regex matches")
    print(match)
