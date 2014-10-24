# -*- coding: utf-8 -*-
'''
Created on Apr 13, 2014

@copyright 2014, Milton C Mobley
'''

# 2to3 from types import StringTypes

from patchtools.lib.ptobject   import PTObject
from patchtools.lib.exceptions import PT_NotFoundError, PT_ParameterError
from patchtools.lib.functions  import Functions as ut

#++
class Archive(PTObject):
    """ Extract information from "patch archive" files
    """
    #--
   
    #++
    def __init__(self, path):
        """ Constructor
          
        Args:
            path (string): path to patch archive file
            
        Raises:
            PT_ParameterError, PT_NotFoundError
        
        Notes:
             A "patch archive" file lists diff sections from patches that were applied to
             produce the associated kernel version. Since the patch archive files can be very large,
             we take care to avoid copying or storing data that is not of interest to the user.
        """
        #--

        self.name = 'Archive'
        
        if (not ut.is_string_type(path)):
            raise PT_ParameterError(self.name, path)
        
        if (not ut.is_file(path)):
            raise PT_NotFoundError(self.name, path)
        
        self._path = path
    
    #++
    def sections(self, filenames):
        """ Find archive file sections that modify files also modified by our patches
        
        Args:
            filenames (list): file names referenced in our patches
            
        Returns:
            A list of sections. Each section is a list of strings, in which
            the first string identifies the start line number of a diff section,
            and the remaining strings are the content of the diff section.
            
        Raises:
            None
        """
        #--
        sections = []
        for (begin, segment) in self._segments():
            if (ut.get_string_filename(segment[0]) in filenames):
                sections += [['archive line %d:' % begin] + segment]
        
        return sections
                    
    def _segments(self):
        ''' Use generator to split the archive file into diff segments
        '''
        index = begin = 0
        curr_seg = []
        for string in ut.read_strings(self._path):
            if (string.startswith('diff ')):
                if (len(curr_seg) > 0):
                    yield (begin, curr_seg)
                begin = index
                curr_seg = [string]
            else:
                curr_seg += [string]
            index += 1
        