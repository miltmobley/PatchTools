# -*- coding: utf-8 -*-
'''
Created on Apr 14, 2014

@copyright 2014, Milton C Mobley

Analyze patchset description and the patches it describes.

Notes on patch set formats:

In an early version of eLinux patch sources, groups were defined to control
the processing order, and each patch file was listed in a group by a path
relative to the root of the patches folder. We regarded the relative path
as the "name" of a patch.

In the "kernel-3.8" version, the number of groups and patches has greatly increased,
and the patches are no longer listed in the desription. The shell script that applies
the patches enumerates the files by walking the group directories in group order and
sorting the filenames the groups contain. We assume the patch filenames will still
enforce correct order in applying the patches.
'''

import os
from datetime import datetime
# 2to3 from types import StringTypes

from patchtools.lib.ptobject   import PTObject
from patchtools.lib.exceptions import PT_ParameterError, PT_NotFoundError
from patchtools.lib.functions  import Functions as ut

#++
class PatchSet(PTObject):
    """ Extract information from a set of patch files
    """
    #--
    
    #++
    def __init__(self, params):
        """ Constructor
        
        Args:
            params (dict):  parameters
                patchdir  (string, required): path to patch directory
                patchset  (dict, required):   description of patches in patchdir
            
        Raises:
            PT_ParameterError     
        """
        #--
       
        self.name = 'PatchSet'
        
        if ((params is None) or (not isinstance(params, dict))):
            raise PT_ParameterError(self.name, 'params')
        
        self.patchdir = self._check_required_string_param(params, 'patchdir')
        self.patchset = self._check_required_param(params, 'patchset', dict)
        groups = self.patchset['groups']
        if (groups[0] in self.patchset): # old format
            self.format = 'old'
        else:
            self.format = 'new'
        self.filedata  = None                
        self.patchdata = None
    
        self.month_numbers = {
            'Jan' : 1,
            'Feb' : 2,
            'Mar' : 3,
            'Apr' : 4,
            'May' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Aug' : 8,
            'Sep' : 9,
            'Oct' : 10,
            'Nov' : 11,
            'Dec' : 12
            }
    #++
    def get_file_data(self):
        """ Get source file data for patches
        
        Args:
            None
        
        Returns:
            A mapping of patch names to file names.
        """
        #--
        
        if (self.filedata is None):
            self._get_data()
            
        return self.filedata
    
    #++
    def get_patch_data(self):
        """ Get patch data for source files
        
        Args:
            None
        
        Returns:
            A mapping of file names to patch names.
        """
        #--
        
        if (self.filedata is None):
            self._get_data()
            
        return self.patchdata
    
    #++
    def get_patch_names(self, params=None):
        """ Return list of names of patches in our patch set 
        
        Args:
            params (dict, optional): parameters
                excl_dirs (list, optional): directories to exclude
                incl_dirs (list, optional): directories to include
            
        Returns:
            list of patch names in the order found in patchset
                
        Notes:
            The "name" of a patch is the concatenation of the name of its parent folder
            and its filename, as shown in the patchset description.
                
            If params is None, names of all patches are returned.
        """
        #--
        if ((params is not None) and isinstance(params, dict)):
            excl_dirs = self._check_optional_param(params, 'excl_dirs', list, [])
            incl_dirs = self._check_optional_param(params, 'incl_dirs', list, [])
        else:
            excl_dirs = []
            incl_dirs = []
            
        names = []
        
        groups = self.patchset['groups']
        
        if (groups[0] in self.patchset): # old format?
            for group in groups:
                names += self.patchset[group]
                
        else: # new format
            if (len(incl_dirs) > 0):
                dirs = incl_dirs
            else:
                dirs = groups
                for dir_ in excl_dirs:
                    if (dir_ in dirs):
                        dirs.remove(dir_)
            for dir_ in dirs:
                dirnames = []
                path = ut.join_path(self.patchdir, dir_)   
                for (_, _, files) in os.walk(path):
                    for file_ in files:
                        name = ut.join_path(dir_, file_)
                        dirnames += [name]
                dirnames.sort()
                names += dirnames
                
        return names
    
    #++
    def get_patch_files(self, patchname):
        """ Return a list of source files referenced in one patch file
        
        Args:
            patchname (string): name of patch file
            
        Raises:
            PT_ParameterError, PT_NotFoundError
            
        Notes:
            This function may be used to generate file lists for the *Finder*.                     
        """
        #--
        
        patchname = self._check_file_1_arg('patchname', patchname)
        
        if (self.filedata is None):
            self._get_data()
        
        if (not patchname in self.patchdata):
            raise PT_NotFoundError(self.name, patchname)
        
        # data is a list of tuples (name, line)
        data = self.patchdata[patchname]
        data = [name for (name, _) in data]
        data.sort()
            
        return data
    
    #++
    def get_file_patches(self, filename):
        """ Return a list of patch files that refer to one source file
        
        Args:
            filename (string): name of source file
            
        Raises:
            PT_ParameterError, PT_NotFoundError
                
        Notes:
            This function may be used to generate file lists for the *Matcher*. 
        """
        #--
        
        filename = self._check_file_1_arg('filename', filename)
        
        if (self.filedata is None):
            self._get_data()
        
        if (not filename in self.filedata):
            raise PT_NotFoundError(self.name, filename)
               
        # data is a list of tuples (patch name, line number)
        data = self.filedata[filename]
        data = [name for (name, _) in data]
        data.sort()
            
        return data
    
    #++
    def get_patch_patches(self, patchname):
        """ Get a list of patches that patchname depends on 
            
        Args:
            patchname (string): name of patch file
   
        Returns:
            A list of names of the parent patches in patchset order
            
        Raises:
            PT_ParameterError, PT_NotFoundError
            
        Notes:
            Patch A depends on patch B when they modify the same files
            and patch B precedes patch A in the patch list.
            
        """
        #--
        
        patchname = self._check_file_1_arg('patchname', patchname)
        
        if (self.patchdata is None):
            self._get_data()
        
        if (patchname not in self.patchdata):
            raise PT_NotFoundError(self.name, patchname)
        
        filelist = [name for (name, _) in self.patchdata[patchname]]
        data = {}
        for filename in filelist: 
            patchlist = [name for (name, _) in self.filedata[filename]]
            for patch in patchlist:
                if (patch == patchname): # don't store self or later
                    break
                else: # Here we delete duplicates
                    data[patch] = True
        
        data = self._sort_patches(data)

        return data
        
    def _find_patch_patches(self, patchname):
        ''' Find the patch records for patch (patchname)
        '''
        
        # data is a list of tuples (file name, line number)
        filelist = [name for (name, _) in self.patchdata[patchname]]
        data = {}
        for filename in filelist: 
            patchlist = [name for (name, _) in self.filedata[filename]]
            # Note the patches were stored in patchset order
            for patch in patchlist:
                if (patch == patchname): # don't store self or later
                    break
                else: # Here we delete duplicates
                    data[patch] = True
        data = sorted(data) # 2to3
        
        return data
    
    #++
    def sort_patches(self, params):
        """ Reorder patches to match the order in the patch set
            
        Args:
            patches (list, required):  list of patchname strings
            order   (string, optional): sort order
                'patchset' = sort patches by the order in patchset groups
                'date'     = sort patches by "Author Date:"
                    default is 'patchset'
                
        Returns:
            The list in the specified order
        """
        
        patches = self._check_required_param(params, 'patches', list)
        order   = self._check_optional_param(params, 'order', str, 'patchset')
        
        if (order == 'patchset'):
            if (self.format == 'new'):                
                return self._sort_patches_new(patches)
            else:
                return self._sort_patches_old(patches)
        elif (order == 'date'):
            return self._sort_on_date(patches)
        else:
            raise PT_ParameterError(self.name, 'order')
            
    
    def _check_file_1_arg(self, name, value):
        ''' Validate file argument when only one file is allowed.
        '''
        
        if (ut.is_string_type(value)):
            return value
        else:
            raise PT_ParameterError(self.name, name)
    
    def _check_file_N_args(self, name, value):
        ''' Validate file argument when N files are allowed.
        '''
        
        if (ut.is_string_type(value)):
            return [value]
        elif (isinstance(value, list)):
            return value
        else:
            raise PT_ParameterError(self.name, name)
        
    def _check_file_params(self, params):
        
        if (('file' in params) and ut.is_string_type(params['file'])):
            return [params['file']]
        
        elif (('files' in params) and isinstance(params['files'], list)):
            return params['files']
        
        else:
            raise PT_ParameterError(self.name, 'filespec')
        
    def _sort_patches_old(self, patches):
        ''' In the "old" format, the patchset "groups" item is a list
            of names of groups intended to be processed in list order,
            and files in each group are listed in the intended order of
            processing.
        '''
        
        # Map the patches into a dict on the group name
        dir_ = {}
        for group in self.patchset['groups']:
            dir_[group] = []
        for patchname in patches:
            for group in dir_:
                if (patchname in self.patchset[group]):
                    dir_[group] += [patchname]
                    break
        
        # Extract the patch names in patchset order
        sorted_ = []
        for group in self.patchset['groups']:
            files = dir_[group]
            if (len(files) > 1):
                files.sort()
            sorted_ += files
        
        return sorted_
    
    def _sort_patches_new(self, patches):
        ''' In the "new" (kernel-3.8) format, the patchset "groups" item
            is a list of names of folders under self.patchdir, and the groups
            are intended to be processed in list order, apparently with the
            order of files within a group being controlled by the first four
            characters xof the file's name.
        '''
        
        # Map the patches into a dict on the folder name
        dir_ = {}
        for patchname in patches:
            parts = patchname.split('/', 1)
            folder, filename = parts[0], parts[1]
            if (folder in dir_):
                dir_[folder] += [filename]
            else:
                dir_[folder] = [filename]
        
        # Extract the patch names in patchset order
        sorted_ = []        
        for group in self.patchset['groups']:
            if (group in dir_):
                files = dir_[group]
                if (len(files) > 1):
                    files.sort()
                items = [ut.join_path(group, name) for name in files]
                sorted_ += items
        
        return sorted_ 
    
    def _sort_on_date(self, patches):
        ''' Sort patches on date field. The format is like:
                Fri, 28 Dec 2012 21:00:31 +0200
        '''
        records = []
        for patch in patches:
            strings = ut.read_strings(ut.join_path(self.patchdir, patch))
            for string in strings:
                if ("Date:" in string): # e.g. 'Date: Wed, 16 Jan 2013 19:09:47 +0000'
                    fields = ut.string_to_words(string[6:].lstrip(' \t'))
                    _, s_day, s_mon, s_year, s_hms, _ = fields
                    s_hour, s_minute, s_second = s_hms.split(':')
                    day, year = int(s_day), int(s_year)
                    hour, minute, second = int(s_hour), int(s_minute), int(s_second)
                    month = self.month_numbers[s_mon]
                    # ignoring microseconds
                    dt = datetime(year, month, day, hour, minute, second) 
                    records += [(dt, patch)]
                    break
        
        records = sorted(records, key = lambda r: r[0])
        
        patches = [patch for (_, patch) in records]
        
        return patches
                   
    def _get_data(self):
        ''' Scan patchset to get two mappings:
                filedata maps filenames to patches
                patchdata maps patches to filenames
        ''' 

        filedata  = {}
        patchdata = {}
        for patchname in self.get_patch_names():
            filelist = []
            strings = ut.read_strings(ut.join_path(self.patchdir, patchname))
            for index in range(len(strings)):
                if (strings[index].startswith('diff --git ')):
                    filename = ut.get_string_filename(strings[index])
                    if (filename in filedata):
                        filedata[filename] += [(patchname, index)]
                    else:
                        filedata[filename] = [(patchname, index)]
                    filelist += [(filename, index)]
            patchdata[patchname] = filelist
                        
        self.filedata  = filedata                
        self.patchdata = patchdata
        
    def _split_path_ext(self, string):
    
        index  = string.rfind('.')
        if (index != -1):
            string, ext = string[:index], string[index + 1:]
        else:
            ext = ''
            
        return string, ext
    
    def _split_path_name(self, string):
        
        index  = string.rfind('/')
        if (index != -1):
            prefix, string = string[:index], string[index + 1:]
        else:
            prefix = ''
        
        return prefix, string
    
    