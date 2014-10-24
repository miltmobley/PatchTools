# -*- coding: utf-8 -*-
'''
Created on Apr 13, 2014

@copyright 2014, Milton C Mobley

Select strings based on caller components: prefixes, suffixes and substrings.
Regular expression matching is also supported.

Note that some patch and kernel files have utf-8 chars with code > 127. Some of
these codes are not legal utf-8 start byte codes. See functions.py for the file
 read, write handling.
'''

import re
from inspect import isfunction

from patchtools.lib.ptobject   import PTObject
from patchtools.lib.exceptions import PatchToolsError, PT_ParameterError

#++
class Matcher(PTObject):
    """ Implement filter selection of strings
    """
    #--

    #++
    def __init__(self, params):
        """ Constructor
          
        Args:
            params (dict): parameters
                match    (list, optional): string match pattern(s)
                prefix   (list, optional): string start pattern(s)
                suffix   (list, optional): string end pattern(s)
                substr   (list, optional): substring pattern(s)
                regexp   (list, optional): regular expression pattern(s)
                funcs    (list, optional): callback function(s)
            
        Raises:
            PT_ParameterError on invalid parameters
                
        Notes:
            At least one option must be specified for the filter to have an effect.         
            Regular expression pattern strings should be coded using the r"..." string form.
        """
        #--

        self.name = 'Matcher'
        
        if (not isinstance(params, dict)):
            raise PT_ParameterError(self.name, 'params')
         
        self.prefix_patterns = self._check_optional_param(params, 'prefix', list, None)      
        self.suffix_patterns = self._check_optional_param(params, 'suffix', list, None)
        self.substr_patterns = self._check_optional_param(params, 'substr', list, None)
        self.match_patterns  = self._check_optional_param(params, 'match',  list, None)
        regexp = self._check_optional_param(params, 'regexp', list, None)
        
        if (isinstance(regexp, list)):
            try:
                self.regex_patterns = [re.compile(s) for s in regexp]
            except Exception as e:
                raise PT_ParameterError(self.name, str(e))
        else:
            self.regex_patterns = None
        
        if ('funcs' in params):
            cbs = params['funcs']
            for cb in cbs:
                if (not isfunction(cb)):
                    raise PatchToolsError(self.name, 'callback must be a function')
            self.callbacks = cbs
        else:
            self.callbacks = None
                   
    #++   
    def __call__(self, string):
        """ Try to match string to stored filter
            
        Args:
            string (string): string to match
            
        Returns:
            text of the matching pattern, or None
        """
        #--
        
        if ('compatible = "ti,am3359-tscadc"' in string):
            pass
        
        if (self.match_patterns is not None):
            for pattern in self.match_patterns:
                if (string == pattern):
                    return pattern
                
        if (self.prefix_patterns is not None):
            for pattern in self.prefix_patterns:
                if (string.startswith(pattern)):
                    return pattern
        
        if (self.suffix_patterns is not None):
            for pattern in self.suffix_patterns:
                if (string.endswith(pattern)):
                    return pattern
        
        if (self.substr_patterns is not None):
            for pattern in self.substr_patterns:
                if (pattern in string):
                    return pattern
         
        if (self.regex_patterns is not None):
            for pattern in self.regex_patterns:
                ret = pattern.match(string)
                if (ret is not None):
                    return str(pattern)
        
        if (self.callbacks is not None):
            for callback in self.callbacks:
                ret = callback(string)
                if (ret is not None):
                    return str(callback)
  
        return None