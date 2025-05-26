s = "hello world"
print(s.count("l"))
print(s.find("l"))
# print(s.rindex("m"))

s2 = "hello world, how are you?"
s3 = s2.split()
print(f"{s3=}")

print("#".join(s3))
s2.replace(" ", "**")
print(f"{s2=}")
print(s2.partition(" "))
