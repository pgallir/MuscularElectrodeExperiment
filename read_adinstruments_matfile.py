'''
Jacopo Rigosa: Luglio 2018
jacopo.rigosa@gmail.com

Module to read ADInstruments generated matfile (from .adicht using labchart)

Fields in the .mat: 
    - 'data' contains the whole data 
    - 'datastart', 'dataend' indicate when the different chunks start and end
    - 'titles' contains the labels for the channels recorded 
    - 'rangemin', 'rangemax' contain the min-max values recorded in the channel 
    - 'unittext' contains the x-axis label
    - 'blocktimes' ...unknown...
    - 'tickrate' contains the sample frequency (Hz) 
    - 'firstsampleoffset' ...unknown - always zero: probably starting always from first sample without any offset... 
    - 'comtext' contains the comments added to trials 
    - 'com' are infos needed to contextualize 'comtext': in particular the second column of each 'com' instance indicate the chunk were the comment is located

The class Experiment knows the fields contained in the .mat to access the data. 
The class Session collets many experiments. 

Specific Session/Experiment implementations must be specifically defined. 
'''



import sys
import os
import glob
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

_full_path  = os.path.dirname(os.path.realpath(__file__))

class Session(object): 
    def __init__(self,path_to_files=None): 
        self._experiments_saved_file_path = path_to_files
        if self._experiments_saved_file_path:
            self._experiments_saved_file_list=glob.glob(path_to_files+"/*.mat") # only malab files
        else: raise(Exception("no folder provided"))        

    def _drop_experiments_of_wrong_kind(self, kind):    # utility for classes who inherits from Session
        assert type(kind) is type(""), "'kind' must be a string"
        _exp_file_list_copy = self._experiments_saved_file_list
        self._experiments_saved_file_list = []
        for i,_exp in enumerate(_exp_file_list_copy):
            if kind in _exp: 
                self._experiments_saved_file_list.append(_exp)
        self._test_session_kind(kind)

    def _test_session_kind(self, kind):                 # utility for classes who inherits from Session
        assert type(kind) is type(""), "'kind' must be a string"
        for i,_exp in enumerate(self._experiments_saved_file_list):
            if kind not in _exp: raise(Exception(_exp+": this file does not contain an experiment of kind '"+kind+"'")) 

    def _collect_all_comtexts(self):                    # utility for classes who inherits from Session
        for i,_exp in enumerate(self._experiments_saved_file_list):
            print(_exp)
            print(self[i]._data['comtext'])

    def __len__(self): return len(self._experiments_saved_file_list)

    def __iter__(self):
        self.__i = 0                #  iterable current item 
        return iter(self._experiments_saved_file_list)

    def __next__(self):
        if self.__i<len(self._experiments_saved_file_list)-1:
            self.__i += 1         
            return self._experiments_saved_file_list[self.__i]
        else:
            raise StopIteration
    
    def __str__(self): 
        s = "list of experiments: \n"
        for idx,f in enumerate(self._experiments_saved_file_list): 
            s+=str(idx)+":\t"+repr(f)+"\n"
        return s
    
    def __getitem__(self,key):  
        try:
            _exp = Experiment(self._experiments_saved_file_list[key])
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

