import os, json, plotly, sys
from subprocess import Popen, PIPE
from plotly.graph_objs import Scatter, Layout

Xaxis = []
Yaxis = []

compiler_name = raw_input("compiler name (clang or gcc): ");
optimisation = raw_input("optimisation (-O1, -O2, -O3, -Os or empty): ");
to_be_plotted = raw_input("What do you want to plot? (user_time, memory or template instantiations): ");
lowest_length = raw_input("Lowest length of strings: ");
highest_length = raw_input("Highest length of strings: ");
lines = raw_input("Number of strings per length: ");

for i in range(int(lowest_length), int(highest_length)+1):

	os.system("python create_files.py " + lines + " " + str(i));
	print "Done creating generated_" + lines + "_lines_" + str(i) + "_chars.cpp";
	
	p = Popen(['./mbuild', 'generated_cpps/generated_' + lines + '_lines_' + str(i) + '_chars.cpp', '--', '-I./boost_1_60_0', '-std=c++11'], stdout=PIPE, stderr=PIPE, stdin=PIPE);

	output = p.stdout.read();
	if len(sys.argv) > 1:
		print output;

	data = json.loads( output );
	print "Done generating json for generated_" + lines + "_lines_" + str(i) + "_chars.cpp";

	Xaxis.append(i);

	for elem in data:
		if  elem['stderr'] != "":
			print elem;
		else:
			if elem['compiler name'] == compiler_name and elem['optimisation'] == optimisation:
				if to_be_plotted != "template instantiations" or elem['compiler version'][-9:] == "Templight":
					Yaxis.append(elem[to_be_plotted]);


plotly.offline.plot({
"data": [ Scatter(x=Xaxis, y=Yaxis) ],
"layout": Layout( title="hello world")
},
filename='generated_cpps/output.html');
