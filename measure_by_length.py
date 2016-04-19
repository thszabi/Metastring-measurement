#!/usr/bin/python

import os, json, plotly, argparse
from subprocess import Popen, PIPE
from plotly.graph_objs import Scatter, Layout

Xaxis = [];
Yaxes = [];
data  = [];

parser = argparse.ArgumentParser(description='Measures runtime and memory usage with increasing string length');
parser.add_argument(
	'--plot',
	required=True,
	help='What to plot. It can be \'user_time\', \'memory\' or \'template instantiations\''
);

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

args = parser.parse_args();

for i in range(0, args.length+1):

	os.system("python create_files.py " + str(args.lines) + " " + str(i));
	print "Done creating generated_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";
	
	p = Popen(['mbuild', 'generated_cpps/generated_' + str(args.lines) + '_lines_' + str(i) + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++11'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if args.debug:
		print output;

	new_data = json.loads( output );
	data.append(new_data);
	print "Done generating json for generated_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";

	Xaxis.append(i);



for i in range(len(data[0])):
	Yaxis = [];

	for j in range(len(data)):
		if data[j][i]['stderr'] != "":
			print data[j][i];
		else:
			if args.plot != "template instantiations" or 'template instantiations' in data[j][i]:
				Yaxis.append(data[j][i][args.plot]);

	plotly.offline.plot({
	"data": [ Scatter(x=Xaxis, y=Yaxis) ],
	"layout": Layout( title=data[0][i]['compiler name'] + " " + data[0][i]['compiler version'] + " " + data[0][i]['optimisation'])
	},
	filename='generated_cpps/output_' + str(i) + '.html');
	#filename='generated_cpps/output_' + data[0][i]['compiler name'] + "_" + data[0][i]['compiler version'] + "_" + data[0][i]['optimisation'] + '.html');
