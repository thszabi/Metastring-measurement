#This script creates a file with arg[1] number of lines in it. Each line creates a compile-time string. Each string has arg[2] number of characters in it.
#-128 - 127
import os, sys
from random import randint

if int(sys.argv[1]) < 4:
	for i in range(0, int(sys.argv[1])):
		sys.stdout.write("\ttoUpper< string<");
		
		if int(sys.argv[2]) > 0:
			sys.stdout.write( str(randint(-128, 127)) );
	
		if int(sys.argv[2]) < 4:
			for j in range(1, int(sys.argv[2])):
				sys.stdout.write(", " + str(randint(-128, 127)));
		else:
			sys.stdout.write(", " + str(randint(-128, 127)));
			sys.stdout.write(", ..., " + str(randint(-128, 127)));
		
		sys.stdout.write("> >::type variable" + str(i) + ";\n");

else:
	for i in range(0, 2):
		sys.stdout.write("\ttoUpper< string<");
		if int(sys.argv[2]) > 0:
			sys.stdout.write(str(randint(-128, 127)));
	
		if int(sys.argv[2]) < 4:
			for j in range(1, int(sys.argv[2])):
				sys.stdout.write(", " + str(randint(-128, 127)));
		else:
			for j in range(0, 2):
				sys.stdout.write(", " + str(randint(-128, 127)));
			sys.stdout.write(", ..., " + str(randint(-128, 127)));

		sys.stdout.write("> >::type variable" + str(i) + ";\n");

	sys.stdout.write("\t...\n");

	sys.stdout.write("\ttoUpper< string<");
	if int(sys.argv[2]) > 0:
		sys.stdout.write(str(randint(-128, 127)));

	if int(sys.argv[2]) < 4:
		for j in range(1, int(sys.argv[2])):
			sys.stdout.write(", " + str(randint(-128, 127)));
	else:
		sys.stdout.write(", " + str(randint(-128, 127)));
		sys.stdout.write(", ..., " + str(randint(-128, 127)));

	sys.stdout.write("> >::type variable" + str(int(sys.argv[1])-1) + ";\n");
