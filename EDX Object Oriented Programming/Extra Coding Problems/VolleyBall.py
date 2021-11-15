#In volleyball, the first team to score 25 points wins.
#However, they must win by 2. So, if the score is 25-24,
#they keep playing until someone is ahead by 2 points.
#
#Write a function called check_volleyball_winner. This
#function will take as input a 2-tuple of two integers: the
#first integer is Team 1's score, and the second integer
#is Team 2's score. check_volleyball_winner should return a
#string:
#
# - If Team 1 has won, return "Team 1 wins!"
# - If Team 2 has won, return "Team 2 wins!"
# - If neither player has won, return "Keep playing!"
#
#For example:
# check_volleyball_winner((23, 17)) -> "Keep playing!"
# check_volleyball_winner((25, 17)) -> "Team 1 wins!"
# check_volleyball_winner((23, 25)) -> "Team 2 wins!"
# check_volleyball_winner((25, 24)) -> "Keep playing!"
# check_volleyball_winner((29, 29)) -> "Keep playing!"
# check_volleyball_winner((29, 30)) -> "Keep playing!"
# check_volleyball_winner((29, 31)) -> "Team 2 wins!"
#
#Remember, the function should RETURN these strings, not
#print them.


#Write your function here!
def check_volleyball_winner(tuple_int):
    team_1 = (tuple_int[0], "Team 1 wins!")
    team_2 = (tuple_int[1], "Team 2 wins!")
    difference = abs(team_1[0]-team_2[0])
    leading = max(team_1,team_2)
    if (team_1[0] >= 25 or team_2[0] >= 25) and difference >= 2:
        return leading[1]
    else:
        return "Keep playing!"
#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print the same output as the examples above.
print(check_volleyball_winner((23, 17)))
print(check_volleyball_winner((25, 17)))
print(check_volleyball_winner((23, 25)))
print(check_volleyball_winner((25, 24)))
print(check_volleyball_winner((29, 29)))
print(check_volleyball_winner((29, 30)))
print(check_volleyball_winner((29, 31)))


