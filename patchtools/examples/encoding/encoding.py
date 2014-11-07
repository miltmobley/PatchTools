'''
Created on Oct 12, 2014

@author: milton

Determine if text files in a source tree are compatible with the 'Latin_1' encoding.
The Matcher's callback function option is used to evaluate files for inclusion in the
tests.
'''
from chardet  import detect as chardetect

from patchtools.lib.helper     import Helper
from patchtools.lib.exceptions import ExceptionHandler
from patchtools.lib.functions  import Functions as ut

def is_text_file(string):
    
    if ('defkeymap.map' in string):
        pass
    path = ut.join_path(c['sourcedir'], string)
    inpt = open(path, "rb")
    fsiz = ut.file_size(path)
    abuf = inpt.read(min(1024, fsiz))
    inpt.close()
    ret  = chardetect(abuf)
    return (isinstance(ret, dict) and ('encoding' in ret) and (ret['encoding'] is not None))

def _enumerate():
    
    p = { "root_path" : c['sourcedir'], "excl_dirs" : [".git"],
          "incl_files" : { 'funcs' : [is_text_file] }, 'test_dirs' : True }
    w = h.walk(p)
    print(str(len(w)))
    h.write(w, 'walk.txt')

def _iterate():

    r = c['sourcedir']
    t = ut.join_path(c['tempdir'], 'encoding.dat')
    w = h.read('walk.txt')
    for file_ in w:
        path = ut.join_path(r, file_)
        s = ut.read_strings(path)
        ut.write_strings(s, t)
          
if __name__ == '__main__':
    
    global c, h
    
    exception_handler = ExceptionHandler()
    
    try:
        h = Helper('config.json')
        c = h.config
        
        print('walking ...')
        _enumerate()
        
        print('iterating ...')
        _iterate()
        
        print('done')
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        exception_handler(e)
        exit(-1)
            