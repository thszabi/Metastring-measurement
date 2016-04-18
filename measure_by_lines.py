#!/usr/bin/python

import os, json, plotly, sys
from subprocess import Popen, PIPE
from plotly.graph_objs import Scatter, Layout

Xaxis = [];
Yaxes = [];
data  = [];

to_be_plotted = raw_input("What do you want to plot? (user_time, memory or template instantiations): ");
lowest_number = raw_input("Lowest number of strings: ");
highest_number = raw_input("Highest number of strings: ");
step = raw_input("Step between lowest and highest by: ");
length = raw_input("Length of strings: ");

for i in range( int(lowest_number), int(highest_number)+1, int(step) ):

	os.system("python create_files.py " + str(i) + " " + length);
	print "Done creating generated_" + str(i) + "_lines_" + length + "_chars.cpp";
	
	p = Popen(['mbuild', 'generated_cpps/generated_' + str(i) + '_lines_' + length + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++11'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if len(sys.argv) > 1:
		print output;

	new_data = json.loads( output );
	data.append(new_data);
	print "Done generating json for generated_" + str(i) + "_lines_" + length + "_chars.cpp";

	Xaxis.append(i);



for i in range(len(data[0])):
	Yaxis = [];

	for j in range(len(data)):
		if data[j][i]['stderr'] != "":
			print data[j][i];
		else:
			if to_be_plotted != "template instantiations" or 'template instantiations' in elem:
				Yaxis.append(data[j][i][to_be_plotted]);

	plotly.offline.plot({
	"data": [ Scatter(x=Xaxis, y=Yaxis) ],
	"layout": Layout( title=data[0][i]['compiler name'] + " " + data[0][i]['compiler version'] + " " + data[0][i]['optimisation'])
	},
	filename='generated_cpps/output_' + str(i) + '.html');
	#filename='generated_cpps/output_' + data[0][i]['compiler name'] + "_" + data[0][i]['compiler version'] + "_" + data[0][i]['optimisation'] + '.html');
