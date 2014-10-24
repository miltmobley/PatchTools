# -*- coding: utf-8 -*-
"""
Created on Feb 3, 2014

@copyright 2014, Milton C Mobley

Utility functions. Note that functions other than file_exists and is_dir
do not wrap requests in try..except blocks to allow callers to decide how
to handle exceptions.

This is the only module in PatchTools that has knowledge of the host operating system.
"""

import os, sys, io
from platform import system
# 2to3 from types    import StringTypes
            
_is_windows = ("Windows" in system())
_is_python3 = (sys.version_info[0] >= 3) # 2to3

'''
Text extracted from patches and source files may contain characters
with ordinal codes > 127 (unicode values > U+00FF).
'latin-1' encoding handles most of them
'''

def _join_unix_path(head, tail):
    
    return os.path.join(head, tail)

def _join_win_path(head, tail):
    
    return os.path.join(head, tail).replace('/','\\')

if _is_windows:
    _join_path = _join_win_path
else:
    _join_path = _join_unix_path

#++     
class Functions(object):
    """ Utility functions
    
    Linux source files and patches that describe them may contain byte values
    that are legal 'Latin-1' (aka ISO-8859-1) character codes, but not legal
    'UTF-8' start bytes. For example, 0xb3 is the 'Latin-1' character for the
    cube symbol, i.e. a superscript 3. For this reason the file access functions
    below default to the 'latin_1' encoding.
    """
    #--
    
    #++
    @staticmethod
    def is_windows():
        """ Report whether the host system is Windows
        
        Args:
            None
        
        Returns:
            True if running on Windows, else False
        """
        #--
        return _is_windows

    #++
    @staticmethod
    def is_python3():
        """ Report whether the Python version is >= 3
        
        Args:
            None
        
        Returns:
            True if running on Python 3, else False
        """
        #--
        return _is_python3
    
    """
    File and directory functions
    """

    #++
    @staticmethod
    def file_size(path):
        """ Determine size of the file/folder at (path)
        
        Args:
            path (string): file path
        
        Returns:
            size (int): file size in bytes
        """
        #--     
        try:
            return os.stat(path).st_size
        except OSError:
            return None

    
        
        
        '''
        try:
            inpt = io.open(path, "r", encoding='UTF-8', errors='strict')
            data = inpt.read(min(prefix, os.stat(path).st_size))
            inpt.close()
            return False
        except Exception as e:
            print(str(e))
            return True
        '''

    #++
    @staticmethod
    def is_dir(path):
        """ Determine whether the object at (path) is a directory
        
        Args:
            path (string): file path
        
        Returns:
            True if the path exists and is a directory.
        """
        #--
        return (Functions.is_string_type(path) and os.path.exists(path) and os.path.isdir(path))

    #++
    @staticmethod
    def is_file(path):
        """ Determine whether the object at (path) is a file
        
        Args:
            path (string): file path
        
        Returns:
            True if the path exists and is a regular file.
        """
        #--
        return (Functions.is_string_type(path) and os.path.exists(path) and os.path.isfile(path))

    #++
    @staticmethod
    def join_path(head, tail):
        """ Form a path from (head) and (tail).
        
        Args:
            head (string): path prefix
            tail (string): path suffix
        
        Returns:
            string: the resulting path
        
        Notes:
            This function allows head and tail to contain embedded '/' characters.
        """
        #--
        if (len(head) > 0):
            return _join_path(head, tail)
        else:
            return tail

    #++
    @staticmethod
    def trim_path(head, path):
        """ remove (head) from (path.
        
        Args:
            head (string): path prefix
            path (string): path
        
        Returns:
            string: the resulting path
        
        """
        #--
        index = len(head)
        if (not head.endswith('/')):
            index += 1
        
        return path[index:
                    ]
    #++
    @staticmethod
    def read_file(path, enc='latin_1'):
        """ Read file data.
        
        Args:
            path (string): file path
        
        Returns:
            File data as a single object.
        """
        #--
        if _is_windows:
            path = path.replace('/','\\')  
        inpt = io.open(path, "r", encoding=enc, errors='strict') 
        data = inpt.read()
        inpt.close()
      
        return data

    #++
    @staticmethod
    def read_lines(path, enc='latin_1'):
        """ Read file lines.
        
        Args:
            path (string): file path
        
        Returns:
            File data as a list of '\n' terminated strings.
        """
        #--
        if _is_windows:
            path = path.replace('/','\\')
        inpt = io.open(path, "r", encoding=enc, errors='strict') 
        data = inpt.readlines()
        inpt.close()
    
        return data

    #++
    @staticmethod
    def read_strings(path, enc='latin_1'):
        """ Read file strings.
        
        Args:
            path (string): file path
        
        Returns:
            File data as a list of strings.
        """
        #--
        if _is_windows:
            path = path.replace('/','\\')
        inpt = io.open(path, "r", encoding=enc, errors='strict') 
        data = inpt.readlines()
        inpt.close() 
    
        return [string.rstrip('\n') for string in data]

    #++
    @staticmethod
    def write_file(text, path, enc='latin_1'):
        """ Write text to file at path
        
        Args:
            path (string): file path
        
        Returns:
            None
        
        """
        #--
        if _is_windows:
            path = path.replace('/','\\') 
        oupt = io.open(path, "w", encoding=enc, errors='strict')
        if (not _is_python3):
            text = unicode(text)
        oupt.write(text)
        oupt.close()

    #++
    @staticmethod
    def write_strings(strings, path, enc='latin_1'):
        """ Write strings to file at(path)
        
        Args:
            path (string): file path
        
        Returns:
            None
        
        Notes:
            If (strings) intentionally has empty strings, using str.join() would
            delete them, which may cause problems for readers of the file.
            Here we write the strings one at a time.
        """
        #--
        if _is_windows:
            path = path.replace('/','\\')
        oupt = io.open(path, "w", encoding=enc, errors='strict') 
        for string in strings:
            if (not _is_python3):
                string = unicode(string)
            oupt.write(string + '\n')
        oupt.close()
        
    """
    Patch related functions
    """

    #++
    @staticmethod                    
    def get_string_filename(string):
        """ Extract filename from string
        
        Args:
            string (string): input string
        
        Returns:
            filename (string): filename substring
        
        Notes:
            Supported string formats:
                In patches:
                    'diff --git a/foo... b/foo...'
                    'diff -u -R -n foo... foo...'
                    '--- foo...'
                    '+++ foo...
                In a Checker output file:
                    'DIFF: diff --git a/arch/powerpc/mm/numa.c b/arch/powerpc/mm/numa.c'
        """
        #--
        string = Functions.normalize_string(string)
    
        # Skip leading 'DIFF' text
        if (string.startswith('DIFF ')):
            index = string.find(' ')
            string = string[index + 1:]
    
        if (string.startswith('diff -')):
            words = string.split(' ')
            index = 2
            while (words[index].startswith('-')):
                index += 1
            filename = words[index]
            if (filename.startswith('a/')):
                filename = filename[2:]
    
        elif (string.startswith('--- ') or string.startswith('+++ ')):
            filename = string[4:]
    
        else:
            filename = None
           
        return filename

    #++
    @staticmethod   
    def normalize_string(string, strip=True):
        """ Replace all internal string whitespace by single spaces
        
        Args:
            string (string): input string
            strip  (bool):   True = strip the string first
        """
        #--
    
        if (strip):
            string = string.strip()
            string = string.replace('\t', ' ')
        while ('  ' in string):
            string = string.replace('  ', ' ')
        
        return string

    #++
    @staticmethod
    def string_to_words(string):
        """ Split a string into words on space boundaries.
        
        Args:
            string (string): input string
        
        Notes:
            After splitting, words are stripped of whitespace and empty words
            are removed.
        """
        #--
        words = string.strip(' \t\n\f').split(' ')
        words = [word.strip(' \t') for word in words]
        words = [word for word in words if len(word) > 0]
    
        return words

    #++
    @staticmethod
    def is_string_type(param):
        """ Determine if an object is a string
        
        Args:
            param (unknown): input object
        
        Returns:
            True if the object is a string, else False
        
        Notes:
            Python2 has str, unicode and StringTypes, while Python3
            has only str.
        """
        #--
        if _is_python3:
            return isinstance(param, str)
        else:
            return isinstance(param, (str, unicode))