class Person:
    kanda = "lasun"
    def __init__(self,):
        self.firstname = ""

        self.lastname = ""

    def get_name(self,extra_info):
        return self.firstname+" " + self.lastname + " " + extra_info
class Person2:
    def __init__(self, extra_info="na"):
        self.firstname = ""
        self.extra_info = extra_info
        self.lastname = ""

    def get_name(self,extra_info):
        return extra_info +" "+ self.firstname+" " + self.lastname + " " + extra_info

sanket = Person2()  # Define instance sanket
sanket.firstname = "Sanket"
sanket.lastname = "Wagh"
print(sanket.get_name( "bp"))

sukanya =Person2(extra_info="oskllls")
print(sukanya.extra_info)
