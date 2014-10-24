# -*- coding: utf-8 -*-
'''
Created on Apr 13, 2014

@copyright 2014, Milton C Mobley

Parse patch file.
'''

# 2to3 from types import str

from patchtools.lib.diff       import Diff
from patchtools.lib.strings    import Strings
from patchtools.lib.ptobject   import PTObject
from patchtools.lib.exceptions import PT_NotFoundError, PT_ParameterError
from patchtools.lib.functions  import Functions as ut

#++
class Patch(PTObject):
    """ Extract information from a patch file
    """
    #--

    #++
    def __init__(self, path):
        """ Constructor
        
        Args:
            path (string): path to patch file
            
        Raises:
            PT_ParameterError
            PT_NotFoundError
        
        Notes:
            Commented out diff and hunk sections are omitted.
        """
        #--
 
        self.name = 'Patch'
        
        if (not ut.is_string_type(path)):
            raise PT_ParameterError(self.name, path)
        
        if (not ut.is_file(path)):
            raise PT_NotFoundError(self.name, path)
        
        strings = Strings(ut.read_strings(path))
        strings = strings.discard('"""','"""')
        
        # Split any email header from the patch data
        (_, body) = strings.partition('diff --git ')
        
        if (body is None): #all diffs commented out?
            self.diffs = []
            self.patch_type = 'text'
        else:
            # Split any email footer from the patch data
            (body, _) = body.rpartition('-- ')
            self._parse_body(body, 'diff --git ')
    
    #++
    @staticmethod
    def list_files(patchpath):
        """ List the files referenced by a patch, without duplicates
        
        Args:
            patchpath (string) path to patch file
            
        Returns:
            list of filenames
            
        Notes:
            A "filename" is the portion of the file's path after the kernel root,
            e.g. "drivers/iio/...".
        """
        #--
        
        strings = ut.read_strings(patchpath)
        files = {}
        for string in strings:
            if (string.startswith('diff --git ')):
                filename = ut.get_string_filename(string)
                files[filename] = True
        
        filenames = sorted(files)   # 2to3
        
        return filenames
            
    def _parse_body(self, strings, splitter):
        
        self.diffs = []
        self.patch_type = 'text'
        if (strings is not None):
            for rec in strings.split(splitter):
                diff = Diff(rec)
                if (diff.diff_type == 'binary'):
                    self.patch_type = 'binary'
                self.diffs += [diff]