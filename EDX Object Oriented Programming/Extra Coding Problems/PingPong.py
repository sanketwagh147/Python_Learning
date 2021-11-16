#In ping-pong (table tennis), the first person to score 21
#points wins. However, they must win by 2. So, if the score
#is 21-20, they keep playing until someone is ahead by 2
#points.
#
#Write a function called check_pingpong_winner. This
#function will take as input a 2-tuple of two integers: the
#first integer is Player 1's score, and the second integer
#is Player 2's score. check_pingpong_winner should return a
#string:
#
# - If Player 1 has won, return "Player 1 wins!"
# - If Player 2 has won, return "Player 2 wins!"
# - If neither player has won, return "Keep playing!"
#
#For example:
# check_pingpong_winner((19, 13)) -> "Keep playing!"
# check_pingpong_winner((21, 13)) -> "Player 1 wins!"
# check_pingpong_winner((19, 21)) -> "Player 2 wins!"
# check_pingpong_winner((21, 20)) -> "Keep playing!"
# check_pingpong_winner((25, 25)) -> "Keep playing!"
# check_pingpong_winner((25, 27)) -> "Player 2 wins!"
#
#Remember, the function should RETURN these strings, not
#print them.


#Write your function here!
def check_pingpong_winner(a_tuple):
    win_score = 21
    difference = abs(a_tuple[1]-a_tuple[0])

    if difference >= 2 and (a_tuple[0]>= 21 or a_tuple[1]>=21):
        if a_tuple[0]>a_tuple[1]:
            return "Player 1 wins!"
        else:
            return "Player 2 wins!"
    else:
        return "Keep playing!"


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print the same output as the examples above.
print(check_pingpong_winner((19, 13)))
print(check_pingpong_winner((21, 13)))
print(check_pingpong_winner((19, 21)))
print(check_pingpong_winner((21, 20)))
print(check_pingpong_winner((25, 25)))
print(check_pingpong_winner((25, 27)))


