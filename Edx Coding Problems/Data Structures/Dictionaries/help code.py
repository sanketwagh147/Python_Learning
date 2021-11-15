original_pin = 1122

count=0

while count < 3:
    try:

        secret_pin = (input('Enter Your Pin: '))
    except ValueError:
        print("Enter Digits only")

    finally:
        if secret_pin == str(original_pin):

            print('DOOR UNLOCKED!!')
            break

        else:
            print('WRONG PIN!! (TRY AGAIN!)')
            count += 1
