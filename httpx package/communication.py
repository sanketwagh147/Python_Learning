

class Communication:
    
    def __init__(self, communication_type:str) -> None:
        self.communication_type = communication_type

    def send(self):
        print("sending Communication")
        

class WhatsappCommunication(Communication):
    def __init__(self, ) -> None:
        super().__init__(communication_type="wa")
    
    def send(self):
        print(f"sending {self.communication_type}")
# c = Communication()
# c.send()
w = WhatsappCommunication()
w.send()