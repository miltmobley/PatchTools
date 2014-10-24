# -*- coding: utf-8 -*-
'''
Created on Oct 17, 2013

@copyright 2014, Milton C Mobley

The module defines it own exceptions and implements some utility functions,
since the code may be useful in other projects. See the jsonfig module section
of the documentation for further information.
'''

import json
# 2to3 from types import StringTypes
import os, sys

class JSONConfigError(Exception):
    def __init__(self, msg):
        super(JSONConfigError, self).__init__(msg)

class JSONConfigSyntaxError(JSONConfigError):
    def __init__(self, msg):
        super(JSONConfigSyntaxError, self).__init__(msg)
        
class JSONConfigNotFoundError(JSONConfigError):
    def __init__(self, msg):
        super(JSONConfigNotFoundError, self).__init__(msg)
        
class JSONConfigTypeError(JSONConfigError):
    def __init__(self, name, type_):
        super(JSONConfigTypeError, self).__init__('%s must have type %s' % (name, type_))

class JSONConfigKeyError(JSONConfigError):
    def __init__(self, msg):
        super(JSONConfigKeyError, self).__init__(msg)  
        
class JSONConfigParameterError(JSONConfigError):
    def __init__(self, msg):
        super(JSONConfigParameterError, self).__init__(msg) 
                      
