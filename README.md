# Metastring-measurement
The purpose of this project is to measure time and memory usage of compile-time strings.

* measure_by_length.py creates .cpp files with increasing length. Run with python measure_by_length.py
* measure_by_lines.py creates .cpp files with increasing number of lines. Run with python measure_by_lines.py

Use python measure_by_length.py -debug or python measure_by_lines.py -debug to print out the json data which is processed by mbuild.

# Requirements

* The two scripts need create_files.py and toUpperChar.cpp files, they should be put next to them.
* The two scripts need mbuild, it should be put next to them.
* The two scripts need boost 1.60.0., which should be placed in the boost_1_60_0 folder next to them.

* The script also needs plotly to be installed. You can get it with "sudo pip install plotly". For more info, go to https://plot.ly/python/
