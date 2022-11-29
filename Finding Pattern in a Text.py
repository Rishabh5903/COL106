import random
import math
import string
#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
	return int(2*math.log(26,2)*m*(math.log(m*math.log(26,2)/eps))/eps) 


# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
	ans=[] #final output list
	m=len(p) #length of p
	n=len(x) #length of p
	prev=1 #initialisation of a varibale which stores the value of remainder by q of subsequent powers of 26 starting from 0 to m-1 
	fpmodq=(string.ascii_uppercase.index(p[-1]))%q #initialisation of a varaible to the value of (26^0*last character of string p)modq which gets updated by adding the remainders of 26^k by q for k in range 0 to m-1 and finally gets the value of f(p)modq in reverse order
	for i in range(2,m+1): 
		fpmodq+=(prev*26*string.ascii_uppercase.index(p[-i]))%q #updating the prev variable and multiplying with the elements of string p then taking modq
		prev=(26*prev)%q #updating prev by next power of 26
	fpmodq=fpmodq%q #taking modq again in case fpmodq obtained above gets > q
	prev=1 #again setting prev=1 to be used later
	fxmodq=(string.ascii_uppercase.index(x[m-1]))%q # doing similar thing as fpmodq to find substring value of x named as fxmodq
	for i in range(1,m): #loop working similar as fpmodq
		fxmodq+=(prev*26*string.ascii_uppercase.index(x[m-1-i]))%q
		prev=(26*prev)%q
	rem=fxmodq #taking another variable rem which stores the sum of indivual remainder of 26^k*x[i] by q to be used later in case this sum is greater than q, because fxmodq will be again taken % with q in next line so the sum of remainders will not be available if this rem was not defined
	fxmodq=fxmodq%q 
	if fxmodq==fpmodq: #checking if initial subtring of x of length m matches with p or not, if yes then appending 0th index in the ans list
		ans.append(0)
	prev2=(prev*string.ascii_uppercase.index(x[0]))%q #another varibale which stores the value of 26^(m-1)*(first letter of subtring in x)%q to be used later which is updated in every substring, prev already has the value of 26^(m-1) modq after above loop
	for i in range(m,n): #loop for traversing in the string x and checking for match with fpmodq
		rem-=prev2 #when moved to next subtring then subtracting the value prev2 from previous rem since it is no longer the part of new subtring 
		rem=(26*rem)%q #updating the rem since shifting to next subtring increases the power of 26 in each single element of subtring as compared to previous iteration
		rem+=string.ascii_uppercase.index(x[i])%q  #adding the value of character next to the last character of previous subtring since it has 26^0 coeff so directly added value
		fxmodq=rem%q #again taking remainder in case rem becomes >q
		if fxmodq==fpmodq: #comparing values of substrings and p
			ans.append(i-m+1) #appending proper index of x in the ans list
		prev2=(prev*string.ascii_uppercase.index(x[i-m+1]))%q #updating prev2 with the value of first element of new substring using prev which has value (26^(m-1)) modq
	return(ans)
