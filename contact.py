from typing import Protocol


class ContactList(list):
    def search(self, name: str) -> list["Contact"]:
        """
        Search for contacts by name.
        :param name: Name to search for
        :return: List of matching contacts
        """
        matching_contacts: list["Contact"] = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts


class Contact:
    all_contacts = ContactList()

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        Contact.all_contacts.append(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self.email!r})"


class Suppliers(Contact):
    def order(self, order: "Order") -> None:
        print(
            "If this where a real system we sould send "
            f"'{order}' order to '{self.name}'"
        )


class Friend(Contact):
    def __init__(self, name: str, email: str, phone: str) -> None:
        super().__init__(name, email)
        self.phone = phone


class Emailable(Protocol):
    email: str


class MailSender(Emailable):
    def send_email(self, message: str) -> None:
        print(f"Sending mail to {self.email=}")


class EmailableContact(Contact, MailSender):
    pass
