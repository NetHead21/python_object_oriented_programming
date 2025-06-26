from contact import Contact


def decode_contact(json_object: any) -> any:
    if json_object.get("__class__") == "Contact":
        return Contact(json_object["first"], json_object["last"])
    else:
        return json_object
