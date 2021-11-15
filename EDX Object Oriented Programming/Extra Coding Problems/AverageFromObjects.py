#Imagine you're writing a program to calculate the class
#average from a gradebook. The gradebook is a list of
#instances of the Student object.
#
#You don't know everything that's inside the Student object,
#but you know that it has a method called get_grade().
#get_grade() will return the average for the student
#represented by a given instance of Student.
#
#You don't know if get_grade() is stored in memory or if
#it's calculated when it's needed, but you don't need to.
#All you need to know is that the class Student has a method
#get_grade() that returns an integer representing the
#student's numeric grade.
#
#Write a function called class_average. class_average()
#should take as input a list of instances of Student, and it
#should return as output the average grade of those
#students, as calculated via their get_grade() method.
#Remember, average is the sum of all their individual
#grades, divided by the number of students.
#
#Hint: You do NOT need to write the Student class to
#complete this problem. You may if you want to in order to
#run and test your code, but when you submit your code for
#grading, we will test it with our Student class. Don't let
#this throw you off: throughout this course, you've been
#using lots of classes without knowing how they work: you
#don't know how the String class works, but you know what
#its upper() method does. You do not need to know how the
#Student class works to use its get_grade() method.


#Write your function here!
def class_average(instance_list):
    total_avg = 0
    for each_instance in instance_list:
        individual_grade = each_instance.get_grade()
        total_avg += individual_grade
    return total_avg/len(instance_list)


#If you want to write a Student class to test your code,
#you could below, and then add your own test cases below
#that. The only requirement you would need to meet is that
#your Student class would need to have a get_grade()
#method that returns an integer (in addition to any other
#usual requirements for classes).



