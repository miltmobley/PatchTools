'''
Created on Sep 25, 2014

@copyright 2014, Milton C Mobley
'''

from patchtools.lib.exceptions import PT_ParameterError, PT_TypeError
from patchtools.lib.functions  import Functions as ut

#++
class PTObject(object):
    """ PatchTools super class
    
    Provides an identifiable super class for all PatchTools classes.
    Implements common parameter checking functions for the sub classes.
    """
    #--
    
    def _check_required_param(self, params, field, types):

        if (field in params):
            param = params[field]
            if (isinstance(param, types)):
                return param
            else:
                PT_TypeError(self.name, field, types)
        else:    
            raise PT_ParameterError(self.name, field)

    def _check_required_string_param(self, params, field):

        if (field in params):
            param = params[field]
            if (ut.is_string_type(param)):
                return param
            else:
                raise PT_TypeError(self.name, field, 'str')
        else:
            raise PT_ParameterError(self.name, field)
            
    def _check_optional_param(self, params, field, types, default):

        if (field in params):
            param = params[field]
            if (isinstance(param, types)):
                return param
            else:
                raise PT_TypeError(self.name, field, str(types))
        else:
            return default

    def _check_optional_string_param(self, params, field, default):

        if (field in params):
            param = params[field]
            if (ut.is_string_type(param)):
                return param
            else:
                raise PT_TypeError(self.name, field, 'str')
        else:
            return default
        
    def _check_path_param(self, name, value):
        
        if (not ut.is_dir(value)):
            raise PT_ParameterError(self.name, name, value)