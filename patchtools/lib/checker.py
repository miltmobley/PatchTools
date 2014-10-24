# -*- coding: UTF-8 -*-
'''
Created on Feb 20, 2014

@copyright 2014, Milton C Mobley

See the checker module section of the documentation for further information.
'''

# 2to3 from types import str

from patchtools.lib.patch      import Patch
from patchtools.lib.ptobject   import PTObject
from patchtools.lib.exceptions import PT_ParameterError
from patchtools.lib.functions  import Functions as ut

#++
class Checker(PTObject):
    """ Validate the contents of Linux kernel patch files against
        the files specified in them
    """
    #--
     
    #++
    def __init__(self, params):
        """ Constructor
                   
        Args:
            params (dict): parameters
                sourcedir  (string,required):       path to source directory
                patchdir   (string,required):       path to patch directory
                targets    (string/list, optional): target file(s)
                indent     (int, optional):         indentation
                    default = 3
                mode (string, optional): scanning mode
                    'full'     : report edit errors only
                    'complete' : report status of all edits
                    default is 'full' 
                find (bool, optional): find missing strings
                    default is True
                debug (int, optional) debug options
                    default is 0
            
        Raises:
            PT_ParameterError
                    
        Notes:
            If '' is passed as sourcedir or patchdir, the caller must supply file
            paths to the match method that are accessible from the caller's current dircectory.
                
            If 'targets' is specified the code will only scan diff sections that
            modify the filenames in params['targets]
        """
        #--
        
        self.name = 'Checker'
        
        if ((params is None) or (not isinstance(params, dict))):
            raise PT_ParameterError(self.name, 'params')
        
        self.sourcedir = self._check_required_string_param(params, 'sourcedir')
        self._check_path_param('sourcedir', self.sourcedir)
        
        self.patchdir = self._check_required_string_param(params, 'patchdir')
        self._check_path_param('patchdir', self.patchdir)
        
        self.indent = self._check_optional_string_param(params, 'indent', '   ')
        self.mode   = self._check_optional_string_param(params, 'mode', 'full')
        self.find   = self._check_optional_param(params, 'find', bool, False)
        self.debug  = self._check_optional_param(params, 'debug', int, 0)
        
        if (not self.mode in ('full', 'complete')):
            raise PT_ParameterError(self.name, 'mode')
        
        if ('targets' in params): 
            targets = params['targets']
            if (ut.is_string_type(targets)):
                self.targets = [targets]
            elif (isinstance(targets, list) and ut.is_string_type(targets[0])):
                self.targets = targets
            else:
                raise PT_ParameterError(self.name, 'targets')
        else:
            self.targets = None
              
    #++                                
    def match(self, param):
        """ Validate the contents of one or more Linux kernel patch files against a kernel

        Args:
            param (choice):
                (string): path to patch file
                (list): paths to patch files
                
        Returns:
            A list of strings describing the results of analysis

        Raises:
            PT_ParameterError
            PT_ParsingError
        """
        #--
        
        if (ut.is_string_type(param)):
            paths = [param]
        elif (isinstance(param, (list, tuple))):
            paths = param
        else:
            raise PT_ParameterError(self.name, param)
        
        self.msgs = []
        self._misc_msg('patchdir  = "%s":' % self.patchdir)
        self._misc_msg('sourcedir = "%s":' % self.sourcedir)
        
        passed = skipped = 0
        for path in paths:
            if (self.debug > 0):
                print("matching %s" % path)
            errors = self._check(path)
            if (errors == 0):
                passed += 1
            elif (errors < 0):
                skipped += 1
                
        self._misc_msg('\nSummary:')
        self._misc_msg('%d passed, %d skipped, %d tested' % (passed, skipped, len(paths)), 1)
    
        return self.msgs
          
    def _check(self, patchpath):
        
        self._misc_msg('\nPATCH: "%s"' % patchpath)   
        patchpath = ut.join_path(self.patchdir, patchpath)
        pdata = Patch(patchpath)
        if (len(pdata.diffs) == 0):
            self._info_msg('skipping empty/commented patch', 1)
            return 0
 
        if (pdata.patch_type == 'binary'):
            self._info_msg('skipping binary patch', 1)
            return -1
               
        errors = 0
        for diff in pdata.diffs:
            
            self._misc_msg('DIFF: "%s"' % diff.spec, 1)
            
            if (not self._check_paths(diff)):
                errors += 1
                continue
            
            if (diff.old_path == '/dev/null'): # Can't fail on adding lines to a new file
                continue
                   
            old_lines = ut.read_strings(ut.join_path(self.sourcedir, diff.old_path))
               
            for hunk in diff.hunks:
                self._misc_msg('HUNK: "%s"' % hunk.spec, 2)
                edits = hunk.edits
                start = hunk.old_start
                count = hunk.old_count
                tag   = 'old'    
                note = hunk.note
                if (not self._check_hunk_format(start, count, len(old_lines), tag)):
                    errors += 1
                    continue
                
                errors += self._check_hunk_edits(diff.old_path, edits, start, count, note, old_lines)
                    
        self._info_msg("%d patch errors" % errors, 1)
        
        return errors
    
    def _check_paths(self, diff):
        ''' Check that:
            (1) file named in diff spec exists (GIT format only)
            (2) file named in '---' line exists or is /dev/null
            (3) file named in '+++' line exists or is /dev/null
            (4) file to be created exists in new tree
            (5) file to be deleted does not exist in old tree
        '''
        
        if (not ut.is_file(ut.join_path(self.sourcedir, diff.a_path))):
            self._error_msg('"a" file not found: %s' % diff.a_path, 2)
            return False
        
        if (diff.old_path != '/dev/null'):
            if (not ut.is_file(ut.join_path(self.sourcedir, diff.old_path))):
                self._error_msg('"old" file not found: %s' % diff.old_path, 2)
                return False
        else:
            if (ut.is_file(ut.join_path(self.sourcedir, diff.new_path))):
                self._error_msg('"new" file found in old tree: %s' % diff.new_path, 2)
                return False
                
        if (diff.new_path != '/dev/null'):
            if (not ut.is_file(ut.join_path(self.sourcedir, diff.new_path))):
                self._error_msg('"new" file not found: %s' % diff.new_path, 2)
                return False
        else:
            if (not ut.is_file(ut.join_path(self.sourcedir, diff.old_path))):
                self._error_msg('"old" file not found in old tree: %s' % diff.old_path, 2)
                return False
                
        return True
    
    def _check_hunk_format(self, start, count, length, tag):
        """ Validate a hunk's start, count, etc., values against the target file.
            The values may be incorrect due to previous merge of other patches
            into the 'old' tree, or to failure to add lines spcified in other hunks
            or patches.
        """
        if ((start > 0) and (count > 0)): # path is a file
            # start is a 1-based index
            if ((start > length) or ((start + count) > length)):   
                self._error_msg("invalid %s start or count for file: start=%d, count=%d, length=%d" % \
                                (tag, start, count, length), 3)
                return False 
            
        return True
    
    def _check_hunk_note(self, note, linenum, alines, old_path):
        """ A hunk "note" (any text after the second '@@') appears to be a copy of
            the closest previous line with a character in column 0. This is often
            the start declaration of a previous or enclosing function, e.g. 'static int foo(...'.
            We may be able to locate a source fragment that has moved by finding the note.
            But we only search for lines that are likely to be unique in the file.
        """
        errors = []
        if (self._is_landmark(old_path, note)):
            matches = self._find_line(note, alines)
            for match in matches:
                errors += ['hunk note found at %d' % match]
                
        return errors
                              
    def _is_null_path(self, path):
        """ Determine if a path indicates a non existent file.
        """
        return (path == '/dev/null')
    
    def _check_hunk_edits(self, filepath, edits, start, count, note, lines):
        """ Check edits against the "a" file. Report errors when lines to be deleted
            or merged are missing, and when lines to be added are present. Note that
            patch lines and source lines may have the same text, but differ in leading
            whitespace. We strip and normalize the strings before testing them. 
            In 'find' mode, try to find missing lines.
        """
        errors = warnings = 0
        current = start
        mismatches = []
        
        for (index, edit1, edit2) in self._get_edits(edits):
            
            op, text1 = edit1[0], edit1[1:]
            norm1 = ut.normalize_string(text1)
            line  = lines[current - 1] # patch line numbers are 1-based
            norm3 = ut.normalize_string(line)
            
            if (edit2 is not None): # change request
                text2 = edit2[1:]
                norm2 = ut.normalize_string(text2)
                if (norm2 == norm3): # Change already applied
                    self._ok_msg('"change" line found at %d: "%s"' % (current, text2), 3)
                elif (norm1 == norm3): # Change not yet applied
                    self._info_msg('"change" line not found at %d: "%s"' % (current, text2), 3)
                else:
                    self._error_msg('"delete" line not found at %d: "%s"' % (current, text2), 3)
                current += 1 # advance to next edit line
                    
            elif (op == '-'): # delete line
                # A line to be deleted by the patch should be at the specified location,
                # but may be elsewhere in the file. If self.find is True, we will look for it.
                # Doing so may return multiple matches.
                if (norm1 != norm3):
                    self._error_msg('"delete" line not found at %d: "%s"' % (current, text1), 3)
                    mismatches += [(index, '-')]
                else:
                    if (self.mode == 'complete'):
                        self._ok_msg('"delete" line found at %d: "%s"' % (current, text1), 3)
                current += 1 # advance to next edit line
            
            elif (op == '+'): # insert line
                # A line to be inserted by the patch should not be at the specified location,
                # but may be elsewhere in the file. If self.find is True, we will look for
                # significant "add" lines below. Doing so may return multiple matches.
                if (norm1 == norm3):
                    self._error_msg('"add"    line found at %d: "%s"' % (current, text1), 3)
                    errors += 1
                else: 
                    if (self.mode == 'complete'):
                        self._info_msg('"add"    line not found at next line: "%s"' % text1, 3)
                    mismatches += [(index, '+')]
                                 
            else: # (op == ' '): # merge line
                # a line to be merged by the patch should be at the specified location,
                # but may be elsewhere in the file. If self.find is True, we will look for it.
                # Doing so may return multiple matches.
                if (norm1 != norm3):
                    self._warn_msg('"merge"  line not found at %d: "%s"' % (current, text1), 3)
                    warnings += 1
                    mismatches += [(index, ' ')]
                elif (self.mode == 'complete'):
                    self._ok_msg('"merge"  line found at %d: "%s"' % (current, text1), 3)
                current += 1 # advance to next edit line                                 
        
        if ((len(mismatches) > 0) and self.find):   
            self._match(filepath, edits, lines, mismatches)
            return 1
        else:
            return 0
    
    def _match(self, filepath, edits, strings, mismatches):
        ''' (1) Try to find missing "delete" or "merge" lines
            (2) Try to find "add" lines
        '''
        for edit_ndx, edit_type in mismatches:
            edit_text = edits[edit_ndx]
            text = edit_text[1:]
            if (text.strip() == 'bool'):
                pass
            if (self._is_landmark(filepath, text)):   
                matches = self._find_line(text, strings)
                for match in matches:
                    if (edit_type == '+'):
                        self._find_msg('"add"    line found at %d: "%s"' %  (match + 1, text), 3)
                    elif (edit_type == '-'):
                        self._find_msg('"delete" line found at %d: "%s"' %  (match + 1, text), 3)
                    else:
                        self._find_msg('"merge"  line found at %d: "%s"' %  (match + 1, text), 3)
                    
        return None # for bkpt only 

    def _find_line(self, text, strings):
        ''' Try to find text in the source strings.
        
            Both text and strings are normalized to eliminate mismatches on varying whitespace.
            
            Source strings may contain items such as author name, etc. with unicode characters
            that can't be converted to ascii or latin-1, so we must not convert the strings to
            Python 2.x str objects.
        '''
        text = ut.normalize_string(text, True)
        matches = []
        for index in range(len(strings)):
            string = ut.normalize_string(strings[index], True)
            if (text == string):
                matches += [index]
        
        return matches
            
    def _split_edit(self, edit):
        """ Split an edit line into op ('+','-' or ' ') and text. Edit lines sometimes
            come in as empty strings or just ' '
        """
        length = len(edit)
        if (length > 1): 
            op, text = edit[0], edit[1:]
        elif (length > 0):
            op, text = edit[0], ''
        else:
            op, text = ' ', ''
        
        return op, text
    
    def _get_edits(self, edits):
        ''' edit lines can be '+' (add), '-' (delete), or ' ' (merge) edits. A '-' followed by
            a '+' is a change request. We use a generator to return the '-' and '+' edits of changes
            as a pair, since modifying the loop index in a for statement controlled by a range
            doesn't work.
        '''
        elen  = len(edits)
        index = 0
        while (index < elen):
            e1 = edits[index]
            if (e1.startswith('-')):
                if (index < (elen - 1)):
                    e2 = edits[index + 1]
                    if (e2.startswith('+')):
                        yield (index, e1, e2)
                        index += 1
            else:
                yield (index, e1, None)
            index += 1
                
    def _is_landmark(self, filepath, string):
        """ Determine if a string is a "landmark" string , i.e. one that is likely to be unique
            in the file, and thus may be easy to isolate if it is present. Searching for strings
            such as '};' could give a large number of extraneous matches. 
        """
    
        if ((len(string) == 0) or string.isspace()):
            return False
        else:
            words = ut.string_to_words(string)
        
        words2 = []
        for word in words:
            if ('_' in word):
                sylls = word.split('_')
                words2 += sylls
            else:
                words2 += [word]
        words = words2
        
        words2 = []
        for word in words:
            if ('-' in word):
                sylls = word.split('-')
                words2 += sylls
            else:
                words2 += [word]
        words = words2
        
        if (len(words) > 4):
            return True
        
        index = filepath.rfind('/') + 1
        filename = filepath[index:]
            
        if (filename.endswith('.c') or filename.endswith('.h')):
            return self._is_c_h_landmark(string, words)
       
        elif (filename.endswith('.S') or filename.endswith('.inc')):
            return self._is_S_landmark(string, words)
        
        elif (filename.endswith('.dts') or filename.endswith('.dtsi')):   
            return self._is_dts_landmark(string, words)
                
        elif (filename.startswith('Kconfig')):
            return self._is_Kconfig_landmark(string, words)
   
        elif (filename.startswith('Makefile')):
            return self._is_Makefile_landmark(string, words)
        
        return self._is_generic_landmark(string, words)
                      
    def _is_c_h_landmark(self, string, words):
        """ Determine if a string is a "landmark" string in a .c or .h file.
        """
        
        #if (self._is_c_h_S_comment(string)):
        #    return False
                
        word0 = words[0]
        
        if ((len(words) == 1) and (words[0] in ('/*','*/','}',')',');','bool'))):
            return False
            
        if (word0 in ('#ifdef', '#ifndef', '#include', 'void', 'const', 'static', 'extern', 'struct', 'union')):
            return True
        
        elif (word0.startswith('MACHINE_')):
            return True
        
        elif (word0.startswith('MODULE_')):
            return True
        
        elif (word0.startswith('module_')):
            return True
        
        elif (word0.startswith('DEFINE_')):
            return True
        
        elif (word0.startswith('DECLARE_')):
            return True
        
        else:
            for word in words:
                if ('(' in word): # start of argument list?
                    return True
                elif (')' in word): # end of argument list?
                    return True
                elif ('->' in word): # pointer dereference
                    return True
            return False
        
    def _is_S_landmark(self, string, words):
        """ Determine if a string is a "landmark" string in a .S (assembler) file.
        """
        
        #if (self._is_c_h_S_comment(string)):
        #    return False
        
        word0 = words[0]
        
        if (word0 in ('#ifdef', '#ifndef', '#include', '#if')):
            return True
        
        elif (word0 in ('.section' , '.size', '.align')):
            return True
        
        elif (word0.endswith(':')):  # label
            return True
        
        else:
            return False
                          
    def _is_dts_landmark(self, string, words):
        """ Determine if a string is a "landmark" string in a .dts or .dtsi file.
            Any line that is not blank or '};' is significant.
        """
        
        if (words[0] in ('};','>;','/*','*/')):
            return False
        
        if ('status =' in string):
            return False
        
        if ('#address-cells = <1>;' in string):
            return False
        
        if ('interrupt-parent = <&intc>;' in string):
            return False
        
        if ('#size-cells = <0>;' in string):
            return False
        
        if ('pinctrl-names = "default";' in string):
            return False
        
        return True
            
        
    def _is_Kconfig_landmark(self, string, words):
        """ Determine if a string is a "landmark" string in a Kconfig file.
        """
        
        #if (self._is_makefile_comment(string)):
        #    return False
        
        return (words[0] in ('config','select','depends','source','menu','choice'))
    
    def _is_Makefile_landmark(self, string, words):
        """ Determine if a string is a "landmark" string in a Makefile.
        """
        
        if (string.startswith('# -')):
            return False
        
        if ('CONFIG_' in string):
            return True
        
        for word in words:
            if (word.endswith(':')): # make target
                return True
            
        return False
    
    def _is_generic_landmark(self, string, words):
        
        # Any string that has > 5 words may be unique
        if (len(words) > 5):
            return True
            
        # Any string that has a word with > 12 chars may be unique
        for word in words:
            if (len(word) > 12):
                return True
        
        return False

    def _is_c_h_S_comment(self, string):
        
        string = string.strip()
        if (string.startswith('/*')):
            return True
        elif (string.endswith('*/')):
            return True
        elif (string.startswith('//')):
            return True
        else:
            return False
    
    def _is_makefile_comment(self, string):
        
        return string.lstrip().startswith('#')
                         
    def _normalize(self, string):
        ''' Strip leading and trailing whitespace, but not trailing '\n'.
            Replace all internal whitespace segments by a single space.
        '''
        string = string.replace('\t', ' ')
        string = string.lstrip(' ')
        while ('  ' in string):
            string = string.replace('  ', ' ')
            
        return string
    
    def _indent(self, string, level=0):
        
        return level * self.indent + string
    
    def _error_msg(self, string, level=0):
        ''' Format error message
        '''
        text = self._indent('ERROR: ' + string, level)
        self.msgs += [text]
        if (self.debug > 1):
            print(text)
            
    def _info_msg(self, string, level=0):
        ''' Format info message
        '''
        text = self._indent('INFO:  ' + string, level)
        self.msgs += [text]
        if (self.debug > 1):
            print(text)
            
    def _find_msg(self, string, level=0):
        ''' Format info message
        '''
        text = self._indent('FIND:  ' + string, level)
        self.msgs += [text]
        if (self.debug > 1):
            print(text)
            
    def _ok_msg(self, string, level=0):
        ''' Format complete mode message
        '''
        text = self._indent('-OK-:  ' + string, level)
        self.msgs += [text]
        if (self.debug > 1):
            print(text)
    
    def _warn_msg(self, string, level=0):
        ''' Format info message
        '''
        text = self._indent('WARN:  ' + string, level)
        self.msgs += [text]
        if (self.debug > 1):
            print(text)
                    
    def _misc_msg(self, string, level=0):
        ''' Format miscellaneous message
        '''
        text = self._indent(string, level)
        self.msgs += [text]
        if (self.debug > 1):
            print(text)
    
    def _check_targets(self, diff_file):
        
        if (self.targets is None):
            return True
        
        for target in self.targets:
            if (target in diff_file):
                return True
        
        return False
                

        
    
    
    