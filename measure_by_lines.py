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
data  = [];

parser = argparse.ArgumentParser(description='Measures runtime and memory usage with increasing number of lines');

parser.add_argument(
	'--lowest',
	type=int,
	required=True,
	help='The lowest number of lines.'
);

parser.add_argument(
	'--highest',
	type=int,
	required=True,
	help='The highest number of lines.'
);

parser.add_argument(
	'--step',
	type=int,
	required=True,
	help='Step between lowest and highest.'
);

parser.add_argument(
	'--length',
	type=int,
	required=True,
	help='Length of strings.'
);

parser.add_argument(
	'--debug',
	action='store_true',
	required=False,
	help='If used, the generated json will be displayed'
);

args = parser.parse_args();

for i in range( args.lowest, args.highest+1, args.step ):

	os.system("python create_files.py " + str(i) + " " + str(args.length));
	print "Done creating generated_" + str(i) + "_lines_" + str(args.length) + "_chars.cpp";
	
	p = Popen(['mbuild', 'generated_cpps/generated_' + str(i) + '_lines_' + str(args.length) + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++11'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if args.debug:
		print output;

	new_data = json.loads( output );
	data.append(new_data);
	print "Done generating json for generated_" + str(i) + "_lines_" + str(args.length) + "_chars.cpp";

	Xaxis.append(i);



for i in range(len(data[0])):
	Yaxis_user_time = [];
	Yaxis_memory = [];
	Yaxis_instantiations = [];

	for j in range(len(data)):
		if data[j][i]['compiles']:
			Yaxis_user_time.append(data[j][i]['user_time']);
			Yaxis_memory.append(data[j][i]['memory']);
			if 'template instantiations' in data[j][i]:			
				Yaxis_instantiations.append(data[j][i]['template instantiations']);
		else:
			print data[j][i];

	if data[0][i]['compiles']:
		data[0][i]['compiler version'] = remove_bad_characters(data[0][i]['compiler version']);
		if data[0][i]['optimisation'] == "":
			data[0][i]['optimisation'] = "no optimisation";
		path = 'plots/' + data[0][i]['compiler name'] + "/" + data[0][i]['compiler version'] + "/" + data[0][i]['optimisation'];

		if not os.path.exists(path + "/"):
			os.makedirs(path + "/");

		plotly.offline.plot({
		"data": [ Scatter(x=Xaxis, y=Yaxis_user_time) ],
		"layout": Layout( title=data[0][i]['compiler name'] + " " + data[0][i]['compiler version'] + " " + data[0][i]['optimisation'])
		},
		filename=path + '/user_time.html');

		plotly.offline.plot({
		"data": [ Scatter(x=Xaxis, y=Yaxis_memory) ],
		"layout": Layout( title=data[0][i]['compiler name'] + " " + data[0][i]['compiler version'] + " " + data[0][i]['optimisation'])
		},
		filename=path + '/memory.html');

		if 'template instantiations' in data[0][i]:
			plotly.offline.plot({
			"data": [ Scatter(x=Xaxis, y=Yaxis_instantiations) ],
			"layout": Layout( title=data[0][i]['compiler name'] + " " + data[0][i]['compiler version'] + " " + data[0][i]['optimisation'])
			},
			filename=path + '/template_instantiations.html');
