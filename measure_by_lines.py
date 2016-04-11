import os, json, plotly, sys
from subprocess import Popen, PIPE
from plotly.graph_objs import Scatter, Layout

Xaxis = []
Yaxis = []

compiler_name = raw_input("compiler name (clang or gcc): ");
optimisation = raw_input("optimisation (-O1, -O2, -O3, -Os or empty): ");
to_be_plotted = raw_input("What do you want to plot? (user_time, memory or template instantiations): ");
lowest_number = raw_input("Lowest number of strings: ");
highest_number = raw_input("Highest number of strings: ");
step = raw_input("Step between lowest and highest by: ");
length = raw_input("Length of strings: ");

for i in range( int(lowest_number), int(highest_number)+1, int(step) ):

	os.system("python create_files.py " + str(i) + " " + length);
	print "Done creating generated_" + str(i) + "_lines_" + length + "_chars.cpp";
	
	p = Popen(['./mbuild', 'generated_cpps/generated_' + str(i) + '_lines_' + length + '_chars.cpp', '--', '-I./boost_1_60_0', '-std=c++11'], stdout=PIPE, stderr=PIPE, stdin=PIPE);

	output = p.stdout.read();
	if len(sys.argv) > 1:
		print output;

	data = json.loads( output );
	print "Done generating json for generated_" + str(i) + "_lines_" + length + "_chars.cpp";

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
