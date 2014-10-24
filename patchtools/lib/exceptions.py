# -*- coding: utf-8 -*-
'''
Created on Apr 10, 2014

@copyright 2014, Milton C Mobley

PatchTools exception classes and exception handler
'''
import traceback

from patchtools.lib.functions import Functions as ut

class PatchToolsError(Exception):
    def __init__(self, mod, msg):
        super(PatchToolsError, self).__init__(msg)
        self.mod = mod

class PT_NotFoundError(PatchToolsError): # file not found, etc.
    def __init__(self, mod, msg):
        super(PT_NotFoundError, self).__init__(mod, 'not found: %s' % msg)
        
class PT_ParameterError(PatchToolsError):
    def __init__(self, mod, name, value=None):
        s = '%s: invalid %s parameter' % (mod, name)
        if (value is not None):
            s += ': '
            if (ut.is_string_type(value)):
                s += value
            else:
                s+= str(value)
        super(PT_ParameterError, self).__init__(mod, s)

class PT_TypeError(PatchToolsError):
    def __init__(self, mod, item, types):
        super(PT_TypeError, self).__init__(mod, '%s must be of type %s' % (item, types))
                
class PT_OperationalError(PatchToolsError):
    def __init__(self, mod, msg):
        super(PT_OperationalError, self).__init__(mod, 'operational error: "%s"' % msg)
        
class PT_ProgrammingError(PatchToolsError):
    def __init__(self, mod, msg):
        super(PT_ProgrammingError, self).__init__(mod, 'programming error: "%s"' % msg)

class PT_UndefinedError(PatchToolsError): # item is undefined
    def __init__(self, mod, msg):
        super(PT_UndefinedError, self).__init__(mod, '%s is undefined' % msg)
        
#++
class ExceptionHandler(object):
    """ Handle exceptions
    """
    #--

    #++    
    def __init__(self, params=None):
        """ Constructor
        
        Args:
            params (dict): parameters
                trace (bool, optional): format exception traceback
                    default is True
                print (bool): print results
                    default is True
        """
        #--
        self.do_trace = True
        self.do_print = True
        if (isinstance(params, dict)):
            if ('trace' in params):
                option = params['trace']
                if (isinstance(option, bool)):
                    self.do_trace = option
            if ('print' in params):
                option = params['print']
                if (isinstance(option, bool)):
                    self.do_print = option
            
    def __call__(self, e):
        
        if (self.do_trace):
            data = self._format_traceback(e)
        else:
            data = [self.format_exception(e)]
        if (self.do_print):
            for string in data:
                print(string)
        else:
            return data
            
    def _format_traceback(self, e):
        
        tb = traceback.format_exc().split('\n')
        if (isinstance(e, PatchToolsError)):
            last = tb[-2]
            index = last.find(':') + 2
            tb[-2] = last[index:]
        
        return tb
    
    @classmethod    
    def format_exception(cls, e):
        
        if (hasattr(e, 'mod')): # PatchToolsError, StringsError, CommmandError, JSONConfigError
            msg  = e.mod + ': ' + str(e)
        
        else: # any other exception
            # str(e) does not include the exception name
            text = str(e)
            name = str(e.__class__)
            # name is e.g. "type: <class 'patchtools.lib.jsonconfig.JSONConfigSyntaxError'>"
            index = name.rfind("'")
            name  = name[:index]
            index = name.rfind(".")
            name  = name[index+1:]
            msg   = name + ': ' + text
        
        return msg
    
        