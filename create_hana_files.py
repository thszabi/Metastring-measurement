#This script creates a file with arg[1] number of lines in it. Each line creates a compile-time string. Each string has arg[2] number of characters in it.
#-128 - 127
import os, sys
from random import randint



if not os.path.exists("generated_cpps"):
	os.makedirs("generated_cpps");

fo = open("generated_cpps/generated_hana_" + sys.argv[1] + "_lines_" + sys.argv[2] + "_chars.cpp", "w")

fo.write("#include \"../include/toUpperChar_hana.hpp\"\n");
fo.write("int main()\n");
fo.write("{\n");

for i in range(0, int(sys.argv[1])):
	fo.write("\ttoUpper< boost::hana::string<");
	if int(sys.argv[2]) > 0:
		fo.write(str(randint(-128, 127)));
	
	for j in range(1, int(sys.argv[2])):
		fo.write(", " + str(randint(-128, 127)));

	fo.write("> >::type variable" + str(i) + ";\n");

fo.write("\treturn 0;\n");
fo.write("}");
fo.close()
