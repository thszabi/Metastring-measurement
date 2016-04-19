#This script creates a file with arg[1] number of lines in it. Each line creates a compile-time string. Each string has arg[2] number of characters in it.
#-128 - 127
import os, sys
from random import randint

#This method increases the given array's given index, considering the remainder.
# [0,0,0]   -> [0,0,1]
# [0,0,127] -> [0,1,-128]
def updateNumber(number):

	number = number + 1;

	if number >= 128:
		number = -128;

	return number;



if not os.path.exists("generated_cpps"):
	os.makedirs("generated_cpps");

fo = open("generated_cpps/generated_" + sys.argv[1] + "_lines_" + sys.argv[2] + "_chars.cpp", "w")

fo.write("#include \"../include/toUpperChar.hpp\"\n");
fo.write("int main()\n");
fo.write("{\n");

#This array systematically stores the characters given to the strings. It starts with [-128, -127, -126] (if length==3), and its last index will be increased every time.
#The length of 'numbers' array is the number of character within the strings.
#number = -128

#A line consists of: "toUpper< string<" ++ length * character ++ "> > variableX" (where X is a number)
for i in range(0, int(sys.argv[1])):
	fo.write("\ttoUpper< string<");
	fo.write(str(randint(-128, 127)));
	#number = updateNumber(number);
	
	for j in range(1, int(sys.argv[2])):
		fo.write(", " + str(randint(-128, 127)));
		#number = updateNumber(number);

	fo.write("> >::type variable" + str(i) + ";\n");

fo.write("\treturn 0;\n");
fo.write("}");
fo.close()
