
li = []
def permute(s, answer):
	if (len(s) == 0):
		print(answer, end = " ")
		return
	
	for i in range(len(s)):
		ch = s[i]
		left_substr = s[0:i]
		right_substr = s[i + 1:]
		rest = left_substr + right_substr
		li.append(permute(rest, answer + ch))

# Driver Code
answer = ""

s = "\'[]19=p-0;" 

print("All possible strings are : ")
permute(s, answer)

# This code is contributed by Harshit Srivastava
