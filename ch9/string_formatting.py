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
