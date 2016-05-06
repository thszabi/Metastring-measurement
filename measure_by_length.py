#!/usr/bin/python
# coding=utf-8

import os, json, plotly, argparse, codecs
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


def write_graph_description(path, measure_type, compiler_name, compiler_version, optimisation, length, lines):
	fo = codecs.open(path + "/" + measure_type + ".tex", "w", "utf-8");

	fo.write(u"\\includegraphics{" + measure_type + u"}\n");
	fo.write(u"Ez a mérés a " + compiler_name + u" fordító " + compiler_version + u" verziójával készült, ");
	if optimisation == "no":
		fo.write(u"optimalizáció nélkül. ");
	else:
		fo.write(optimisation  + u" optimalizációval. ");
	if measure_type == "user-time":
		fo.write(u"A fenti diagramon látható, mennyi időt vett igénybe növekvő hosszúságú, fordítás idejű stringeket tartalmazó fájlok fordítása. ");
	if measure_type == "memory":
		fo.write(u"A fenti diagramon látható, mennyi memóriát vett igénybe növekvő hosszúságú, fordítás idejű stringeket tartalmazó fájlok fordítása. ");
	if measure_type == "template-instantiations":
		fo.write(u"A fenti diagramon látható, hány template példányosítás történt növekvő hosszúságú, fordítás idejű stringeket tartalmazó fájlok fordítása során. ");
	fo.write(u"Az első fájl 0 hosszúságú (azaz üres) stringeket tartalmaz, az utolsó pedig " + str(length) + u" karakter hosszú stringeket tartalmaz. Minden egyes fájl " + str(lines) + u" darab stringet hoz létre.\n");
	fo.write(u"Az ábrán látható, hogy...\n\n");
	
	fo.close();

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


	os.system("python create_metaparse_files.py " + str(args.lines) + " " + str(i));
	
	p = Popen(['mbuild', 'generated_cpps/generated_metaparse_' + str(args.lines) + '_lines_' + str(i) + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++11'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if args.debug:
		print output;

	new_data = json.loads( output );
	data_metaparse.append(new_data);


	os.system("python create_hana_files.py " + str(args.lines) + " " + str(i));
	print "Done creating generated_hana_" + str(args.lines) + "_lines_" + str(i) + "_chars.cpp";
	
	p = Popen(['mbuild', 'generated_cpps/generated_hana_' + str(args.lines) + '_lines_' + str(i) + '_chars.cpp', '--verbose', '--', '-Iinclude', '-std=c++14'], stdout=PIPE, stderr=None, stdin=PIPE);

	output = p.stdout.read();
	if args.debug:
		print output;

	new_data = json.loads( output );
	data_hana.append(new_data);

	Xaxis.append(i);



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
			data_string[0][i]['optimisation'] = "no";
		path = 'plots/' + data_string[0][i]['compiler name'] + "/" + data_string[0][i]['compiler version'] + "/" + data_string[0][i]['optimisation'];

		if not os.path.exists(path + "/"):
			os.makedirs(path + "/");


		scatter_string = Scatter(
			x=Xaxis,
			y=Yaxis_string_user_time,
			name='Basic method',
			mode='lines+text',
			text=map(str, Yaxis_string_user_time),
			textposition='bottom right',
			textfont=dict(size=18));
		scatter_metaparse = Scatter(
			x=Xaxis,
			y=Yaxis_metaparse_user_time,
			name='Metaparse\'s String',
			mode='lines+text',
			text=map(str, Yaxis_metaparse_user_time),
			textposition='bottom right',
			textfont=dict(size=18));
		scatter_hana = Scatter(
			x=Xaxis,
			y=Yaxis_hana_user_time,
			name='Hana\'s String',
			mode='lines+text',
			text=map(str, Yaxis_hana_user_time),
			textposition='bottom right',
			textfont=dict(size=18));
		plotly.offline.plot({
			"data": [ scatter_string, scatter_metaparse, scatter_hana ],
			"layout": Layout( title="Compilation time with " + data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " (" + data_string[0][i]['optimisation'] + " optimisation)", xaxis=dict(title='Stringek hossza (karakterek)'), yaxis=dict(title='Idő (mp)'))
			},
			filename=path + '/user-time.html');
		if args.tex:
			write_graph_description(path, "user-time", data_string[0][i]['compiler name'], data_string[0][i]['compiler version'], data_string[0][i]['optimisation'], args.length, args.lines);


		scatter_string = Scatter(
			x=Xaxis,
			y=Yaxis_string_memory,
			name='Basic method',
			mode='lines+text',
			text=map(str, Yaxis_string_memory),
			textposition='bottom right',
			textfont=dict(size=18));
		scatter_metaparse = Scatter(
			x=Xaxis,
			y=Yaxis_metaparse_memory,
			name='Metaparse\'s String',
			mode='lines+text',
			text=map(str, Yaxis_metaparse_memory),
			textposition='bottom right',
			textfont=dict(size=18));
		scatter_hana = Scatter(
			x=Xaxis,
			y=Yaxis_hana_memory,
			name='Hana\'s String',
			mode='lines+text',
			text=map(str, Yaxis_hana_memory),
			textposition='bottom right',
			textfont=dict(size=18));
		plotly.offline.plot({
		"data": [ scatter_string, scatter_metaparse, scatter_hana ],
		"layout": Layout( title="Memory usage with " + data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " (" + data_string[0][i]['optimisation'] + " optimisation)", xaxis=dict(title='Stringek hossza (karakter)'), yaxis=dict(title='Felhasznált memória (KB)'))
		},
		filename=path + '/memory.html');
		if args.tex:
			write_graph_description(path, "memory", data_string[0][i]['compiler name'], data_string[0][i]['compiler version'], data_string[0][i]['optimisation'], args.length, args.lines);


		if 'template instantiations' in data_string[0][i]:
			scatter_string = Scatter(
				x=Xaxis,
				y=Yaxis_string_instantiations,
				name='Basic method',
				mode='lines+text',
				text=map(str, Yaxis_string_instantiations),
				textposition='bottom right',
				textfont=dict(size=18));
			scatter_metaparse = Scatter(
				x=Xaxis,
				y=Yaxis_metaparse_instantiations,
				name='Metaparse\'s String',
				mode='lines+text',
				text=map(str, Yaxis_metaparse_instantiations),
				textposition='bottom right',
				textfont=dict(size=18));
			scatter_hana = Scatter(
				x=Xaxis,
				y=Yaxis_hana_instantiations,
				name='Hana\'s String',
				mode='lines+text',
				text=map(str, Yaxis_hana_instantiations),
				textposition='bottom right',
				textfont=dict(size=18));
			plotly.offline.plot({
				"data": [ scatter_string, scatter_metaparse, scatter_hana ],
				"layout": Layout( title="Template instantiations with " + data_string[0][i]['compiler name'] + " " + data_string[0][i]['compiler version'] + " (" + data_string[0][i]['optimisation'] + " optimisation)", xaxis=dict(title='Stringek hossza (karakterek)'), yaxis=dict(title='Template példányosítások'))
			},
			filename=path + '/template-instantiations.html');
			if args.tex:
				write_graph_description(path, "template-instantiations", data_string[0][i]['compiler name'], data_string[0][i]['compiler version'], data_string[0][i]['optimisation'], args.length, args.lines);
