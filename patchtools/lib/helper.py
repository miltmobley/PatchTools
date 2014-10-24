'''
Created on Sep 11, 2014

@copyright 2014, Milton C Mobley

Convenience wrapper for PatchTools classes.
'''

import json

from patchtools.lib.finder     import Finder
from patchtools.lib.checker    import Checker
from patchtools.lib.viewer     import Viewer
from patchtools.lib.walker     import Walker
from patchtools.lib.watcher    import Watcher
from patchtools.lib.patchset   import PatchSet
from patchtools.lib.command    import Command
from patchtools.lib.exceptions import PatchToolsError
from patchtools.lib.functions  import Functions as ut
from patchtools.lib.jsonconfig import JSONConfig

# Items imported above are now in our globals dict. Our callers may reference them
# without re-importing the classes, e.g. by entering "h.Strings()"

class HelperError(PatchToolsError):
    def __init__(self, msg):
        super(HelperError,self).__init__('Error: ' + msg)

class ParametersError(PatchToolsError):
    # NB! Python already defines ParameterError
    def __init__(self, msg):
        super(ParametersError,self).__init__('invalid parameters ' + msg)  

#++
class Helper(object):
    """ Facilitate use of PatchTools's classes
    """
    #--
    
    #++
    def __init__(self, configpath):
        """ Constructor
        
        Args:
            config (dict): configuration data
        """
        #--
        self.config = JSONConfig({ 'filepath' : configpath })
        self.config['defaults'] = {
            'sourcedir' : self.config['sourcedir'],
            'patchdir'  : self.config['patchdir'],
            'patchset'  : self.config['patchset'],
            'tempdir'   : self.config['tempdir'],
            }

    '''
    Wrappers for tools modules.
    '''
    
    #++    
    def cmd(self, command):
        """ Handle Command request
        
        Args:
            command (string) shell command to execute
        """
        #--
        
        def _format_string(prefix, lines):
            
            strings = lines.strip().split('\n')
            strings = [prefix] + ['   ' + string for string in strings]
            
            return strings
        
        ret  = Command().sync(command)
        rlen = len(ret)
        strings = [ret[0]]
        for index in range(1, rlen):
            ret_str = ret[index]
            if (ret_str.startswith('output: ')):
                strings += _format_string('output: ', ret_str[8:])
            elif (ret_str.startswith('errors: ')):
                strings += _format_string('errors: ', ret_str[8:])
        
        return strings
    
    #++                       
    def find(self, patterns, params):
        """ Handle Finder request
            
        Args:
             patterns (dict) Matcher parameters
             params   (dict) Finder parameters 
        """
        #--
        return Finder(params).match(patterns)

    #++
    def check(self, patches, params=None):
        """ Handle Checker request

        Args:
            patches (string/list, required) patch file(s)
            params  (dict, optional) Checker parameters
        """
        #--
        if (params is None):
            params = self.config['defaults']
            
        return Checker(params).match(patches)
    
    #++
    def walk(self, params):
        """ Handle Walker request
            
        Args:
            params (dict, required) Walker parameters
        """
        #--
        return Walker(params).walk()
    
    #++        
    def watch(self, archives, params=None):
        """ Handle Watcher request

        Args:
            archives (string/list)    archive file path(s)
            params   (dict, optional) Watcher parameters
        """
        #--
        if (params is None):
            params = self.config['defaults']
                
        return Watcher(params).watch(archives)
    
    #++ 
    def view(self, files, params=None):
        """ View specified file(s)
        
        Args:
            files  (string/list) file path(s)
            params (dict, optional) Viewer parameters
                
        Notes:
            If params is not specified, the default file viewer is used.
        """
        #--
        return Viewer(params).view(files)
    
    #++   
    def vp2f(self, patchname, params=None):
        """ View patch and the source files it references
        
        Args:
            patchname (string) patch file name
            params    (dict, optional) Viewer parameters
        """
        #--
        return Viewer(params).vp2f(patchname)
    
    #++     
    def vf2p(self, filepath, params=None):
        """ View source file and the patches that reference it
            
        Args:
            filepath (string) file path
            params   (dict, optional) Viewer parameters
        """
        #--
        return Viewer(params).vp2f(filepath)
    
    #++      
    def vp2p(self, patchname, params=None):
        """ View patch and other patches that reference its files
        
        Args:
            patchname   (string) patch name
            params      (dict, optional) Viewer parameters
        """
        #--
        return Viewer(params).vp2p(patchname)
    
    #++
    def vp2a(self, patchname, archivepath, params=None):
        """ View patch and archive diff sections that reference its files:
        
        Args:
            patchname   (string) patch name
            archivepath (string) archive file path
            params      (dict, optional) Viewer parameters
                
        """
        #--
        # Viewer.vp2a will create a temporary file to hold diff sections,
        # so it must wait for the subprocess to exit before destroying the file.
        if (params is None):
            params = { 'wait' : True }
        else:
            params['wait'] = True
    
        return Viewer(params).vp2a(patchname, archivepath)
    
    #++
    def vcpf(self, checkpath, patchname, context=None, params=None):
        """ View Checker output, patch file and the source files it references,
            one at a time.
            
        Args:
            checkpath (string) checker output file path
            patchname (string) patch name
            context   (dict)   source, dir, patchdir, etc.
            params    (dict, optional) Viewer parameters
        
        Notes:
            If context is not passed, config['defaults'] is used.
        """
        #--
        if (context is None):
            context = self.config['defaults']
            
        return Viewer(params).vcpf(checkpath, patchname, context)
    
    '''
    Convenience functions
    '''
    
    #++     
    def load(self, path):
        """ Load data that is formatted as a JSON object coded in a string
        
            Args:
                path (string) file path
        """
        return json.loads(ut.read_file(path))
    
    #++
    def save(self, data, path):
        """ Save data as a JSON object coded in a string
        
            Args:
                data (various) any variable
                path (string) file path
                
            Variables will always be written as JSON objects, but lists will be
            output manually to prevent json.dumps from encoding them as a single
            string without line breaks.
        """
        if (isinstance(data, list)): # pretty print data as JSON
            data = [json.dumps(item) for item in data]
            '''
            for index in range(len(data)):
                item = data[index]
                item = json.dumps(item)
                data[index] = item
            '''
            ut.write_file('[\n' + ',\n'.join(data) + '\n]\n', path)
        else:
            ut.write_file(json.dumps(data) + '\n', path)
    
    #++    
    def read(self, filepath):
        """ Read data from path as a sequence of '\\n' terminated lines.
            Convert the lines to a list of strings
            
            Args:
                filepath (string): file path
            
            Notes:
                This function is used to input data output by the Checker, etc.
        """
        return ut.read_strings(filepath)
    
    #++    
    def write(self, data, filepath):
        """ Write data to path as a sequence of '\\n' terminated lines.
            
            Args:
                data (various): any variable
                filepath (string): file path
            
            Notes:
                All data items are "pretty printed", i.e. they are split into lines
                according to content.
        """
        if (isinstance(data, list)):
            text = '\n'.join(data) + '\n'
        elif (isinstance(data, dict)):
            text = self._format_dict(data)
        elif (ut.is_string_type(data)):
            text = data + '\n'
        ut.write_file(text, filepath)
    
    #++
    def list_patches(self, sel=None, params=None):
        
        if (params is None):
            params = self.config['defaults']
        
        return PatchSet(params).get_patch_names(sel)
    
    #++    
    def list_sources(self, params=None):
        
        if (params is None):
            params = self.config['defaults']
            
        f = { "suffix" : [".c","h",".dts","*.dtsi",".txt"], "prefix": ["Makefile","Kconfig"] }
        p = { "root_path" : params['sourcedir'], "incl_files" : f }
        p1 = self.extend(p, { "incl_dirs" : ["arch/arm/mach-omap2"] })
        p2 = self.extend(p, { "excl_dirs" : [".git","arch","samples","scripts","staging","tools",
                                             "Documentation"] })     
        u = sorted(self.walk(p1))
        #print(len(u))
        v = sorted(self.walk(p2))
        #print(len(v))
        return u + v
        
                      
    '''
    Utility functions
    '''
    
    _MBD = 'argument must be a dict'
    
    #++
    def extend(self, arg1, *rest):
        """ Extend a dict by adding key-value pairs from other dict(s)
        
        Args:
            arg1 (dict)  first dict argument
            rest (tuple) other dict arguments 
        """
        if (not isinstance(arg1, dict)):
            raise TypeError(self._MBD)
        
        # If arg1 was passed as a variable, not a dict literal, we should extend a copy
        t = arg1.copy()
        
        for arg in rest:
            if (isinstance(arg1, dict)):
                for key in arg:
                    t[key] = arg[key]
            else:
                raise TypeError(self._MBD)
            
        return t
        
    def _echo_str(self, string):
        
        print(string)
        
    def _echo_strs(self, strings):
        
        for string in strings:
            print(string)
    
    def _format_dict(self, result):
        ''' If the dict will fit on one line, just print it.
            Otherwise, recurse on each key-value pair.
        '''
        
        string = str(result)
        if (len(string) <= 72):
            return [string]
        
        keys = sorted(result) # +2to3
        #keys = .keys()
        #keys.sort()
        strings = ['{']
        for key in keys:
            val = result[key]
            if (isinstance(val, int)):
                strings += ['   "%s" : %d' % (key, val)]
            elif (ut.is_string_type(val)):
                val = val.rstrip(' \t\n')
                keystr = '   "%s" : ' % key
                if ('\n' in val):
                    strs = val.split('\n')
                    strs = [('      ' + astr.strip()) for astr in strs]
                    strings += [keystr] + strs
                else:
                    strings += [keystr + val]
            elif (isinstance(val, dict)):
                strings += self._format_dict(val)
            else:
                strings += ['   "%s" : %s' % (key, str(val))]
        strings += ['}']
        
        return strings
            
    def _format_list(self, result):
        ''' If the list will fit on one line, just print it.
            Otherwise, recurse on each list item, which may be a dict.
        '''

        string = str(result)
        if (len(string) <= 72):
            return [string]
        
        strings = []
        for item in result:
            strings += self._format_result(item)
        
        return strings
    