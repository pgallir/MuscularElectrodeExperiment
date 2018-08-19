'''
Jacopo Rigosa: Luglio 2018
jacopo.rigosa@gmail.com

Define here generic specifications for the session/experiment made with muscular electrodes 
'''

import read_adinstruments_matfile as adi


class myExperiment(adi.Experiment): 
    def _get_electrode_name(self):
        _idx = 0
        while 1:  
            if _idx==-1: break
            _idx = self._file.find("F",_idx+1)
            if self._file[_idx+1] >="0" <= "9" \
                and self._file[_idx+3] >="0" <= "9" \
                and self._file[_idx] == "F": # case sensitive
                    self._electrode_name = self._file[_idx:_idx+4]

    def _get_electrode_type(self): 
        # electrode type
        if "Intraneural" in self._file: self._electrode_type = "Intraneural"
        else:                           self._electrode_type = "Microneuro" 

    def _get_active_sites(self):
        # active sites - can be up or down (U/D)
        self._active_sites = {}
        _idxs = []
        # down
        _idx = 0
        while 1:  
            if _idx==-1: break
            _idx = self._file.find("D",_idx+1)
            if self._file[_idx-1] >="0" <= "9" \
                and self._file[_idx] == "D": # case sensitive
                _idxs.append(_idx)
        # up
        _idx = 0
        while 1:  
            if _idx==-1: break
            _idx = self._file.find("U",_idx+1)
            if self._file[_idx-1] >="0" <= "9" \
                and self._file[_idx] == "U": # case sensitive
                _idxs.append(_idx)
        #
        for _id_ch_less_1,_idx in enumerate(sorted(_idxs, key=int)): 
            _el = self._file[_idx-1:_idx+1]
            self._active_sites[_el] = _id_ch_less_1+1 # first is trigger

    def _parse_comtext_information(self,iChunk): 
        # given a chunk, get the message
        _idx_msg = self._comtext_assigned_to_chunk[iChunk]
        _msg     = self._data['comtext'][_idx_msg]
        # extra code needed which is Experiment dependent - MUST be implemented in the derived Experiment class implementations
        # ...