class Experiment(object): 
    def __init__(self,filename):
        # controllo se il filename e` valido
        if type(filename) != type(""):                 
            raise(Exception("filename should be string"))
        if not os.path.exists(filename): 
            raise(Exception("filename does not exists"))
        
        # carico i dati
        self._file = filename
        self._data = scipy.io.loadmat(self._file)
        
        # i dati sono divisi in canali e in chunks 
        #       per ogni canale i dati sono divisi in chunks
        #       ciascuno dei quali corrisponde ad una prova
        #       la prova viene descrita nella sezione comtext
        assert len(self._data['dataend'])    == len(self._data['datastart']   ),\
                "datastart var must have same dim of dataend (rows)"
        assert len(self._data['dataend'][0]) == len(self._data['datastart'][0]),\
                "datastart var must have same dim of dataend (cols)"
        self._num_channels = len(self._data['dataend'])     # #channels 
        self._num_chunks   = len(self._data['dataend'][0])  # #chunks 
        
        # testo che mi tornino le dimensioni dei canali e dei chunks 
        assert self._num_channels == len(self._data['titles'])   ,\
                "titles var names channels: should have same #elements of dataend #rows"
        assert self._num_chunks   == len(self._data['datastart'][0]),\
                "datastart var should have same dim of dataend"
        #assert self._num_chunks == len(self._data['comtext'])   ,\
        #        "comtext var names chunks: should have same #elements of dataend #columns"
        self._assign_comtext_to_chunk()

    def __getitem__(self,key): 
        # l'indicizzazione di matlab permette tipi non interi e comincia da 1
        # in python devono essere interi e partono da 0
        _init = [int(i)-1 for i in self._data['datastart'][key]] 
        _end  = [int(e)-1 for e in self._data['dataend'][key]  ]
        _channel = [] 

        for _i,_e in zip(_init,_end): 
            if _i == -1 or              \
               _e == -1:    
                _channel = None
                break
            else:           
                _channel.append(self._data['data'][0][_i:_e])
        return _channel 

    def __str__(self): 
        _to_print ="\nSummary of ...\n\t" + self._file                   +"\n"
        _to_print+=" - channels: "   +str(self._num_channels)            +"\n"
        _to_print+=" - chunks:   "   +str(self._num_chunks)              +"\n"
        _to_print+=" - len(comtext):"+str(len(self._data['comtext']))    +"\n" 
        _to_print+=" - len(com):"    +str(len(self._data['com']))        +"\n" 
        _to_print+=" - len(com[0]):" +str(len(self._data['com'][0]))     +"\n" 
        return _to_print

    def _assign_comtext_to_chunk(self): 
        self._comtext_assigned_to_chunk = {}
        _range_chunks_to_update = [] 
        _from_this_chunk = 0 # first chunk
        for _idx,_com in enumerate(self._data['com']): 
            _up_to_this_chunk = int(_com[1])

            if _from_this_chunk == _up_to_this_chunk: 
                for _chunk in _range_chunks_to_update:
                    self._comtext_assigned_to_chunk[_chunk].append(_idx)
            else: 
                _range_chunks_to_update = [i for i in range(_from_this_chunk,_up_to_this_chunk)]
                for _chunk in _range_chunks_to_update:
                    self._comtext_assigned_to_chunk[_chunk] = [_idx]
                _from_this_chunk = _up_to_this_chunk

    def _show_data(self): print(self._data)

    def _plot(self,iChannel=None,iChunk=None): 
        # default   all channels 
        _one_ch_to_plot = True
        if not iChannel:    
            iChannel = self._num_channels
            _one_ch_to_plot = False
        else: 
            if iChannel > self._num_channels: 
                raise Exception("there are not enough channels")
        # default all chunks
        _stack_them_all = False
        if not iChunk:     
            iChunk  = self._num_chunks
            _stack_them_all = True
        else: 
            if iChunk > self._num_chunks: 
                raise Exception("there are not enough chunks")
        # 
        # create the axes
        #
        if _one_ch_to_plot: 
            fig, ax = plt.subplots()
        else: 
            fig, ax = plt.subplots(iChannel,1,sharex=True)
        #
        # plot stuff
        #
        if _stack_them_all:
            for _channel in range(iChannel):
                _to_be_filled = np.asarray([])
                for _chunk in range(iChunk):
                    _to_be_filled = np.append(_to_be_filled,\
                                              self[_channel][_chunk])
                if _one_ch_to_plot: 
                    ax.plot(_to_be_filled)
                else: 
                    ax[_channel].plot(_to_be_filled)
        else: 
            ax.plot(self[iChannel-1][iChunk])
        plt.show()

def interactive_data_exploration(iData):
    print(sess[iData])
    print(sess[iData]._data['comtext'])
    print(sess[iData]._data['com'])
    sess[iData]._plot()


if __name__ == "__main__": 

    print("\ntesto che non vengano macinate sessioni senza un path")
    try: 
        sess = Session()
    except Exception as err: 
        print("*** expected err: ",end = "")
        print(err)

    print("\n\ntesto sessioni con path")
    _path_to_data = _full_path+'/../../data/'
    sess = Session(_path_to_data)

    print("\n test session slicing -> experiment")
    #idx = [i for i,el in enumerate(sess._experiments_saved_file_list) if "2_9" in el][0]
    for i,_exp_filename in enumerate(sess): 
        _exp = sess[i]
        print(sess[i]) 
        print(sess[i]._data)
        if i>1: break

    print("\n test experiment slicing -> channel")
    print(sess[0][0])

    print("\n list experiments")
    print(sess)

    if False: 
        iData = 6
        interactive_data_exploration(iData) 

    