#++
class JSONConfig(dict):
    """ Store configuration data obtained from enhanced JSON input files
    """
    #--
    
    #++
    def __init__(self, params=None):
        """ Constructor
        
        Args:
            params (dict, optional): parameters
                filepath  (string, required): path to file with enhanced JSON encoded string, or None
                separator (string, optional): char to use as separator in path expressions
                    default is '/'
                
        Raises:
            JSONConfigParameterError
        """
        #--
 
        super(JSONConfig, self).__init__()
        self._separator  = '/'
        self._is_python3 = (sys.version_info[0] >= 3) # 2to3
        
        if (params is not None):
            if (not isinstance(params, dict)):
                raise JSONConfigParameterError('params')
            
            if ('separator' in params):
                if (self._is_string_type(params['separator'])):
                    self._separator = params['separator']
                                
            if ('filepath' in params):
                filepath = params['filepath']
                if (not self._is_string_type(filepath)):
                    raise JSONConfigParameterError('filepath')
                if (not os.path.isfile(filepath)):
                    raise JSONConfigNotFoundError(filepath)
                self._load_file(filepath) 
    
    #++
    def __getitem__(self, key):
        """ Ensure that a slice of our data is returned as a str object,
            when the value is a unicode string, on Python2.x
            
        Args:
            k (str/unicode):   item index
            
        Returns:
            str(value) when Python is 2.x and value is unicode
            otherwise, value
            
        Raises:
            JSONConfigTypeError, JSONConfigKeyError
        """
        #--
        if (not self._is_string_type(key)):
            raise JSONConfigTypeError('key', 'string')
        
        if (key not in self):
            raise JSONConfigKeyError(key)
            
        value = super(JSONConfig, self).__getitem__(key)
        
        if (not self._is_python3):    # 2to3
            if (isinstance(value, unicode)):    
                value = str(value)
            
        return value
      
    #++                                         
    def get(self, key):
        """ Get top level value or internal value
        
        Args:
            key (string): path to internal value
                        
        Returns:
            The value addressed by key
            
        Raises:
            JSONConfigTypeError, JSONConfigKeyError
            
        Notes:
            The key argument may be the name of a top level key in the data, or a "path expression".
            Such an expression contains one or more instances of '/' or of a user defined separator,
            and encodes a path to a node in the dict.
            For example, self.get("/mysql_options/admin_profile/data_base") will get the value at
                self["mysql_options"]["admin_profile"]["data_base"]
                
            Values may also be accessed by normal Python indexing of the dict superclass.
        """
        #--
        
        if (not self._is_string_type(key)):
            raise JSONConfigTypeError('key', 'string')
        
        if (self._separator in key): # key is a path to an internal node
            value = self._get_via_path(key) # raises KeyError if any part of path not found
            
        else: # key is a top level node
            try:
                value = self[key]
            except KeyError:
                raise JSONConfigKeyError(key)
        
        if (not self._is_python3):    # 2to3
            if (isinstance(value, unicode)):    
                value = str(value)
            
        return value
    
    #++        
    def set(self, key, value):
        """ Set top level value or internal value
        
        Args:
            key   (string): path to internal value
            value (any Python value)
                
        Returns:
            None
            
        Raises:
            JSONConfigTypeError, JSONConfigKeyError
            
        Notes:
            See notes for get method.
        """
        #--
          
        if (not self._is_string_type(key)):
            raise JSONConfigTypeError('key', 'string')
        
        if (self._separator in key): # key is a path to an internal node
            self._set_via_path(key, value)
        
        else: # key is a top level node
            self[key] = value
        
        return True
        
    #++    
    def add(self, data):
        """ Add data to the current config
        
        Args:
            data (choice):
                A string path to a file to load
                A string representation of a JSON object
                A Python dict
        
        Returns:
            None
            
        Raises:
            OSError or IOError when a file has problems
            JSONConfigTypeError, etc, when JSON string is incorrectly formatted
        """
        #--
        
        if (isinstance(data, dict)):
            self._add_dict_data(data)    
        elif (self._is_string_type(data)):
            if (data.startswith('{')): # Assume it's a string JSON object
                self._add_str_data(data)
            else:
                self._add_file_data(data)
    
    #++            
    def has(self, key):
        """ Determine if item is in the config data
        
            Args:
                key (string): path to internal value
            
            Returns:
                True if item was found, else False
        """
        #--
        try:
            self.get(key)
            return True
        except JSONConfigKeyError:
            return False
            
    def _get_via_path(self, path, default=None):
        ''' Get an internal node by traversing the path argument. If any node
            it names does not exist, KeyError is raised. Internal targets may be
            dicts or lists, but only dicts can have their own internal nodes.
        '''
        atoms  = path.split(self._separator)
        target = self
        for index in range(len(atoms)):
            if (atoms[index] in target):
                if (isinstance(target, dict)):
                    target = target[atoms[index]]
                elif (isinstance(target, list)):
                    target = atoms[index]
                    break
                else:
                    raise JSONConfigTypeError(str(atoms[index]))
            else:
                raise JSONConfigKeyError(atoms[index])
                
        return target
            
    def _set_via_path(self, path, value):
        ''' Set an internal node by traversing the path argument. If any node
            it names does not exist, KeyError is raised.
        '''
        atoms = [atom.strip(' ') for atom in path.split(self._separator)]
        alen  = len(atoms)
        
        if (alen == 1):
            self[atoms[0]] = value
            
        elif (alen == 2):
            self[atoms[0]][atoms[1]] = value
            
        elif (alen == 3):
            self[atoms[0]][atoms[1]][atoms[2]] = value
            
        else:
            raise JSONConfigParameterError('too many levels for set request')
        
    def _load_file(self, config_file):
        ''' Load JSON config file, which may have line or block comments.
            Remove the comments and blank lines. Convert the remaining lines
            to a dict and add its contents to the object.
        '''
        inpt   = open(config_file, "r") # 
        lines  = inpt.readlines()
        inpt.close()
        lines, numbers = self._strip_lines(lines)
        # Now numbers has the original line numbers (1-based) of the lines that
        # were not stripped.
        text = '\n'.join(lines)
        try:
            data = json.loads(text)
            self.update(data)
        except Exception as e:
            excstr = str(e)
            # If the exception msg has a line number, convert it to the unstripped value
            index1 = excstr.find(' line ') 
            if (index1 != -1):
                index1 += 6 # start of line number
                index2 = excstr.find(' ', index1 + 1) # end of line number
                number = int(excstr[index1:index2])
                number = numbers[number - 1]
                string = excstr[:index1] + str(number) + excstr[index2:]
                raise JSONConfigSyntaxError(string)
            else:
                raise e
    
    def _strip_lines(self, lines):
        ''' Remove line and block comments and blank lines. Generate line numbers for
            non comment lines. Note that JSON exception reports use 1-based line numbers.
        '''
        lines2 = []
        numbers = []
        state  = 0
        for index in range(len(lines)):
            line  = lines[index]
            line2 = line.lstrip(' \t').rstrip(' \t\n')
            if (state == 0): # not in a block comment
                if (line2 == '"""'):
                    state = 1
                elif ((not line2.startswith('#')) and (len(line2) > 0)):
                    lines2  += [line2]
                    numbers += [index + 1]
                # else ignore blank or # comment line
            else: # state = 1, in a block comment
                if (line2 == '"""'):
                    state = 0
                
        return lines2, numbers
    
    def _is_string_type(self, param):
        ''' Copied here to eliminate dependency on functions.py
        '''
    
        if (self._is_python3):
            return isinstance(param, str)
        else:
            return isinstance(param, (str, unicode))