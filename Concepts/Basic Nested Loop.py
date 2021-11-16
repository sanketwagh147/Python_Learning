egg = True
milk = True
butter = True
flour = True

if egg:
    if milk:
        if butter:
            if flour:
                print("pancakes")
            else:
                print("omelette")
        else:
            print("custard")
    else:
        print("poached eggs")
else:
    print("Go to the store!")
