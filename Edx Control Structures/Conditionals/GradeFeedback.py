grade = 82
curve = 8

#You may modify the lines of code above, but don't move them!
#When you Submit your code, we'll change these lines to
#assign different values to the variables.

#Professor Burdell is grading final exams. Based on the
#class average, he has established a curve, whose value is
#given in the variable curve above.
#
#Then, for each individual student, he wants to send a
#personal message based on their grade. Their grade is the
#sum of the value of grade and the value of curve, but it
#cannot be greater than 100; if the curve takes them above
#100, their grade is 100.
#
#Prof. Burdell then wants to send one of the following
#messages, depending on the student's final grade:
#
# - If the total grade 90 to 100, the message would state:
#   "Congratulations! Your final grade is [their grade], an A."
# - If the total grade is 80 to 89, the message would state:
#   "Good job! Your final grade is [their grade], a B."
# - If the total grade is 70 to 79, the message would state:
#   "Not bad! Your final grade is [their grade], a C."
# - If the total grade is 60 to 69, the message would state:
#   "You passed! Your final grade is [their grade], a D."
# - If the total grade is under 60, the message would state:
#   "It's just one grade. Your final grade is [their grade], an F."
#
#[their grade] should be the result of adding grade and curve,
#but should not be greater than 100.


#Add your code here!
a_number = grade + curve
minimum = 0
maximum = 100
grade_1 = minimum if a_number < minimum else maximum if a_number > maximum else a_number
# print(a)
if 90 <= grade_1 <= 100:
    print(f"Congratulations! Your final grade is {grade_1}, an A.")
elif 80 <= grade_1 <= 89:
    print(f"Good job! Your final grade is {grade_1}, a B.")
elif 70 <= grade_1 <= 79:
    print(f"Not bad! Your final grade is {grade_1}, a C.")
elif 60 <= grade_1 <= 69:
    print(f"You passed! Your final grade is {grade_1}, a D.")
else:
    print(f"It's just one grade. Your final grade is {grade_1}, an F.")

