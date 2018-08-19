'''
Jacopo Rigosa: Luglio 2018
jacopo.rigosa@gmail.com

Define here the specific EMG session/experiment made with muscular electrodes 
'''

import os
import read_adinstruments_matfile as adi
from myExperiment import myExperiment

_full_path  = os.path.dirname(os.path.realpath(__file__))

class CMAP_Session(adi.Session): 
    def __init__(self,path_to_files=None): 
        super(CMAP_Session,self).__init__(path_to_files)
        self._drop_experiments_of_wrong_kind('CMAP')
        #self._collect_all_comtexts()

    def __getitem__(self,key):  
        try:
            _exp = CMAP_Experiment(self._experiments_saved_file_list[key])
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

class CMAP_Experiment(myExperiment): 
    ''' 
        GOAL: make statistical analysis between different active sites

        Experiment: recorded tibial muscle signals during continuous neural stimulation (trigger) 

        filename meaning: 
            ex: F1.7 CMAP ch2.5     2U 3U 5U 7U
                |       |   |           |
            electrode   |   |           muscular active 
                        | channel       sites  (simultaneously)
                        |    used       used 
                        |
                        experiment type

        CMAP: 
            - sciatic nerve is stimulated with microneurography (or intraneural if specified) 
            - stimulation range [1,15] mA, step 1 mA -- for each com should be 15 chunks (test it, if not do not process) 
                                                     -- read the comment
                                                     
        active sites: 
            - recording sites is tibial muscle 
            - #active sites are chFROM.TO
            - U means UP 
            - D means DOWN

    '''

    pass


if __name__ == "__main__": 

    _path_to_data = _full_path+'/../data/'

    try: 
        sess = CMAP_Session(_path_to_data)
    except Exception as err: 
        print("*** expected err: ",end = "")
        print(err)

    print("\n show all experiments in the session")
    print(sess)
