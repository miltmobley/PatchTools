# -*- coding: UTF-8 -*-
'''
Created on Mar 13, 2014

@copyright 2014, Milton C Mobley

View patch archive diff sections and related patch and source files.
        
See the watcher module section of the documentation for further information.
'''

# 2to3 from types import str

from patchtools.lib.archive    import Archive
from patchtools.lib.viewer     import Viewer
from patchtools.lib.patchset   import PatchSet
from patchtools.lib.ptobject   import PTObject
from patchtools.lib.exceptions import PT_NotFoundError, PT_ParameterError
from patchtools.lib.functions  import Functions as ut

#++
class Watcher(PTObject):
    """ Determine if your patches have been integrated into released kernel versions
    """
#--
    
    #++
    def __init__(self, params):
        """ Constructor
        
        Args:
            params (dict): parameters
                patchdir  (string, required): path to patch folder
                sourcedir (string, required): path to source folder
                datadir   (string, required): path to data folder
                tempdir   (string, required): path to temp file folder
                patchset  (dict, required):   description of patches
                
        Raises:
            PT_ParameterError
            PT_NotFoundError
        
        Notes:
            Experience in testing shows a very low probability that an archive
            diff section will match any of our patches exactly, so we merely
            display the related files.
        """
        #--
        
        self.name = 'Watcher'
        
        if ((params is None) or (not isinstance(params, dict))):
            raise PT_ParameterError(self.name, 'params')
        
        self._patchdir = self._check_required_string_param(params, 'patchdir')
        self._check_path_param('patchdir', self._patchdir)
        
        self._sourcedir = self._check_required_string_param(params, 'sourcedir')
        self._check_path_param('sourcedir', self._sourcedir)
        
        self._datadir = self._check_required_string_param(params, 'datadir')
        self._check_path_param('datadir', self._datadir)
        
        self._tempdir = self._check_required_string_param(params, 'tempdir')
        self._check_path_param('tempdir', self._tempdir)
        
        self._patchset = PatchSet(params)
        
    #++    
    def watch(self, archpath):
        """ View files related to archive diff sections
        
        Args:
            archpath (string): path to patch archive file
            
        Returns:
            None. Output is a series of launches of the Viewer to view the files.
            
        Raises:
            PT_ParameterError
            PT_NotFoundError
        """
        #--
        
        if (not ut.is_string_type(archpath)):
            raise PT_ParameterError(self.name, 'archpath') 
        
        if (not ut.is_file(archpath)):
            raise PT_NotFoundError(self.name, archpath)
               
        tempfile = ut.join_path(self._tempdir, 'archdata.txt')
        filedata = self._patchset.get_file_data()
        filenames = [key for key in filedata]
        a = Archive(archpath)
        s = a.sections(filenames)
        print("Found %d matching sections" % len(s))
        v = Viewer()
        for section in s:
            ut.write_strings(section, tempfile)
            filename = ut.get_string_filename(section[1])
            filepath = ut.join_path(self._sourcedir, filename)
            patchfiles = []
            for (fn, _) in filedata[filename]:
                patchfiles += [ut.join_path(self._patchdir, fn)]
            r = v.view([tempfile, filepath] + patchfiles)
            print(r)
        
        
        
                                                                            
    