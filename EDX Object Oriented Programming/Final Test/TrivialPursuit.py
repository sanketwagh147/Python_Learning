#In the board game Trivial Pursuit, players try to collect
#six pieces: Yellow, Green, Red, Blue, Purple, and Orange.
#The first player to collect all six wins.
#
#Write a function called check_winner. This function will
#take as input a tuple with at least 2 lists, but up to 6.
#Each list will represent one player's current progress
#toward gathering six pieces.
#
#If any player has all 6 pieces, check_winner should return
#the string, "Player X wins!", where X refers to the position
#of the player in the list who has all 6 pieces. For this
#problem, the first player in the list should be called
#Player 1, the second player Player 2, and so on.
#
#If no player has all 6 pieces, check_winner should return
#the string, "Keep playing!"
#
#For example, if these were four possible players:
# winning_player = ["Red", "Orange", "Yellow", "Purple", "Green", "Blue"]
# losing_player_a = []
# losing_player_b = ["Red", "Orange"]
# losing_player_c = ["Yellow", "Purple", "Green", "Blue"]
#
# Then...
#
# check_winner((winning_player, losing_player_a, losing_player_b)) -> "Player 1 wins!"
# check_winner((losing_player_a, losing_player_b, losing_player_c)) -> "Keep playing!"
# check_winner((losing_player_b, losing_player_c, winning_player)) -> "Player 3 wins!"
#
#Remember, the function should RETURN these strings, not
#print them. You may assume that only one player will have
#all six pieces.
#
#You may assume we will never use an invalid piece name,
#duplicate pieces, etc.; in other words, if a player has
#six items in their list, you may assume they have won.
#You don't need to check what the pieces actually are.
#
#HINT: Make sure to read those last instructions on
#lines 35-38: they make this problem _much_ eacher.


#Write your function here!
def check_winner(a_tuple_of_list):
    # playing_list
    for i in range(0, len(a_tuple_of_list)):
        if len(a_tuple_of_list[i]) == 6:
            return "Player {} wins!".format(i+1)
    return "Keep playing!"

    


#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print the same output as the examples above.
winning_player = ["Red", "Orange", "Yellow", "Purple", "Green", "Blue"]
losing_player_a = []
losing_player_b = ["Red", "Orange"]
losing_player_c = ["Yellow", "Purple", "Green", "Blue"]

print(check_winner((winning_player, losing_player_a, losing_player_b)))
print(check_winner((losing_player_a, losing_player_b, losing_player_c)))
print(check_winner((losing_player_b, losing_player_c, winning_player)))


