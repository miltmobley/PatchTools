# -*- coding: utf-8 -*-
'''
Created on Mar 29, 2014

@copyright 2014, Milton C Mobley

Implement string like methods for lists of strings.

The module implements its own exceptions and reimplements certain utility functions,
since the code may be useful in other projects.

See the strings module section of the documentation for further information.
'''

import sys
from platform import system
# 2to3 from types import StringTypes

_is_windows = ("Windows" in system())
_is_python3 = (sys.version_info[0] >= 3) # 2to3

class StringsError(Exception):
    def __init__(self, msg):
        super(StringsError, self).__init__(msg)
        self.mod = 'Strings'
        
class StringsParameterError(Exception):
    def __init__(self, msg):
        super(StringsParameterError, self).__init__('parameter Error: ' + msg)
        
#++
class Strings(list):
    """ Provide some useful string like methods for lists of strings
    """
    #--
    
    #++
    def __init__(self, data=None):
        """ Constructor
        
        Args:
            data (list, optional): a list of strings 
            
        Raises:
            StringsParameterError
        """
        #--
 
        if (data is not None):
            if (not isinstance(data, list)):
                raise StringsParameterError('data', data)
            for item in data:
                if (not self._is_string_type(item)):
                    raise StringsParameterError('data', data)
        else:
            data = []
            
        super(Strings, self).__init__(data)
    
    #++
    def __getitem__(self, i):
        """ Ensure that slices of Strings objects are returned as Strings objects, not lists
            
        Args:
            i (int):   item index
            i (tuple): (start, stop, [step])
            
        Returns:
            Strings(self[i:j])
        
        Notes:
            For mysterious reasons, slice keys can be passed as tuples, not slice objects.
            In such cases, we convert the tuples to slices.
        """
        #--
        
        if isinstance(i, tuple):
            if (len(i) > 2):
                i = slice(i[0], i[1], i[2])
            else:
                i = slice(i[0], i[1])
            
        value = super(Strings, self).__getitem__(i)
        
        if isinstance(value, list):
            value = Strings(value)
        
        return value
                        
    #++
    def find(self, pattern, begin=None, end=None):
        """ Find the first string in our data that starts with (pattern)
            
        Args:
            pattern (str):  the substring to match
            begin   (int):  start index
            end     (int):  stop index
            
        Returns:
            Found: the index of matching string
            Not found: -1
            
        Raises:
            StringsParameterError
                
        Notes:
            If begin is not specified, it is set to 0
            If end is not specified, it is set to len(self).
            All strings are left stripped before testing.
        """
        #--
        index, _ = self.match([pattern], begin, end)
        
        return index
        
    #++
    def match(self, patterns, begin=None, end=None):
        """ Find the first string in our data that starts with a pattern in (patterns)
            
        Args:
            patterns (list): The substring to match
            begin    (int):  Start index
            end      (int):  Stop index
            
        Returns:
            Found: the index of matching string, and the matching pattern
            Not found: -1, ''
            
        Raises:
            StringsParameterError
                
        Notes:
            If begin is not specified, it is set to 0
            If end is not specified, it is set to len(self).
            All strings are left stripped before testing.
        """
        #--
        plen = len(patterns)
        for index in range(plen):
            patterns[index] = self._check_string_param('pattern', patterns[index])
        length = len(self)
        begin  = self._check_index_param('begin', begin, 0, length, 0)
        end    = self._check_index_param('end', end, 0, length, length)
        
        if (begin > end):
            raise StringsParameterError('begin, end', (begin, end))
              
        for index1 in range(begin, end):
            string = self[index1].lstrip()
            for index2 in range(plen):
                if (string.startswith(patterns[index2])):
                    return index1, patterns[index2]
                
        return -1, ''
    
    #++
    def rfind(self, pattern, begin=None, end=None):
        """ Find the last string in our data that starts with (pattern)
            
        Args:
            pattern (str):  the substring to match
            begin   (int):  start index
            end     (int):  stop index
            
        Returns:
            Found: the index of matching string
            Not found: -1
            
        Raises:
            StringsParameterError
                    
        Notes:
            If end is not specified, it is set to -1.
            len(self) is added to the value of begin.
            All strings are left stripped before testing.
        """
        #--
        index, _ = self.rmatch([pattern], begin, end)
        
        return index
    
    #++
    def rmatch(self, patterns, begin=None, end=None):
        """ Find the last string in our data that starts with a string in (patterns)
            
        Args:
            patterns (str): The substrings to match
            begin    (int):  Start index
            end      (int):  Stop index
            
        Returns:
            Found: the index of matching string, and the matching pattern
            Not found: -1, ''
            
        Raises:
            StringsParameterError
                    
        Notes:
            If end is not specified, it is set to -1.
            len(self) is added to the value of begin.
            All strings are left stripped before testing.
        """
        #--
        
        plen = len(patterns)
        for index in range(plen):
            patterns[index] = self._check_string_param('pattern', patterns[index])
        length = len(self)
        begin  = self._check_index_param('begin', begin, length - 1, -1, length - 1)
        end    = self._check_index_param('end', end, -1, length - 1, -1)
        
        if (begin < end):
            raise StringsParameterError('begin, end', (begin, end))
            
        for index1 in range(begin, end, -1):
            string = self[index1].lstrip()
            for index2 in range(plen):
                if (string.startswith(patterns[index2])):
                    return index1, patterns[index2]
                
        return -1, ''
    
    #++
    def filter(self, pattern, begin=None, end=None):
        """ Find all strings in our data that start with (pattern)
            
        Args:
            pattern (str):  the substring to match
            begin   (int):  start index
            end     (int):  stop index
            
        Returns:
            Found: A list of the indices of the matching strings
            Not found: None
            
        Raises:
            StringsParameterError
                    
        Notes:
            If begin is not specified, it is set to 0
            If end is not specified, it is set to len(self).
            All strings are left stripped before testing.
        """
        #--
        
        pattern = self._check_string_param('pattern', pattern)
        length = len(self)
        begin  = self._check_index_param('begin', begin, 0, length, 0)
        end    = self._check_index_param('end', end, 0, length, 0)
        
        if (begin > end):
            raise StringsParameterError('begin, end', (begin, end))
        
        return [index for index in range(begin, end) if self[index].lstrip().startswith(pattern)]
    
    #++
    def index(self, pattern):
        """ Return indices of strings that exactly match (pattern)
        
        Args:
            pattern (string): search text
            
        Raises:
            StringsParameterError
        """
        #--
        
        pattern = self._check_string_param('pattern', pattern)
        
        matches = []
        for index in range(len(self)):
            if (self[index] == pattern):
                matches += [index]
        
        return matches
    
    #++
    def lstrip(self):
        """ Remove leading lines that are empty or whitespace
        
        Args:
            none
            
        Returns:
            self, to allow chaining to slices, other methods
        """
        #--
        
        while ((len(self) > 0) and ((len(self[0]) == 0) or self[0].isspace())):
            self.pop(0)
        
        return self
    
    #++
    def rstrip(self):
        """ Remove trailing lines that are empty or whitespace.
        
        Args:
            none
            
        Returns:
            self, to allow chaining to slices, other methods
        """
        #--
        
        while ((len(self) > 0) and ((len(self[-1]) == 0) or self[-1].isspace())):
                self.pop(-1)
        
        return self
            
    #++
    def partition(self, splitter):
        """ Split our data into two parts at a splitter pattern, searching forwards
            
        Args:
            splitter (str): The substring that splits the parts
                
        Returns:
            splitter was found:
                A tuple (head, tail) where head is a Strings object containing the first part,
                and tail is a Strings object containing the second part.
            splitter was not found:
                (self, None)
            
        Notes:
            Example: (head, body) = patch.partition('diff --git ')  
        """
        #--
        
        splitter = self._check_string_param('splitter', splitter)
        
        index = self.find(splitter)
        if (index != -1):
            return (Strings(self[:index]), Strings(self[index:]))
        else:
            return (self, None)
    
    #++
    def rpartition(self, splitter):
        """ Split our data into two parts at a splitter pattern, searching backwards
            
        Args:
            splitter (str): The substring that splits the parts
                
        Returns:
            splitter was found:
                A tuple (body, tail) where body is a Strings object containing the first part,
                and tail is a Strings object containing the second part
            splitter was not found:
                (None, self)
            
        Notes:
            Example: (body, tail) = patch.rpartition('-- ')
        """
        #--
        
        splitter = self._check_string_param('splitter', splitter)
        
        index = self.rfind(splitter)
        if (index != -1):
            return (Strings(self[:index]), Strings(self[index:]))
        else:
            return (None, self)
        
    #++
    def split(self, splitter):
        """ Split our data into two or more parts at occurrences of a splitter pattern
            
        Args:
            splitter (str): The substring that splits the parts
                
        Returns:
            A list of Strings objects, each of which contains a part
            
        Raises:
            StringsParameterError
                    
        Notes:
            Example: diffs = body.split('diff --git ') 
            This code will split the Strings object 'body' into a list of sections,
            each of which starts with a string beginning with ('diff --git ').
        """
        #--
        
        splitter = self._check_string_param('splitter', splitter)
        
        matches = [index for index in range(len(self)) if self[index].lstrip().startswith(splitter)]
        
        parts = []
        
        if (len(matches) > 0):
            parts = []
            if (matches[0] > 0):
                parts += [self.__getslice__(0, matches[0])]
            for index in range(len(matches) - 1):
                parts += [Strings(self[matches[index]: matches[index+1]])]
            if (matches[-1] < len(self)):
                parts += [Strings(self[matches[-1]:])]
        else:
            parts = [Strings(self)]
            
        return parts
        
    #++
    def extract(self, begin, end):
        """ Extract a list of sections tagged by (begin) and (end)
            
        Args:
            begin (str): section start marker
            end   (str): section end marker
            
        Returns:
            A list of Strings objects, one for each extracted section
                
        Notes:
            The begin and end markers are not returned in the output
            
            Example: sections = strlist.extract('#++', '#--')
            This code will extract all strings between '#++' and '#--' in strings.py
            (this file) if the file has been read into strlist.
        
        """
        #--
        
        begin = self._check_string_param('begin', begin)
        end   = self._check_string_param('end', end)
        
        def splitter(begin_, end_):
            start = 0
            for index in range(len(self)):
                string = self[index].strip()
                if (string == begin_):
                    start = index + 1
                elif (string == end_):
                    yield (start, index)
                    
        sections = []
        for (first, last) in splitter(begin, end):
            sections += [Strings(self[first, last])]
            
        return sections
    
    #++
    def discard(self, begin, end):
        """ Remove a list of sections tagged by (begin) and (end)
            
        Args:
            begin (str): section start marker
            end   (str): section end marker
            
        Returns:
            A Strings object.
                
        Notes:
            The begin and end markers are not returned in the output
        """
        #--
        
        strings = Strings()
        state = 0
        for string in self:
            if (state == 0):
                if (string.lstrip().startswith(begin)):
                    state = 1
                else:
                    strings += [string]
            elif (string.lstrip().startswith(end)):
                state = 0
        
        return strings
    
    def ltrim(self, pattern):
        """ Remove text to start of pattern from our strings.
        
        Args:
            pattern (string) splitter pattern
        
        Returns:
            self
        """
        for index1 in range(len(self)):
            string = self[index1]
            index2 = string.find(pattern)
            if (index2 != -1):
                string = string[index2:]
                self[index1] = string
        
        return self
                
    def rtrim(self, pattern):
        """ Remove text beginning with pattern from our strings.
        
        Args:
            pattern (string) splitter pattern
        
        Returns:
            self
        """
        for index1 in range(len(self)):
            string = self[index1]
            index2 = string.find(pattern)
            if (index2 != -1):
                string = string[:index2]
                self[index1] = string
        
        return self
    
    #++
    def sort(self):
        """ Sort our data.
        
        Args:
            none
        """
        #--
        self[:] = sorted(self)
    
        return self # allow method chaining
        
    #++
    def unique(self):
        """ Remove duplicate successive instances of strings in  our data.
        
        Args:
            none
            
        Notes:
            To remove all duplicates, sort the data first
        """
        #--
        uniq_ = []
        for string in self:
            if ((len(uniq_) == 0) or (uniq_[-1] != string)):
                uniq_ += [string]
    
        self[:] = uniq_
    
        return self # allow method chaining

    #++
    @staticmethod
    def join(lists):
        """ Join a list of objects into a single Strings object.
        
            Each object is a list of strings or a Strings object.
            
        Args:
            lists (list): list of list or Strings objects
                
        Returns:
            A Strings object containing all strings in the lists
            
        Raises:
            StringsParameterError
            
        Notes:
            Example:
                list1 = Strings(['a','b'])
                list2 = ['c','d']
                list3 = Strings.join([list, list2])
            This code will join the contents of list1 and list2 in list3.
                
        """
        #--
        
        if ((not isinstance(lists, list)) or (not isinstance(lists[0], list))):
            raise StringsParameterError('lists', lists)
         
        joined = []
        
        for index in range(len(lists)):
            if (isinstance(lists[index], Strings)):
                joined += lists[index]._as_list()
            else:
                joined += lists[index]
                
        return Strings(joined)
    
    def _as_list(self):
        
        return self[:]
            
    def _check_index_param(self, name, value, min_, max_, default):

        if (value is None):
            return default
        
        if (isinstance(value, int)):
            return value
        else:
            raise StringsParameterError(name, value)
        
    def _check_string_param(self, name, value):

        if (self._is_string_type(value) and (len(value) > 0)):
            return value
        else:
            raise StringsParameterError(name, value)
    
    def _is_string_type(self, param):
    
        if _is_python3:
            return isinstance(param, str)
        else:
            return isinstance(param, (str, unicode))