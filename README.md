# MuscularElectrodeExperiment
Analysis of data recorded with custom made muscular electrodes.

Data have been recorded with ADInstruments.
Data have been exported with Labchart to matfiles.
Analysis are made using python, loading matfiles with a scipy utility.

Long story short:
 - read\_adinstruments\_matfile.py:     
   main utility to access data
 - myExperiment.py, \*experiment.py:  
   implementation of specific features for the experiment(s) conducted
 - \*comtext.txt:                      
   collection of comments for any experiment kind

Further info in the first commit.
