story = "A"
text = "B"
role = "C"
director = "D"
cast = "F"

#You may modify the lines of code above, but don't move them!
#When you Submit your code, we'll change these lines to
#assign different values to the variables.
#
#In Bryan Cranston's autobiography, he describes how after
#his success on Breaking Bad, he developed a scoring system
#for evaluating new scripts that he received.
#
#First, he would assign the script a grade -- A, B, C, D, or
#F -- in each of five categories: Story, Text, Role, Director,
#and Cast.
#
#Then, he would tally those grades into a total score for the
#script, according to the following chart:
#
#            A   B   C   D   F
# Story     +6  +5  +4  +2  +0
# Text      +5  +4  +3  +1  +0
# Role      +4  +3  +2  +1  +0
# Director  +3  +2  +1  +0  +0
# Cast/Misc +2  +1  +0  +0  +0
#
#For example: an A story, B text, C role, D directory, and
#F cast would get a score of 12: +6 for the story, +4 for the
#text, +2 for the role, +0 for the director, and +0 for the
#cast.
#
#Then, based on that score, the script would be assigned a
#category (note these are slightly different from the image
#because we've excluded the time variable):
#
# 20: Perfect score
# 17 to 19: Must do
# 14 to 16: Seriously consider
# 12 to 13: On the bubble
# 11 or below: Pass
#
#The variables above give the letter grades assigned to each
#of the five components. Write a program that calculates the
#total score he would assign to the script represented by
#these variables. Then on the next line, print the category
#he would assign to that script. For example, for the values
#above, this program would print:
#
#12
#On the bubble
#
#HINT: This is a *long* program. It's not particularly
#complex -- you're doing the same thing over and over, However,
#that 'same thing' required 4-8 lines each time you do it. Our
#answer is 46 lines long! So, don't think you're off-track just
#because you're writing a lot of lines.
# {"None", "A", "B", "C", "D", "F"],
#Add your code here!
check = {"story":story, "text": text, "role":role, "director":director, "cast":cast}
Format = {
           "story"   : {"A": 6, "B": 5, "C": 4, "D": 2, "F": 0},
           "text"    : {"A": 5, "B": 4, "C": 3, "D": 1, "F": 0},
           "role"    : {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0},
           "director": {"A": 3, "B": 2, "C": 1, "D": 0, "F": 0},
           "cast"    : {"A": 2, "B": 1, "C": 4, "D": 0, "F": 0}
          }
score = 0
for each in check.items():
    # print(each)
    a,b = each
    # print(Format[each][each])
    score += Format[a][b]
print(score)
if score == 20:
    print("Perfect score")
elif 17 <= score <=19:
    print('Must do')
elif 14 <= score <=16:
    print('Seriously consider')
elif 12 <= score <=13:
    print('On the bubble')
else:
    print('P    ass')
