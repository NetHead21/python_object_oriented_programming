import json
from contact import Contact
from contact_encoder import ContactEncoder
from decode_contact import decode_contact 
from pprint import pprint


c = Contact("Juniven", "Saavedra")
text = json.dumps(c, cls=ContactEncoder)
pprint(text)


some_text = (
    '{"__class__": "Contact", "first": "Milli", "last": "Dale", '
    '"full_name": "Milli Dale"}'
)

c2 = json.loads(some_text, object_hook=decode_contact)
print(c2.full_name)
