# -*- coding: UTF-8 -*-
'''
Created on Apr 6, 2014

@copyright 2014, Milton C Mobley

Launch graphical editor(s) to view a file and the files it references.

Tested editors:
    Linux:   gedit, gvim
    Windows: write (aka WordPad)

To use gvim, pass this editspec:

    {
        'target'    : 'gvim',
        'multifile' : True,
        'multiview' : False
    }
'''

import os
# 2to3 from types import StringTypes

from patchtools.lib.patch      import Patch
from patchtools.lib.patchset   import PatchSet
from patchtools.lib.ptobject   import PTObject
from patchtools.lib.command    import Command
from patchtools.lib.exceptions import PT_ParameterError, PT_NotFoundError
from patchtools.lib.functions  import Functions as ut

#++
class Viewer(PTObject):
    """ Display a set of files in a user selected editor
    """
    #--

    #++
    def __init__(self, params=None):
        """ Constructor
        
        Args:
            params (dict, optional): parameters
                editor (dict, optional): editor specification
                    target    (string, required): name or path for target program
                    multifile (bool, required):   can open multiple files in a single invocation
                    multiview (bool, required):   can display multiple files in a single window
                root (string, optional): a path to prefix to all filenames
                wait (bool, optional):   wait for subprocess to exit
                    default is False
            
        Raises:
            PT_ParameterError
                
        Notes:
            If editor is not specified, the default editor for the host system is used.
            The default editor for Linux is gedit. The default editor for Windows is write
            (aka 'WordPad').
            If any method is called in a loop, the wait option should be True.
        """
        #--
    
        self.name = 'Viewer'
        
        if ((params is not None) and (not isinstance(params, dict))):
            raise PT_ParameterError(self.name, 'params')
        
        if (isinstance(params, dict)):
            editor = self._check_optional_param(params, 'editor', dict, None)
            self.root = self._check_optional_string_param(params, 'root', None)
        else:
            editor = None
            self.root = None
            
        is_windows = ut.is_windows()
        
        if (editor is not None):
            self.target    = self._check_required_string_param(editor, 'target')
            self.multifile = self._check_required_param(editor, 'multifile', bool)
            self.multiview = self._check_required_param(editor, 'multiview', bool)
        elif (is_windows):
            self.target    = 'write'
            self.multifile = False # check this
            self.multiview = False  
        else:
            self.target    = 'gedit'
            self.multifile = True
            self.multiview = True
        
        if (is_windows):    
            self.cmd_sep = ' && '
        else:   
            self.cmd_sep = ' ; '
        self.command = Command()    
    
    #++        
    def view(self, files):
        """ Launch specified editor to view the file(s)
    
        Args:
            files (list): paths of files to display
            check_files(bool): verify target files exist
                          
        Raises:
            PT_ParameterError for any missing files
        """
        #--
        
        
        if (not isinstance(files, list)):
            raise PT_ParameterError(self.name, 'files')
        
        # The user may specify a file that does not exist
        paths = []
        for path in files:
            if (ut.is_file(path)):
                paths += [path]
        
        return self._view(paths)
                
    #++    
    def vp2f(self, patchname, params):
        """ List patch and files it uses
    
        Args:
            patchname (string): name of patch file
            params    (dict):   parameters
                patchdir  (string, required): path of patches folder
                
        Raises:
            PT_ParameterError for any missing files
        """
        #--
        
        if (not isinstance(params, dict)):
            raise PT_ParameterError(self.name, 'params')
          
        sourcedir = self._check_directory_param(params, 'sourcedir')
        patchdir  = self._check_directory_param(params, 'patchdir')
        patchpath = self._check_filename_param(patchdir, patchname, 'patchname')
        
        # Get list of source filenames referenced in patch
        # Note that a patch may refer to files that do not exist in the source tree.
        filelist = Patch.list_files(patchpath)
        filepaths = []
        for file_ in filelist:
            path = ut.join_path(sourcedir, file_)
            if (ut.is_file(path)):
                filepaths += [path]
            
        paths = [patchpath] + filepaths
        
        return self._view(paths)

    #++    
    def vf2p(self, filename, params):
        """ List file and patches that use it
    
        Args:
            filename (string): name of patch file
            params   (dict):   parameters
                sourcedir (string, required): path of sources folder
                patchdir  (string, required): path of patches folder
                patchset  (dict, required):   patchset description
            
        Raises:
            PT_ParameterError for any missing files
        """

        if (not isinstance(params, dict)):
            raise PT_ParameterError(self.name, 'params')
        
        sourcedir = self._check_directory_param(params, 'sourcedir')
        patchdir  = self._check_directory_param(params, 'patchdir')
        patchset  = self._check_required_param(params, 'patchset', dict)
        filepath  = self._check_filename_param(sourcedir, filename, 'filename')
        
        # Get list of patches that use the source file
        patchset   = PatchSet({ 'patchdir' : patchdir, 'patchset' : patchset })
        patchlist  = patchset.get_file_patches(filename)
        
        # Arrange the patches in patchset group order.
        #patchlist = patchset.sort_patches({ "patches" : patchlist })
        
        # Create abolute paths for the patches
        patchpaths = []
        for patchname in patchlist:
            patchpaths += [ut.join_path(patchdir, patchname)]
        filepaths  = [filepath] + patchpaths
         
        return self._view(filepaths)
    
    #++                 
    def vp2p(self, patchname, params):
        """ Display a patch file and the other patch files that use the same source files
        
        Args:
            patchname (string): name of patch file
            params    (dict):   parameters
                patchdir  (string, required): path of patches folder
                patchset  (dict, required):   patchset description
                
        Raises:    
            PT_ParameterError for any missing files
        """
        #--
        
        if (not isinstance(params, dict)):
            raise PT_ParameterError(self.name, 'params')
        
        patchdir  = self._check_directory_param(params, 'patchdir')
        patchset  = self._check_required_param(params, 'patchset', dict) 
        patchpath = self._check_filename_param(patchdir, patchname, 'patchname')
        
        # Get list of files used by the patch
        filelist = Patch.list_files(patchpath)
        
        # Get list of patches that use the same files
        patchlist = []
        patchset  = PatchSet({ 'patchdir' : patchdir, 'patchset' : patchset })
        patchdata = patchset.get_file_data()
        patchkeys = sorted(patchdata) # 2to3
        for file_ in filelist:
            for key in patchkeys:
                if (file_ == patchdata[key][0]):
                    patchlist += [key]
                    break
        patchpaths = [ut.join_path(patchdir, patch) for patch in patchlist]
        paths = [patchpath] + patchpaths
        
        return self._view(paths)
    
    #++
    def vp2a(self, patchname, archpath, params):
        """ Display patch and archive diff sections that use its files
        
        Args:
            patchname (string): name of patch file
            archpath  (string): path to archive file
            params    (dict):   parameters
                patchdir (string, required): path of patches folder
                tempdir  (string, required): path to store temporary data
                
        Raises:    
            PT_ParameterError for any missing files
        
        Notes:
            Launches the editor synchronously, since a temporary file is created to hold
            the archive sections.
        """
        #--
        
        if (not isinstance(params, dict)):
            raise PT_ParameterError(self.name, 'params')
        
        sourcedir  = self._check_directory_param(params, 'sourcedir')
        patchdir = self._check_directory_param(params, 'patchdir')
        tempdir = self._check_directory_param(params, 'tempdir')
        
        patchpath = self._check_filename_param(patchdir, patchname, 'patchname')
        if (not ut.is_file(archpath)):
            raise PT_NotFoundError(self.name, archpath)
        
        # Get list of files used by the patch
        filelist = Patch.list_files(patchpath)
        filepaths = [ut.join_path(sourcedir, file_) for file_ in filelist]

        # Get archive diff sections that use any of the files
        strings = []
        for diff in self._get_diffs(archpath, filepaths):
            strings += diff
        
        if (len(strings) == 0):
            return []
        
        # Store the diff sections in a temporary file
        archname = archpath[archpath.rfind('/') + 1:]
        tempname = archname + '.tmp'
        temppath = ut.join_path(tempdir, tempname)
        ut.write_strings(strings, temppath)
        
        self._view([patchpath, temppath], True)
        
        # Note that we requested _view to wait for subprocess exit above,
        # so that we do not try to delete the file while it is in use.
        
        os.remove(temppath)
        
    #++
    def vcpf(self, checkpath, patchname, params):
        """ List checker output file, patch and files it uses
    
        Args:
            checkpath (string): path to Checker output file
            patchname (string): patch name
            params (dict) parameters:
                sourcedir (string, required): path of sources folder
                patchdir  (string, required): path of patches folder
            
        Raises:    
            PT_ParameterError
            PT_NotFoundError
        """
        #--

        if (not isinstance(params, dict)):
            raise PT_ParameterError(self.name, 'params')
    
        if (not ut.is_file(checkpath)):
            raise PT_NotFoundError(self.name, checkpath)
        
        sourcedir = self._check_directory_param(params, 'sourcedir')
        patchdir  = self._check_directory_param(params, 'patchdir')
        patchpath = self._check_filename_param(patchdir, patchname, 'patchname')
        
        # Get list of source filenames referenced in patch.
        # Note that a patch may refer to files that do not exist in the source tree.
        filelist = Patch.list_files(patchpath)
        filepaths = []
        for file_ in filelist:
            path = ut.join_path(sourcedir, file_)
            if (ut.is_file(path)):
                filepaths += [path]
            
        paths = [checkpath, patchpath] + filepaths
            
        return self._view(paths)
    
    def _check_directory_param(self, params, field):
        
        path = self._check_required_string_param(params, field)
        if (not ut.is_dir(path)):
            raise PT_NotFoundError(self.name, field)
        
        return path
            
    def _check_filename_param(self, prefix, value, name):
        
        if (not ut.is_string_type(value)):
            raise PT_ParameterError(self.name, name)
        
        path = ut.join_path(prefix, value)
        if (not ut.is_file(path)):
            raise PT_NotFoundError(self.name, value)
        
        return path
    
    def _get_diffs(self, archive, filenames):
        ''' Generate list of diff sections that refer to files in filenames
        '''
        
        strings = ut.read_strings(archive)
        
        diff = []
        for index in range(len(strings)):
            string = strings[index]
            if (string.lstrip().startswith('diff --git ')):
                if (len(diff) > 0):
                    yield diff
                filename = ut.get_string_filename(string)
                if (filename in filenames):
                    diff = ["%04d: %s" % (index + 1, string)]
            elif (len(diff) > 0):
                diff += ["%04d: %s" % (index + 1, string)]
        if (len(diff) > 0):
            yield diff
                
    def _view(self, paths):
        
        if (self.multiview):
            # Launch one editor to view N files
            args = [self.target] + paths
        else:
            # Launch N editors to view N files
            cmds  = [(self.target + ' ' + path) for path in paths]   
            args = self.cmd_sep.join(cmds)
        
        return self.command.sync(args)
