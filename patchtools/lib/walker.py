# -*- coding: UTF-8 -*-
'''
Created on Apr 10, 2014

@copyright 2014, Milton C Mobley
'''

import os
# 2to3 from types import StringTypes

from patchtools.lib.ptobject   import PTObject
from patchtools.lib.exceptions import PT_ParameterError
from patchtools.lib.matcher    import Matcher
from patchtools.lib.functions  import Functions as ut

#++
class Walker(PTObject):
    """ Enumerate paths of selected files in a source tree
    """
    #--
    
    #++
    def __init__(self, params):
        """ Constructor
        
        Args:
            params (dict, required)  parameters:
                root_path  (string, required): search root path
                incl_dirs  (list, optional):   top level subdirs to include
                excl_dirs  (list, optional):   top level subdirs to exclude
                incl_files (dict, optional):   include file name filters
                excl_files (dict, optional):   exclude file name filters
                test_dirs  (bool, optional):   True = include dir in tests
                    
        Raises:
            PT_ParameterError
            
        Notes:
            The "root_path" parameter specifies the root of the search.
            If the "incl_dirs" option is specified, only those subdirs of the root will be searched.
            If the "excl_dirs" option is specified, those subdirs of the root will not be searched.
            If the "incl_files" option is specified, only those filetypes will be enumerated.
            If the "excl_files" option is specified, those filetypes will not be enumerated.
            If it is desired to search a folder that is a subfolder of an excluded folder,
            the search must be split into two operations.
            When callback functions need the containing directory to test a file name,
            the 'test_dirs' option should be set to True
            
            Walking a large file tree can take significant time and produce a large amount of data,
            but this tendency can be reduced by cleaning the tree of generated files beforehand,
            and by applying suitable directory and file filters.   
        """
        #--
        
        self.name = 'Walker'
        
        if ((params is None) or (not isinstance(params, dict))):
            raise PT_ParameterError(self.name, 'params')
           
        self._root_path = self._check_required_string_param(params, 'root_path')
        self._check_path_param('root_path', self._root_path)
        
        incl_dirs  = self._check_optional_param(params, 'incl_dirs',  list, None)     
        excl_dirs  = self._check_optional_param(params, 'excl_dirs',  list, None)    
        incl_files = self._check_optional_param(params, 'incl_files', dict, None)    
        excl_files = self._check_optional_param(params, 'excl_files', dict, None)        
        
        self.test_dirs = self._check_optional_param(params, 'test_dirs', bool, False)
        self._trim_paths = self._check_optional_param(params, 'trim_paths', bool, True)
        
        if ((incl_dirs is None) and (excl_dirs is None)):
            self._folders = [self._root_path] 
        
        elif (incl_dirs is not None): # only iterate over incl_dirs
            self._folders = [ut.join_path(self._root_path, d) for d in incl_dirs] 
        
        else: # exclude subdirs in excl_dirs
            dirs = [d for d in os.listdir(self._root_path) 
                    if os.path.isdir(ut.join_path(self._root_path, d))]
            for x in excl_dirs:
                if x in dirs:
                    dirs.remove(x)
            self._folders = [ut.join_path(self._root_path, d) for d in dirs]
            
        if (incl_files is not None):
            self._incl_files_filter = Matcher(incl_files)
        else:
            self._incl_files_filter =  None
    
        if (excl_files is not None):
            self._excl_files_filter = Matcher(excl_files)
        else:
            self._excl_files_filter =  None    
    
    #++
    def walk(self):
        """  The walk starts here
        
        Args:
            None
            
        Returns:
            A list of matching file paths
            
        Raises:
            None
        """
        #--
    
        results = []

        for f in self._folders:
            for (dir1, _, files) in os.walk(f):
                if (len(files) > 0):
                    # Pythons's os.walk function will prepend the root path to dir1
                    dir2 = ut.trim_path(self._root_path, dir1)
                    if (self._trim_paths):
                        results += self._enumerate(dir2, files)
                    else:
                        results += self._enumerate(dir1, files)
                        
        return results
    
    def _enumerate(self, dir_, files):
        
        results = []
        
        for file_ in files:
            if (self.test_dirs):
                path = ut.join_path(dir_, file_)
            else:
                path = file_
            if ((not self._is_file_excluded(path)) and self._is_file_included(path)):
                results += [ut.join_path(dir_, file_)]
        
        return results
    
    def _is_dir_excluded(self, dir_):
        
        if (self._excl_dirs_filter is None):
            return False
        else:
            return (self._excl_dirs_filter(dir_) is not None)
    
    def _is_dir_included(self, dir_):
        
        if (self._incl_dirs_filter is None):
            return True
        else:
            return (self._incl_dirs_filter(dir_) is not None)
    
    def _is_file_excluded(self, name):
        
        if (self._excl_files_filter is None):
            return False
        else:
            return (self._excl_files_filter(name) is not None)
        
    def _is_file_included(self, name):
        
        if (self._incl_files_filter is None):
            return True
        else:
            return (self._incl_files_filter(name) is not None)
