'''
Jacopo Rigosa: Luglio 2018
jacopo.rigosa@gmail.com

Define here the specific force load session/experiment made with muscular electrodes 
'''

import os
import read_adinstruments_matfile as adi
from myExperiment import myExperiment

_full_path  = os.path.dirname(os.path.realpath(__file__))

class Force_Load_Session(adi.Session): 
    def __init__(self,path_to_files=None): 
        super(Force_Load_Session,self).__init__(path_to_files)
        self._drop_experiments_of_wrong_kind('force load')
        #self._collect_all_comtexts()

    def __getitem__(self,key):  
        try:
            _exp = Force_Load_Experiment(self._experiments_saved_file_list[key])
        except FileNotFoundError as err:
            print("*********FileNotFoundError********")
            print(self._experiments_saved_file_list[key])
            raise(err)
        except TypeError as err: 
            print("********TypeError*********")
            print("key", key)
            print(self._experiment_type[key])
            print(self._experiments_saved_file_list[key])
            raise(err)

        return _exp

class Force_Load_Experiment(myExperiment): 
    '''

        Experiment: different kinds... you understand from comments...
            
            -1- 
                - ch1 instramuscular stimulus with increasing current [1,15] mA , 3 repetitions each (first are removed, start from last, last always 15 mA), pulsewidth 10 uSec (compute charge)
                - ch6 force load
                - GOAL: make statistical analysis on ...
                        ...the elicited force by using different active sites and stimulation current 
                        ...difference between muscle fibers (slow vs fast)
            
            -2-
                - stimulation pulses at different pulse-per-second (check the trigger, these trials are not separated in chunks...) 
                - GOAL: study muscular fatigue 


    '''

    pass


if __name__ == "__main__": 

    _path_to_data = _full_path+'/../data/'

    try: 
        sess = Force_Load_Session(_path_to_data)
    except Exception as err: 
        print("*** expected err: ",end = "")
        print(err)

    print("\n show all experiments in the session")
    print(sess)
