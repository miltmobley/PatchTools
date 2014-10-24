'''
Created on Oct 2, 2014

@copyright 2014, Milton C Mobley

This is a simple test of the Watcher and Archive classes.
'''
from patchtools.lib.helper     import Helper
from patchtools.lib.exceptions import ExceptionHandler
from patchtools.lib.functions  import Functions as ut

if __name__ == '__main__':
    
    global c, h
    
    exception_handler = ExceptionHandler()
    
    try:
        
        h = Helper('config.json')
        c = h.config
        archdir  = ut.join_path(c['datadir'], 'archives')
        archpath = ut.join_path(archdir, 'patch-3.16.3')
        h.watch(archpath, c)
    
    except KeyboardInterrupt:
        pass    
    except Exception as e:
        exception_handler(e)
        exit(-1)
    
    print('done')