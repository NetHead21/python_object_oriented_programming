name = "Bob"
activity = "reviewing"
message = f"Hello {name}, you are currently {activity}."
print(message)

emails = ("bob@example.com", "john@example.com")
message = {
    "subject": "Next Chapter",
    "message": "Here's the next chapter to review!",
}

formatted = f"""
From: <{emails[0]}>
To: <{emails[1]}>
Subject: {message["subject"]}

{message["message"]}
"""
print(formatted)

print(f"{[2*a+1 for a in range(5)]}")

for n in range(1, 20):
    print(f"{'fizz' if n % 3 == 0 else n}")
