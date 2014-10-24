# -*- coding: utf-8 -*-
'''
Created on Apr 13, 2014

@copyright 2014, Milton C Mobley

Parse a patch diff section.
'''

from patchtools.lib.ptobject   import PTObject
from patchtools.lib.hunk       import Hunk
from patchtools.lib.exceptions import PT_ParameterError
from patchtools.lib.functions  import Functions as ut

#++
class Diff(PTObject):
    """ Extract information from a diff section of a patch file
    """
    #--
    
    #++
    def __init__(self, strings):
        """ Constructor
         
        Args:
            strings (Strings): diff section from a patch file or archive file
            
        Raises:
            PT_ParameterError
        """
        #--
    
        self.name = 'Diff'
        
        if ((strings is None) or (not isinstance(strings, list))):
            raise PT_ParameterError(self.name, 'strings')
        
        (head, body) = strings.partition('@@ ')
        self._parse_head(head)
        self._parse_body(body)
    
    def _parse_head(self, strings):
        
        if (strings[0].startswith('diff -')):
            self._parse_diff_line(strings[0])
        else:
            self.spec   = None
            self.a_path = None
            self.b_path = None
            
        self.diff_type = 'text'
        for string in strings[1:]:
            if (string == 'GIT binary patch'):
                self.diff_type = 'binary'
                self.old_path  = None
                self.new_path  = None
                break
            elif (string.startswith('--- ')):
                if (string[4:] == '/dev/null'):
                    self.old_path = '/dev/null'
                else:    
                    self.old_path = string[6:] # drop leading 'a/'
            elif (string.startswith('+++ ')):
                if (string[4:] == '/dev/null'):
                    self.new_path = '/dev/null'
                else:    
                    self.new_path = string[6:] # drop leading 'b/'   
    
    def _parse_diff_line(self, string):
        ''' Extract old and new paths from diff line, which has a format like:
                'diff --git a/<path_to_file> b/<path_to_file>'
            We extract the paths and strip the leading 'a/' or 'b/'.
        '''
        self.spec = string
        string = ut.normalize_string(string, False)
        parts  = string.split(' ')
        self.a_path = parts[2][2:] # strip 'a/'
        self.b_path = parts[3][2:] # strip 'b/'
        
        # On rare occasions the diff line is corrupted
        if (self.a_path.endswith('/')):
            self.a_path = self.b_path
            
    def _parse_body(self, strings):
        
        if (strings is None):
            self.hunks = []
        else:
            self.hunks = [Hunk(rec) for rec in strings.split('@@ ')]
        