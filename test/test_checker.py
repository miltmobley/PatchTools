'''
Created on Oct 15, 2014

@author: milton
'''

from patchtools.lib.helper     import Helper
from patchtools.lib.exceptions import ExceptionHandler
from patchtools.lib.strings    import Strings

if __name__ == '__main__':
    
    global c, h
    
    exception_handler = ExceptionHandler()
    
    try:
        
        h = Helper('config.json')
        c = h.config
        drivers = h.read('alldrivers.txt')
        patches = h.list_patches()
        params  = { 'root_path' : c['patchdir'], 'file_paths' : patches, 'mode' : 'file' }         
        drvrefs = h.find({ 'substr' : drivers }, params)
        drvrefs = [dr[:dr.find(':')] for dr in drvrefs]
        drvrefs = Strings(drvrefs).sort().unique()
        #print(len(drvrefs))
        
        #l = h.list_patches()
        #l = ["dma/0001-Without-MACH_-option-Early-printk-DEBUG_LL.patch"]
        p = h.extend(c['defaults'], { 'mode' : 'complete', 'find' : True, 'debug' : 1 })
        k = h.check(drvrefs, p)
        print(len(k))
        h.write(k, 'check.txt')
    
    except KeyboardInterrupt:
        pass     
    except Exception as e:
        exception_handler(e)
        exit(-1)
        
    print('done')