#!/usr/bin/python

import os, json, plotly, argparse
from subprocess import Popen, PIPE
from plotly.graph_objs import Scatter, Layout

def remove_bad_characters(text):
	bad_character_index = text.find("/");
	while(bad_character_index >= 0):
		text_list = list(text);
		text_list[bad_character_index] = '\\';
		text = "".join(text_list);
		bad_character_index = text.find("/");
	return text;



Xaxis = [];
data_string     = [];
data_metaparse  = [];
data_hana       = [];

parser = argparse.ArgumentParser(description='Measures runtime and memory usage with increasing string length');

parser.add_argument(
	'--length',
	type=int,
	required=True,
	help='The highest length of strings.'
);

parser.add_argument(
	'--lines',
	type=int,
	required=True,
	help='Number of strings per length.'
);

parser.add_argument(
	'--debug',
	action='store_true',
	required=False,
	help='If used, the generated json will be displayed'
);

parser.add_argument(
	'--tex',
	action='store_true',
	required=False,
	help='If used, a .tex file will be generated containing info about the plots'
);

args = parser.parse_args();

for i in range(0, args.length+1):

	os.system("python create_string_files.py " + str(args.lines) + " " + str(i));
	print "Done creating generated_string_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";
	
	p = Popen(['mbuild', 'generated_cpps/generated_string_' + str(args.lines) + '_lines_' + str(i) + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++11'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if args.debug:
		print output;

	new_data = json.loads( output );
	data_string.append(new_data);
	print "Done generating json for generated_string_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";


	os.system("python create_metaparse_files.py " + str(args.lines) + " " + str(i));
	print "Done creating generated_metaparse_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";
	
	p = Popen(['mbuild', 'generated_cpps/generated_metaparse_' + str(args.lines) + '_lines_' + str(i) + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++11'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if args.debug:
		print output;

	new_data = json.loads( output );
	data_metaparse.append(new_data);
	print "Done generating json for generated_metaparse_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";


	os.system("python create_hana_files.py " + str(args.lines) + " " + str(i));
	print "Done creating generated_hana_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";
	
	p = Popen(['mbuild', 'generated_cpps/generated_hana_' + str(args.lines) + '_lines_' + str(i) + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++14'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if args.debug:
		print output;

	new_data = json.loads( output );
	data_hana.append(new_data);
	print "Done generating json for generated_hana_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";

	Xaxis.append(i);



if args.tex:
	fo = open("plain_explanation.tex", "w");

number_of_compiler_and_version_combinations = len(data_string[0]);
for i in range(number_of_compiler_and_version_combinations):
	Yaxis_string_user_time = [];
	Yaxis_string_memory = [];
	Yaxis_string_instantiations = [];
	Yaxis_metaparse_user_time = [];
	Yaxis_metaparse_memory = [];
	Yaxis_metaparse_instantiations = [];
	Yaxis_hana_user_time = [];
	Yaxis_hana_memory = [];
	Yaxis_hana_instantiations = [];

	for j in range(len(data_string)):
		if data_string[j][i]['compiles']:
			Yaxis_string_user_time.append(data_string[j][i]['user_time']);
			Yaxis_string_memory.append(data_string[j][i]['memory']);
			if 'template instantiations' in data_string[j][i]:
				Yaxis_string_instantiations.append(data_string[j][i]['template instantiations']);
		else:
			Yaxis_string_user_time.append(0);
			Yaxis_string_memory.append(0);
			if 'template instantiations' in data_string[j][i]:
				Yaxis_string_instantiations.append(0);

		if data_metaparse[j][i]['compiles']:
			Yaxis_metaparse_user_time.append(data_metaparse[j][i]['user_time']);
			Yaxis_metaparse_memory.append(data_metaparse[j][i]['memory']);
			if 'template instantiations' in data_metaparse[j][i]:
				Yaxis_metaparse_instantiations.append(data_metaparse[j][i]['template instantiations']);
		else:
			Yaxis_metaparse_user_time.append(0);
			Yaxis_metaparse_memory.append(0);
			if 'template instantiations' in data_metaparse[j][i]:
				Yaxis_metaparse_instantiations.append(0);

		if data_hana[j][i]['compiles']:
			Yaxis_hana_user_time.append(data_hana[j][i]['user_time']);
			Yaxis_hana_memory.append(data_hana[j][i]['memory']);
			if 'template instantiations' in data_hana[j][i]:
				Yaxis_hana_instantiations.append(data_hana[j][i]['template instantiations']);
		else:
			Yaxis_hana_user_time.append(0);
			Yaxis_hana_memory.append(0);
			if 'template instantiations' in data_hana[j][i]:
				Yaxis_hana_instantiations.append(0);



	if data_string[0][i]['compiles']:
		data_string[0][i]['compiler version'] = remove_bad_characters(data_string[0][i]['compiler version']);
		if data_string[0][i]['optimisation'] == "":
			data_string[0][i]['optimisation'] = "no optimisation";
		path = 'plots/' + data_string[0][i]['compiler name'] + "/" + data_string[0][i]['compiler version'] + "/" + data_string[0][i]['optimisation'];

		if not os.path.exists(path + "/"):
			os.makedirs(path + "/");

		plotly.offline.plot({
		"data": [ Scatter(x=Xaxis, y=Yaxis_string_user_time), Scatter(x=Xaxis, y=Yaxis_metaparse_user_time), Scatter(x=Xaxis, y=Yaxis_hana_user_time) ],
		"layout": Layout( title=data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " " + data_string[0][i]['optimisation'])
		},
		filename=path + '/user_time.html');
		if args.tex:
			fo.write(data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " " + data_string[0][i]['optimisation'] + " user_time picture goes here\n");
			fo.write("This test was run with " + data_string[0][i]['compiler name'] + " (version " + data_string[0][i]['compiler version'] + ")");
			if data_string[0][i]['optimisation'] == "no optimisation":
				fo.write(" with no optimisation. ");
			else:
				fo.write(" with " + data_string[0][i]['optimisation'] + "optimisation. ");
			fo.write("The graph shows how much time it took to compile files which contain compile-time strings with a given length. The first test contains strings with 0 characters in it, and the last test contains strings with " + str(args.length) + " characters. Each file contains " + str(args.lines) + " strings. The compiled source files contain the following lines:\n");
			
			fo.write("generated_" + str(args.lines) + "_lines_0_chars.cpp:\n")
			p = Popen(['python', 'create_string_example.py', str(args.lines), str(0)], stdout=PIPE, stderr=None, stdin=PIPE);
			fo.write(p.stdout.read());

			fo.write("generated_" + str(args.lines) + "_lines_" + str(args.length) + "_chars.cpp:\n")
			p = Popen(['python', 'create_string_example.py', str(args.lines), str(args.length)], stdout=PIPE, stderr=None, stdin=PIPE);
			fo.write(p.stdout.read());

			fo.write("The graph shows that...\n");


		plotly.offline.plot({
		"data": [ Scatter(x=Xaxis, y=Yaxis_string_memory), Scatter(x=Xaxis, y=Yaxis_metaparse_memory), Scatter(x=Xaxis, y=Yaxis_hana_memory) ],
		"layout": Layout( title=data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " " + data_string[0][i]['optimisation'])
		},
		filename=path + '/memory.html');
		if args.tex:
			fo.write(data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " " + data_string[0][i]['optimisation'] + " memory picture goes here\n");
			fo.write("This test was run with " + data_string[0][i]['compiler name'] + " (version " + data_string[0][i]['compiler version'] + ")");
			if data_string[0][i]['optimisation'] == "no optimisation":
				fo.write(" with no optimisation. ");
			else:
				fo.write(" with " + data_string[0][i]['optimisation'] + "optimisation. ");
			fo.write("The graph shows how much memory was used during compilation of files which contain compile-time string with a given length. The first test contains strings with 0 characters in it, and the last test contains strings with " + str(args.length) + " characters. Each file contains " + str(args.lines) + " strings. The compiled source file contains the following lines:\n");

			fo.write("generated_" + str(args.lines) + "_lines_0_chars.cpp:\n")
			p = Popen(['python', 'create_string_example.py', str(args.lines), str(0)], stdout=PIPE, stderr=None, stdin=PIPE);
			fo.write(p.stdout.read());

			fo.write("generated_" + str(args.lines) + "_lines_" + str(args.length) + "_chars.cpp:\n")
			p = Popen(['python', 'create_string_example.py', str(args.lines), str(args.length)], stdout=PIPE, stderr=None, stdin=PIPE);
			fo.write(p.stdout.read());

			fo.write("The graph shows that...\n");


		if 'template instantiations' in data_string[0][i]:
			plotly.offline.plot({
		"data": [ Scatter(x=Xaxis, y=Yaxis_string_instantiations), Scatter(x=Xaxis, y=Yaxis_metaparse_instantiations), Scatter(x=Xaxis, y=Yaxis_hana_instantiations) ],
			"layout": Layout( title=data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " " + data_string[0][i]['optimisation'])
			},
			filename=path + '/template_instantiations.html');
			if args.tex:
				fo.write(data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " " + data_string[0][i]['optimisation'] + " template instantiations picture goes here\n");
				fo.write("This test was run with " + data_string[0][i]['compiler name'] + " (version " + data_string[0][i]['compiler version'] + ")");
				if data_string[0][i]['optimisation'] == "no optimisation":
					fo.write(" with no optimisation. ");
				else:
					fo.write(" with " + data_string[0][i]['optimisation'] + "optimisation. ");
				fo.write("The graph shows how much templates were instantiated during compilation of files which contain compile-time string with a given length. The first test contains strings with 0 characters in it, and the last test contains strings with " + str(args.length) + " characters. Each file contains " + str(args.lines) + " strings. The compiled source file contains the following lines:\n");

				fo.write("generated_" + str(args.lines) + "_lines_0_chars.cpp:\n")
				p = Popen(['python', 'create_string_example.py', str(args.lines), str(0)], stdout=PIPE, stderr=None, stdin=PIPE);
				fo.write(p.stdout.read());

				fo.write("generated_" + str(args.lines) + "_lines_" + str(args.length) + "_chars.cpp:\n")
				p = Popen(['python', 'create_string_example.py', str(args.lines), str(args.length)], stdout=PIPE, stderr=None, stdin=PIPE);
				fo.write(p.stdout.read());

				fo.write("The graph shows that...\n");

if args.tex:
	fo.close();
