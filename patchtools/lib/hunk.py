# -*- coding: utf-8 -*-
'''
Created on Apr 13, 2014

@copyright 2014, Milton C Mobley

Parse a patch hunk section.
'''

from patchtools.lib.ptobject  import PTObject
from patchtools.lib.functions import Functions as ut

#++
class Hunk(PTObject):
    """ Extract information from a hunk section of a patch file
    """
    #--

    #++
    def __init__(self, strings):
        """ Constructor
        
        Args:
            strings (Strings): hunk section from a patch file or archive file
        """
        #--
        
        # On rare occasions, a hunk may be followed by an empty line before the next diff
        while (len(strings[-1]) == 0):
            strings.pop(-1)
            
        self._parse_hunk_line(strings[0])
        self.edits = strings[1:]
    
    def _parse_hunk_line(self, string):
        ''' Parse hunk line like '@@ -428,7 +428,7 @@ DEFINE_...'. The text after
            the second '@@' is a 'hunk note'.
        '''

        self.spec = string
        string = ut.normalize_string(string, False)
        
        (_, old, new, tail) = string.split(' ', 3)
        if (tail == '@@'): # no hunk note
            self.note = ''
        else:
            self.note = tail.split(' ')[1]
        
        parts = old[1:].split(',')
        self.old_start = int(parts[0])
        if (',' in old): # old has line count
            self.old_count = int(parts[1])
        else:
            self.old_count = 1
        
        parts = new[1:].split(',')
        self.new_start = int(parts[0])
        if (',' in new): # new has line count
            self.new_count = int(parts[1])
        else:
            self.new_count = 1