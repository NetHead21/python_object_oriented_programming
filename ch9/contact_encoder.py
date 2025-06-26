import json
from contact import Contact


class Contactencoder(json.JSONEncoder):
    def default(self, obj: any) -> any:
        if isinstance(obj, Contact):
            return {
                "__class__": "Contact",
                "first": obj.first,
                "last": obj.last,
                "full_name": obj.full_name,
            }
        return super().default(obj)
