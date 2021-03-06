#In the game Rock-Paper-Scissors, two opponents
#simultaneously choose to throw either "Rock", "Paper",
#or "Scissors". Rock beats Scissors, Scissors beats Paper,
#and Paper beats Rock. If both players throw the same
#object, the round is a tie.
#
#Write a function called find_winner. find_winner will take
#as input a list of 2-tuples, each representing a round of
#Rock-Paper-Scissors. Each 2-tuple will contain two strings.
#Each string will be either "Rock", "Paper", or "Scissors".
#The first item in the 2-tuple will represent what Player 1
#chooses in each round, and the second item in the 2-tuple
#will represent what Player 2 chooses in each round.
#
#find_winner should return the string "Player 1 wins!" if
#Player 1 wins more games than Player 2. It should return the
#string "Player 2 wins!" if Player 2 wins more games than
#Player 1. It should return the string "It's a tie!" if the
#two players win an equal number of times.
#
#The number of times the two players tie is irrelevant to the
#result: all that matters is who wins more rounds than the
#other.
#
#For example:
#
# find_winner([("Rock", "Rock"), ("Rock", "Scissors"),
#              ("Paper", "Rock"), ("Scissors", "Rock")])
#
#...would return "Player 1 wins!" because Player 1 wins
#two round and Player 2 wins one round.


#Write your function here!
def find_winner(a_list_of_2_tuples):
    count_1 = 0
    count_2 = 0
    for each_tuple in a_list_of_2_tuples:
        # print(each_tuple)
        if each_tuple[0] == each_tuple[1]:
            # print("Tie Works")
            pass
        if each_tuple[0] == "Rock":
            if each_tuple[1] == "Scissors":
                # print("P1 1")
                count_1 +=1
            if each_tuple[1] == "Paper":
                # print("P2 1")
                count_2 +=1
        if each_tuple[0] == "Scissors":
            if each_tuple[1] == "Rock":
                # print("P2 2")
                count_2 +=1
            if each_tuple[1] == "Paper":
                # print("P1 2")
                count_1 +=1
        if each_tuple[0] == "Paper":
            if each_tuple[1] == "Rock":
                # print("P1 3")
                count_1 +=1
            if each_tuple[1] == "Scissors":
                # print("P2 3")
                count_2 +=1
    # print(count_1)
    # print(count_2)
    if count_2 > count_1:
        return "Player 2 wins!"
    elif count_1 > count_2:
        return "Player 1 wins!"
    else:
        return "It's a tie!"




#Below are some lines of code that will test your function.
#You can change the value of the variable(s) to test your
#function with different inputs.
#
#If your function works correctly, this will originally
#print:
#Player 1 wins!
#Player 2 wins!
#It's a tie!
p1_wins = [("Rock", "Rock"), ("Rock", "Scissors"), ("Paper", "Rock"), ("Scissors", "Rock")]
p2_wins = [("Paper", "Rock"), ("Paper", "Paper"), ("Paper", "Scissors"), ("Rock", "Paper")]
itsatie = [("Paper", "Paper"), ("Paper", "Rock"), ("Rock", "Paper"), ("Scissors", "Scissors")]
# print(find_winner(p1_wins))
# print(find_winner(p2_wins))
# print(find_winner(itsatie))
s = [('Scissors', 'Paper'), ('Paper', 'Paper'), ('Scissors', 'Rock'), ('Scissors', 'Scissors'), ('Paper', 'Paper'), ('Rock', 'Scissors'), ('Paper', 'Scissors')]
print(find_winner(s))
