#!/usr/bin/python

import os, json, plotly, sys
from subprocess import Popen, PIPE
from plotly.graph_objs import Scatter, Layout

Xaxis = [];
Yaxes = [];
data  = [];

to_be_plotted = raw_input("What do you want to plot? (user_time, memory or template instantiations): ");
highest_length = raw_input("Highest length of strings: ");
lines = raw_input("Number of strings per length: ");



for i in range(0, int(highest_length)+1):

	os.system("python create_files.py " + lines + " " + str(i));
	print "Done creating generated_" + lines + "_lines_" + str(i) + "_chars.cpp";
	
	p = Popen(['mbuild', 'generated_cpps/generated_' + lines + '_lines_' + str(i) + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++11'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if len(sys.argv) > 1:
		print output;

	new_data = json.loads( output );
	data.append(new_data);
	print "Done generating json for generated_" + lines + "_lines_" + str(i) + "_chars.cpp";

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
