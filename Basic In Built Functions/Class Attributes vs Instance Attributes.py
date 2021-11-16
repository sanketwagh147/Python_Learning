class Partner:
    # This is a class Variable
    # It is shared among all instances
    database = []

    def __init__(self, name, age, likes_me):
        # This are instance Variables
        self.name = name
        self.age = age
        self.likes_me = likes_me
        Partner.database.append(self)


sanket = Partner("suk", 14 , True)
sanket1 = Partner("susk", 14 , True)
sanket2 = Partner("susadk", 4 , True)
sanket4 = Partner("susadk", 24 , False)
sanket4 = Partner("sukanya", 24 , True)

for partner in Partner.database:
    if partner.age >21 and partner.likes_me:
        print(partner.name, str(partner.age)+ " Likes YOU")

print(sanket.age)
