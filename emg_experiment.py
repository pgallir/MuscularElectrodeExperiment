'''
Jacopo Rigosa: Luglio 2018
jacopo.rigosa@gmail.com

Define here the specific EMG session/experiment made with muscular electrodes 
'''

import os
import read_adinstruments_matfile as adi
from myExperiment import myExperiment

_full_path  = os.path.dirname(os.path.realpath(__file__))

class EMG_Session(adi.Session): 
    def __init__(self,path_to_files=None): 
        super(EMG_Session,self).__init__(path_to_files)
        self._drop_experiments_of_wrong_kind('EMG')
        #self._collect_all_comtexts()

    def __getitem__(self,key):  
        try:
            _exp = EMG_Experiment(self._experiments_saved_file_list[key])
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

class EMG_Experiment(myExperiment): 
    '''
        GOAL: make statists.... 
        
        Experiment: recorded EMG signals after different kind (see the comment) of continuous toe-pain stimulation (trigger)
            - 3 triggers for each stimulus kind 
                - if kind is written in comment ok, trust it...
                - ... otherwise the sequence is generally 3-3-3-3 of {pressure, pinch, controlateral pinch, strong pinch} ...
                - ... sometimes ({sanna vs needle pinch} {sanna vs needle strong pinch}) channel 2 is not an active site but it is an EMG: 
                    - check the qualitative difference in the feature sets between different kind of EMG electrodes 
                    
                
        filename meaning: 
            ex: F1.7   EMG ch2.5     2U 3U 5U 7U
                |       |   |           |
            electrode   |   |           muscular active 
                        | channel       sites  (simultaneously)
                        |    used       used 
                        |
                        experiment type

            PLEASE NOTE THAT intraneural means nothing for EMG experiments


        active sites: 
            - recording sites is tibial muscle 
            - #active sites are chFROM.TO
            - U means UP 
            - D means DOWN

    '''

    def __init__(self,filename): 
        super(EMG_Experiment,self).__init__(filename)
        self._parse_filename_information()

    def __getitem__(self,key): 
        assert type(key) is type(1), "this __getitem__ implementation works with integer keys"
        self._parse_comtext_information(key)
        return super(EMG_Experiment,self).__getitem__(key)

    def _parse_filename_information(self): 
        if "EMG" not in self._file: raise Exception("this experiment is of the wrong type")
        self._get_electrode_name()
        self._get_electrode_type() 
        self._get_active_sites()
        #print(self._file)
        #print(self._electrode_name, self._electrode_type, self._active_sites)
        
    def _parse_comtext_information(self,iChunk): 
        # retreive the list of messages for that chunk 
        _msg_list = self._get_comtext_msg_from_chunk(iChunk) 
        
        print(_msg_list)

if __name__ == "__main__": 

    _path_to_data = _full_path+'/../data/'

    try: 
        sess = EMG_Session(_path_to_data)
    except Exception as err: 
        print("*** expected err: ",end = "")
        print(err)

    print("\n show all experiments in the session")
    print(sess)

    print(type(sess))
    print(type(sess[0]))
    print(type(sess[0][0]))
    print(sess[1][0])
