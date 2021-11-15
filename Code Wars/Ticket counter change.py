def tickets(people):
    balance = 0
    ticket_price = 25
    a_dict = {"100":0, "50":0, "25":0, }

    for i in people:
        a_dict[str(i)] += 1
        change = i - ticket_price
        balance += ticket_price
        if balance >= change and change != 0:
            if change == 25:
                if a_dict["25"] >= 1:
                    a_dict["25"] -= 1
                else:
                    return "NO"
            elif change == 50:
                if a_dict["25"] >= 2:
                    a_dict["25"] -= 2
                elif a_dict["50"] >= 1:
                    a_dict["50"] -= 1
                else:
                    return "NO"
            elif change == 75:
                if  a_dict["25"] >= 3:
                    a_dict["25"] -= 3
                elif a_dict["25"]>= 1 and a_dict["50"]>=1:
                    a_dict["25"]-= 1
                    a_dict["50"]-=1
                else:
                    return "NO"

    return "YES"
print(tickets([25, 25, 50])) # => YES
# tickets([25, 100]) # => NO. Vasya will not have enough money to give change to 100 dollars
# tickets([25, 25, 50, 50, 100]) #


# BEst solution
def tickets(a):
    n25 = n50 = n100 = 0
    for e in a:
        if   e==25            : n25+=1
        elif e==50            : n25-=1; n50+=1
        elif e==100 and n50>0 : n25-=1; n50-=1
        elif e==100 and n50==0: n25-=3
        if n25<0 or n50<0:
            return 'NO'
    return 'YES'