def modPatternMatchWildcard(q,p,x): #function to return pattern matching in case of wildcard element ?
	ans=[] #output list
	ind=0 #another variable to store the value of index(taking from last element of string) of the wildcard character ?
	m=len(p) 
	n=len(x)
	prev=1 #same working as above function
	fpmodq=0 #same use as above function
	wildcard_mul=1 #a variable to store the value of 26^k mod q of the wildcard character '?' to be used later
	wildcard_mul_2=1 #a variable to store the value of 26^(k-1) mod q of the wildcard character '?' to be used later
	for i in range(1,m+1): #loop traversing in reverse order in p
		if i<=m-1: #to avoid list index out of range in next step
			if p[-1]!='?' and p[-i-1]=='?': # storing the value of (power of 26 of the next chacter to ? in p)modq when the last character is not ?(because then it has no next character in p)
				wildcard_mul_2=prev 
		if p[-i]!='?': #when the character is not '?' then adding indivual remainders of characters*prev by q in fpmodq
			fpmodq+=(prev*string.ascii_uppercase.index(p[-i]))%q
		else:
			ind=i #assigning tthe index of ? to ind 
			wildcard_mul=prev #assigning the value of wildcard_mul as the (power of 26 at position of ?)mod q
		prev=(26*prev)%q #updating prev similar to above function
	fpmodq=fpmodq%q 
	prev=1 # resetting prev to be used later
	fxmodq=0 # same use as above function
	val1=0 # new variable to store the value of 26^k*(character present at the place of ? in substring of x as compared to p)modq to be used later which gets updated in each substring
	val2=0 # new variable to store the value of 26^(k-1)*(next character of character present at the place of ? in substring of x as compared to p)modq to be used later which gets updated in each substring
	for i in range(m): #iterating in first subtring of x of length m in reverse order
		if i!=ind-1: #if the character is not at the place of ? as compared to p then updating fxmodq
			fxmodq+=(prev*string.ascii_uppercase.index(x[m-1-i]))%q
		else: #wehn we reache the index of ? in subtring
			if i!=m-1: #if ? is not the first character of subtring
				val1=(wildcard_mul*string.ascii_uppercase.index(x[m-1-i]))%q # assigning the value of val1 using the wildcard_mul defined earlier
			elif i==m-1:
				val1=-1 #setting val1 as -1 when ? is the first character since this case needs to be addressed separately
			if i!=0: #if ? is not the last element of substring
				val2=((wildcard_mul_2)*string.ascii_uppercase.index(x[m-i]))%q #assigning the value of val2
			elif i==0:
				val2=-1
		if i!=m-1: #in the last interation prev need not be updated since it has already got the value of 26^(m-1) modq
			prev=(26*prev)%q #updating prev
	rem=fxmodq #same use as above function
	fxmodq=fxmodq%q
	if fxmodq==fpmodq:
		ans.append(0)
	
	prev2=(prev*string.ascii_uppercase.index(x[0]))%q #same use as above function
	for i in range(m,n): #iterating in x 
		if val1!=-1:
			rem-=prev2 #subtracting prev2 if ? was not the first character of p because in that case prev2 was not counted in rem in previous substring so need not be subtracted here
		if val1!=-1:
			rem+=val1 # adding val1(because it was excluded from rem in repvious iteration) to rem if ? was not the first element of p since it is not more a part of new subtring so need not be added
		if val2!=-1: # if ? is the last element of p then it has no next character so nothing to be done if val2==-1
			rem-=val2 #subtracting the value of val2 from rem because in previous substring it was next to the index of ? in substring as compared to p and in this iteration it comes at the index of of ? so need to be excluded
		rem=(26*rem)%q
		if val2!=-1: # adding the value of last character in new subtring if last character of p was not ? because then the next character of last character of previous subtring will now be at the index of ? so need not be added
			rem+=string.ascii_uppercase.index(x[i])%q  
		if val1!=-1: #updating val1
			val1=(wildcard_mul*string.ascii_uppercase.index(x[i-ind+1]))%q
		if val2!=-1: #updating val2
			val2=((wildcard_mul_2)*string.ascii_uppercase.index(x[i-ind+2]))%q
		fxmodq=rem%q
		if fxmodq==fpmodq: #comapring and appending
			ans.append(i-m+1)
		prev2=(prev*string.ascii_uppercase.index(x[i-m+1]))%q #updating prev
	return(ans) #returning ans list
n = 1000
e = 0.1
wrong_e = 0
for i in range(10):
	c,w =0,0
	for i in range(n):
		if randPatternMatch(e, 'IRIS', 'IAPPLEBOIRISHAIRISBH') == [8,14]:
			c += 1
		else:
			w += 1
	if w/n > e:
		wrong_e += 1
	print (c,w)
	print ('error:', w/n)
# print (c,w)
# print ('error:', w/n)
print (wrong_e)