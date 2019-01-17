import sys


def isNumber(str):
	numbers = ['0','1','2','3','4','5','6','7','8','9']
	for letter in str:
		if letter not in numbers:
			return False	
	return True


#Process the production rule F -> any# | (E) 
def f(linearray,count):
	if isNumber(linearray[count]):
		count=count+1
	elif linearray[count]=="(":
		count=count+1
		e(linearray,count)
		if linearray[count]!=")":
			print "MISSING PAREN, Position: %d, Line: %s" % (count, linearray)
			sys.exit()
		count=count+1
	else:
		print "SYNTAX ERROR, Position: %d, Line: %s" % (count, linearray)
		sys.exit()


# Process the production rule T -> F * T | F / T | T
def t(linearray,count):
	f(linearray,count)
	if linearray[count] == "*" or linearray[count] == "/":
		count=count+1
		t(linearray,count)

# Process the production rule E -> T + E | T - E | T
def e(linearray, count):
	t(linearray,count)
	if linearray[count] == "+" or linearray[count] == "-":
		count=count+1
		e(linearray,count)

def main():

	filename = sys.argv[1]
	file = open(filename)
	filedata = file.read()
	lines = filedata.split("\n")	
	for line in lines:
		count = 0
		linearray = line.split(" ")
		e(linearray,count)

	print "Parsing complete!"



main()

