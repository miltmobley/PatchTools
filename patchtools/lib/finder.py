# -*- coding: UTF-8 -*-
'''
Created on Mar 22, 2014

@copyright 2014, Milton C Mobley

See the finder module section of the documentation for further information.
'''

# 2to3 from types import str

from patchtools.lib.ptobject   import PTObject
from patchtools.lib.exceptions import PT_ParameterError
from patchtools.lib.matcher    import Matcher
from patchtools.lib.functions  import Functions as ut

#++
class Finder(PTObject):
    """ Find references to patterns you specify in a Linux kernel tree,
        a patch archive file, or in a set of patches
    """
    #--

    #++
    def __init__(self, params):
        """ Constructor
            
        Args:
            params (dict): parameters
                root_path   (string, required): path of file tree root
                file_paths  (list, required):   relative paths of files to search
                options (string, optional): display format
                    'terse'    show count of matching lines
                    'compact'  show line numbers of matching lines
                    'full'     show line number and text of matching lines
                    'complete' also show matching pattern
                    'match'    list only matching text
                        default is 'full'
                mode (string, optional) search mode
                    'file' report results by file
                    'pattern' report results by pattern
                
                trim_paths (bool, optional): remove root portion of paths from returned paths
                    default is True
                      
        Raises:
            PT_ParameterError
            PT_NotFoundError
        """
        #--
    
        self.name = 'Finder'
        
        if ((params is None) or (not isinstance(params, dict))):
            raise PT_ParameterError(self.name, 'params')
        
        self.root_path  = self._check_required_string_param(params, 'root_path')
        self._check_path_param('root_path', self.root_path)
        
        self.options = self._check_optional_string_param(params, 'options', 'full')
        if (self.options not in ('full','compact','complete','match','terse')):
            raise PT_ParameterError(self.name, 'options param') 
        self.mode    = self._check_optional_string_param(params, 'mode', 'file')
        
        self.file_paths = self._check_required_param(params, 'file_paths', list)
        self.trim_paths = self._check_optional_param(params, 'trim_paths', bool, True)
        self.debug      = self._check_optional_param(params, 'debug', int, 0)
        
    #++
    def match(self, params):
        """ Report matches by file to (patterns) found in selected files
        
        Args:
            filter (dict): Filter parameters
                
        Returns:
            A list of matches in the format specified above

        Raises:
            PT_ParameterError
                
        Notes:
            See the Filter object for a description of Filter parameters.
        """
        #--
        
        if (not isinstance(params, dict)):
            raise PT_ParameterError(self.name, 'params')
        
        self.matcher = Matcher(params)
        self.matches = {}
    
        if (self.mode == 'file'):
            for path in self.file_paths:
                self._match_files(path)
            matches = self._list_by_file()
        else:
            for path in self.file_paths:
                self._match_pattern(path)
            matches = self._list_by_pattern()
         
        return matches
    
    def _match_files(self, path):
        ''' Search files in self.paths for match to self.matcher.
        '''
        filepath = ut.join_path(self.root_path, path)
        strings = ut.read_strings(filepath)
        for index in range(len(strings)):
            text = strings[index]
            if (self.debug > 1):
                print('   "%s"' % text)
            pattern = self.matcher(text)
            if (pattern is not None):
                if (self.trim_paths):
                    path_ = path
                else:
                    path_ = filepath
                if (path_ not in self.matches):
                    self.matches[path_] = []
                self.matches[path_] += [(pattern, index + 1, text.lstrip())]
    
    def _match_patterns(self, path):
        ''' Search files in self.paths for match to self.matcher. 
        '''
        filepath = ut.join_path(self.root_path, path)
        strings = ut.read_strings(filepath)
        for index in range(len(strings)):
            text = strings[index]
            if (self.debug > 1):
                print('   "%s"' % text)
            pattern = self.matcher(text)
            if (pattern is not None):
                if (self.trim_paths):
                    path_ = path
                else:
                    path_ = filepath
                if (pattern not in self.matches):
                    self.matches[pattern] = []
                self.matches[pattern] += [(path_, index + 1, text.lstrip())]
                        
    def _list_by_file(self):
        ''' List matches by file. self.matches is a dict:
            
                self.matches[path] = [(pattern, number, text),...]
        '''
        strings  = []
        filenames = sorted(self.matches)    # 2to3
        for filename in filenames:
            matches = self.matches[filename] 
            if (self.options == 'compact'):
                strings += self._list_file_compact(filename, matches)
            if (self.options == 'complete'):
                strings += self._list_file_complete(filename, matches)
            elif (self.options == 'terse'):
                strings += self._list_file_terse(filename, matches)
            elif (self.options == 'match'):
                strings += self._list_file_match(filename, matches)
            else: # (self.options == 'full')
                strings += self._list_file_full(filename, matches)
        
        return strings
    
    def _list_file_compact(self, filename, matches):
        ''' Output line is path : list of line numbers
        '''
        numbers = [str(line) for (_, line, _) in matches]
        numbers = ', '.join(numbers)
        
        return [': '.join([filename, numbers])]
                         
    def _list_file_complete(self, filename, matches):
        ''' Output lines are path, line number, text, pattern
        '''
        strings  = []
        for (pattern, line, text) in matches:
            strings += [': '.join([filename, str(line), text, pattern])]
            
        return strings
    
    def _list_file_full(self, filename, matches):
        ''' Output lines are path, line number, text
        '''
        strings  = []
        for (_, line, text) in matches:
            strings += [': '.join([filename, str(line), text])]
            
        return strings
    
    def _list_file_match(self, filename, matches):
        ''' Output lines are path, line number, text
        '''
        strings  = []
        for (_, line, text) in matches:
            strings += [text]
            
        return strings
        
    def _list_file_terse(self, filename, matches):
        ''' Output lines are path, count of line numbers
        '''
        numbers = len(matches)
        
        return [': '.join([filename, str(numbers)])]
                   
    def _list_by_pattern(self):
        ''' List matches by pattern. self.matches is a dict:
            
                self.matches[pattern] = [(path, number, text),...]
        '''
        if (self.options == 'compact'):
            strings = self._pattern_compact()
        elif (self.options == 'terse'):
            strings = self._pattern_terse()
        else: # (self.options == 'full')
            strings = self._pattern_full()
        
        return strings

    def _list_pattern_compact(self):
        ''' Output lines are pattern, count of matching files
        '''
        patterns = sorted(self.matches) # 2to3
        strings  = []
        for pattern in patterns:
            strs = [pattern]
            strs += [str(len(self.matches)) + ' matches found']
            strings += [': '.join(strs)]
        
        return strings
            
    def _list_pattern_full(self):
        ''' Output lines are pattern, path, line number, text
        '''
        patterns = sorted(self.matches) # 2to3
        strings  = []
        for pattern in patterns:
            items = sorted(self.matches[pattern], key=lambda x: x[0])
            for (path, line, text) in items:
                strings += [': '.join([pattern, path, str(line), text])]
                
        return strings
      
    def _list_pattern_terse(self):
        ''' Output lines are pattern, count of matching files
        '''
        patterns = sorted(self.matches) # 2to3
        strings  = []
        for pattern in patterns:
            items = sorted(self.matches[pattern], key=lambda x: x[0])
            for (path, _,_) in items:
                strings += [': '.join([pattern, path])]
                
        return strings
        
