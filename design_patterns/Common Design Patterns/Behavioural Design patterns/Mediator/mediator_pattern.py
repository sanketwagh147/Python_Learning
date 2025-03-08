"""
Implementation of mediator pattern in a chat room
"""


class Person:
    def __init__(self, name) -> None:
        self.name = name
        self.chat_log = []
        self.room: ChatRoom | None = None

    def receive(self, sender, msg):
        s = f"{sender}: {msg}"
        print(f"{self.name} chat session {s}")
        self.chat_log.append(s)

    def say(self, msg):
        if self.room:
            self.room.broadcast(self.name, msg)

    def private_message(self, who, message):
        if self.room:
            self.room.message(self.name, who, message)


class ChatRoom:
    """
    This is a central mediator which allows to communicate with each another
    """

    def __init__(self) -> None:
        self.people: list[Person] = []

    def join(self, person: Person):
        join_msg = f"{person.name} joined the chat"
        self.broadcast("room", join_msg)
        person.room = self
        self.people.append(person)

    def broadcast(self, source, msg):
        for p in self.people:
            if p.name != source:
                p.receive(source, msg)

    def message(self, source, destination, message):
        for p in self.people:
            if p.name == destination:
                p.receive(source, message)


if __name__ == "__main__":
    room = ChatRoom()
    sanket = Person("Sanket")
    sukanya = Person("Sukanya")
    room.join(sanket)
    room.join(sukanya)
    sanket.say("Hi room")
    sukanya.say("Hi snake")

    rahul = Person("rahul")
    room.join(rahul)
    rahul.say("Hi all")

    sukanya.private_message("rahul", "happy to see you here")
