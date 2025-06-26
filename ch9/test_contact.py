import json
from contact import Contact
from contact_encoder import ContactEncoder
from pprint import pprint


c = Contact("Juniven", "Saavedra")
text = json.dumps(c, cls=ContactEncoder)
pprint(text)
