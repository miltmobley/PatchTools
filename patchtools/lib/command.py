# -*- coding: utf-8 -*-
'''
Created on Feb 4, 2014

@copyright 2014, Milton C Mobley

A simple wrapper for the subprocess module.

See the command module section of the documentation for further information.
'''

import subprocess, sys
# 2to3 from types import StringTypes

from patchtools.lib.exceptions import ExceptionHandler                                 
from patchtools.lib.functions  import Functions as ut

class CommandError(Exception):
    def __init__(self, msg):
        super(CommandError, self).__init__(msg)
        self.mod = 'Command'
        
class CommandParameterError(CommandError):
    def __init__(self, name, value):
        s = '%s: invalid %s parameter' % name
        if (value is not None):
            s += ': '
            if (ut.is_string_type(value)):
                s += value
            else:
                s += str(value)
        
        super(CommandParameterError, self).__init__(s)
        
class CommandStateError(CommandError):
    def __init__(self):
        super(CommandStateError, self).__init__('no process is active')
                
#++
class Command(object):
    """ Execute command in subprocess
    """
    #--

    #++
    def __init__(self):
        """ Constructor
          
        Args:
            None
        """
        #--
        self._is_python3 = (sys.version_info[0] >= 3) # 2to3
       
    #++
    def sync(self, cmd):
        """ Execute subprocess synchronously
        
        Args:
            cmd (string): shell command to execute
            cmd (list):   command arguments to pass
                
        Returns:
            A list of strings:
                ['retcode' : 0,
                 'output' : '...',
                 'errors' : '...'
                 ]
                 
        Raises:
            CommandParameterError when command is not a string type
                
        Notes:
            Shell command  is a string like "cd tmp && ls".
            Command arguments is a list like ['gedit', 'file1', file2',...]
            Output and errors strings are only returned to the caller
            when the subprocess returns output or errors.
        """
        #--
        if (ut.is_string_type(cmd)):
            shellmode = True
        elif (isinstance(cmd, (list,tuple))):
            shellmode = False
        else:
            raise CommandParameterError('cmd', cmd)
        
        try:
            self.proc = subprocess.Popen(cmd,
                                         shell=shellmode,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
            bstdout, bstderr = self.proc.communicate()
            retcode = self.proc.returncode
            self.proc.stdout.close()
            self.proc.stderr.close()
            self.proc = None      
            return self._format_result(retcode, bstdout, bstderr)
        except Exception as e:
            raise CommandError(ExceptionHandler.format_exception(e))
        
    #++    
    def async(self, cmd):
        """ Execute subprocess asynchronously
        
        Args:
            cmd (string): shell command to execute
           
        Returns:
            None
            
        Raises:
            see sync method above.
                
        Notes:
            see sync method above. 
        """
        #--
        if (isinstance(cmd, str)):
            shell_mode = True
        elif (isinstance(cmd, (list,tuple))):
            shell_mode = False
        else:
            raise CommandParameterError(self.name, 'cmd', cmd)
        
        try:
            self.proc = subprocess.Popen(cmd,
                                         shell=shell_mode,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        except Exception as e:
            raise CommandError(ExceptionHandler.format_exception(e))
    
    #++    
    def wait(self):
        """ Wait for asynchronous subprocess to exit
        
        Args:
            None
            
        Returns:
            list of result strings
            
        Raises:
            CommandStateError when no subprocess is active    
        """
        #--
        
        if (self.proc is None):
            raise CommandStateError()
        
        try:
            self.proc.wait()
            retcode = self.proc.returncode  
            msgs = self._format_result(retcode, None, None)
            del self.proc
            self.proc = None
            return msgs
        except Exception as e:
            raise CommandError(ExceptionHandler.format_exception(e))
        
    def _format_result(self, code, stdout, stderr):
        ''' Format result into a list of strings.
            Python2.7 returns stdout and stderr as str's ('...'
            Python3.x returns stdout and stderr as bytes (b'...\\xe2...'),
            with characters having ord > 128 escaped to hex.
        '''
        
        msgs = ['retcode: %d' % code]
        if (stdout is not None):
            if (self._is_python3):
                # stdout is a bytearray
                stdout = str(stdout, encoding='utf-8', errors='strict')
                # Replace lsquo char by '
                stdout = stdout.replace('\\xe2\\x80\\x98', "'")
                # Replace rsquo char by '
                stdout = stdout.replace('\\xe2\\x80\\x99', "'")
            msgs += ['stdout: %s' % stdout]
        if (stderr is not None):
            if (self._is_python3):
                # stdout is a bytearray
                stderr = str(stderr, encoding='utf-8', errors='strict')
                stderr = stderr.replace('\\xe2\\x80\\x98', "'")
                stderr = stderr.replace('\\xe2\\x80\\x99', "'")
            msgs += ['stderr: %s' % stderr]
        
        return msgs
    
    
    
    