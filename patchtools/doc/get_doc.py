#! /usr/bin/env python
'''
Created on Mar 30, 2014

@author: Milton C Mobley

For each py file:
    extract the api docs sections
    reformat them for REST
    concatenate the docs sections into a single file section
    concatenate the file sections into a single file (api.rst)
    
For each file, the extracted sections are:
(1) a classdoc section in which the first line begins with 'class'
(2) one or more public method sections, in which the first line begins with 'def'

The REST syntax used in Python docs is fairly restrictive. Indentation and blank lines
must be carefully controlled, and tabs are not allowed.

Target markup:

API
...

   class Command(object):
   
      Wrapper for subprocess module
    
      def run(self, command):

         Execute subprocess synchronously
        
         Args
            command (str):  The shell command to use.
           
         Returns
            dict:
                code (int) code returned by Popen
                    0 -- Success!
                    >0 -- No good.
               
                output (string) output returned by Popen
                errors (string) errors returned by Popen 

         Raises
            OSError, ValueError (from Popen)
    
         Notes
            The code is adapted from the mq_patches_applied function in Python's
            Tools/ccbench/patchcheck.py.
            
indent level 0 = ''
indent level 1 = 3 * ''
'''

import os

from patchtools.lib.jsonconfig import JSONConfig
from patchtools.lib.strings    import Strings
from patchtools.lib.functions  import Functions as ut

def merge_files(config):

    oupt = open("./_rest/manual.rst", "w")
    for module in config['manual']:
        print('merge: ' + module)
        filepath = os.path.join("./_rest", module)
        inpt = open(filepath, "r")
        oupt.write(inpt.read())
        inpt.close()
    oupt.close()
    
    
IND1 = 4  * ' '
IND2 = 8  * ' '
IND3 = 12 * ' '
IND4 = 16 * ' '

def trim(strings):
    ''' Remove blank/empty strings from front of list
    '''
    pass

def rtrim(strings):
    ''' Remove blank/empty strings from back of list
    '''
    pass

def conv_class_section(strings):
    ''' Convert, e.g:
    
        class Foo(PTObject):
            """ summary
            
            description
            """\n
    '''
    global class_name
    
    # Get class name string from e.g. 'class Finder(PTObject):'
    class_name = strings.pop(0)
    class_name = class_name[6: class_name.find('(')]
    
    head  = ['']
    title = class_name
    head += [title]
    head += [len(title) * '-']
    head += ['']
    
    if (len(strings) > 0):
        # Convert body of docstring
        strings[0] = strings[0].replace('"""','')
        strings.pop(-1)
        body = [string.lstrip() for string in strings]
    else:
        body = []
    
    return Strings(head + body + [''])

def conv_method_section(strings):
    ''' Convert, e.g:
    
        def __getitem__(self, params):
            """ summary
            
            description
                
            Args:
                foo (type) description
                    Default is ...
                ...
            
            Returns:
                ...
                
            Raises:
                ...
            
            Notes:
                ...
            """\n
    '''
    global class_name
    
    if (class_name == 'Archive'):
        pass
    
    # Get method name string
    name_str = strings.pop(0).lstrip().rstrip(' \t:')
    
    # Remove 'def', '(self, ', etc.
    name_str = name_str.replace('def ','')
    name_str = name_str.replace('(self)','()')
    name_str = name_str.replace('self, ','')
    if (name_str.startswith('__init__')):
        name_str = class_name + name_str[len('__init__'):]
    underline = len(name_str) * '.'
    
    body = conv_method_body(strings, 8, 8)
    
    return Strings([name_str, underline, ''] + body + [''])

def conv_decorated_section(strings):
    ''' Convert, e.g:
    
        @classmethod
        def name(cls, params):
            """ summary
                
            Args:
                foo (type) description
                    Default is ...
                ...
            
            Returns:
                ...
                
            Raises:
                ...
            
            Notes:
                ...
            """\n
    ''' 
    deco_str = strings.pop(0).lstrip(' \t@').rstrip(' \t')
    if ('write_file' in strings[0]):
        pass
    
    strings = conv_method_section(strings)
    strings[0] += (' <' + deco_str + '>')
    strings[1] += ((len(deco_str) + 3) * '.')
    
    return strings
            
def conv_method_body(strings, old_indent, new_indent):
    ''' Convert to REST format, e.g.
        """ summary
            
            description
                
        Args:
            ...
            
        Returns:
            ...
                
        Raises:
            ...
            
        Notes:
            ...
        """\n
        
        Split the strings into a head and a body at 'Args:'
        Unindent the head section
        Adjust the indentation of the body section
    '''

    # lstrip first line of docstring
    strings[0] = strings[0].replace('"""','')
    
    # remove the last line ('   """')
    strings.pop(-1)
    
    # remove blank lines from tail of docstring
    strings.rstrip()
   
    (head, body) = strings.partition('Args:')
    
    head = [string.strip() for string in head]
    head = [string.strip() for string in head if len(string) > 0]
    if (len(head) > 0):
        head += ['']
    
    if (body is not None):
        body.lstrip().rstrip()
        delta = new_indent * ' '
        body = ['|' + delta + string[old_indent:] for string in body]
    else:
        body = []
    
    return head + body
    
def conv_section(strings):
    
    # First, check for format errors
    for string in strings:
        if (string.strip() in ('#++','#--')):
            print('Format error:')
            print('   ' + strings[0])
            print('   ' + strings[1])
            exit(-1)
            
    string = strings[0].strip()
    
    if (string in ('@staticmethod','@classmethod')):
        strings = conv_decorated_section(strings)

    elif (string.startswith('class')):
        strings = conv_class_section(strings)
    
    else:   
        strings = conv_method_section(strings)
        
    return strings
    
def check_config(srcroot, docroot, modules):
    """ Check the configuration
    """
    errors = 0
    
    # Do all the Python/REST source files exist?
    for module in modules:
        
        # Python modules have a Python source file and a .rst docs file
        if (isinstance(module, list)):
            path = os.path.join(srcroot, module[1])
            if (not ut.is_file(path)):
                print("check_config: %s not found" % path)
                errors += 1
            path = os.path.join(docroot, module[0])
            if (not ut.is_file(path)):
                print("check_config: %s not found" % path)
                errors += 1
        else:
            # REST modules have only an .rst file
            path = os.path.join(docroot, module)
            if (not ut.is_file(path)):
                print("check_config: %s not found" % path)
                errors += 1
            
    return errors
                            
def convert_api_data(config):

    srcroot = config['srcroot']
    sources = config['sources']
    data = []
    for source in sources:
        print('extract: ' + source)
        path = ut.join_path(srcroot, source)
        strings  = Strings(ut.read_strings(path))
        sections = strings.extract('#++','#--')
        if (len(sections) > 0):
            sections = [conv_section(section) for section in sections]
            data += Strings.join(sections)
        else:
            pass
    
    ut.write_strings(data, './_rest/api.txt')

if __name__ == '__main__':
    
    config = JSONConfig({ 'filepath' : 'doc_config.json' })
    convert_api_data(config)
    merge_files(config)
    