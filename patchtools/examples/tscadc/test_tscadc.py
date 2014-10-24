'''
Created on May 4, 2014

@copyright 2014, Milton C Mobley

Use the Helper to investigate tsc_adc issues.

The relevant DTS source files include:
    am335x-boneblack.dts
    am335x-bone-common.dtsi
    am33xx.dtsi
    am33xx-clocks.dtsi
    tps65217.dtsi
'''

from patchtools.lib.strings    import Strings
from patchtools.lib.helper     import Helper
from patchtools.lib.exceptions import ExceptionHandler

# Initial survey: find patches that relate to "tscadc","tsc","adc"
def find_patch_refs():
    l = h.list_patches()
    p = { "substr" : ["tscadc.c","tscadc.h","tsc.c","tsc.h","adc.c","adc.h"] }
    f = h.find(p, { "root_path" : c['patchdir'], "file_paths" : l, "format" : "full" })
    h.save(f, "test1.tmp")

'''
Inspection of test1.tmp shows these files are touched by the patches:
    (1) drivers/iio/adc/ti_am335x_adc.c
    (2) drivers/input/touchscreen/ti_am335x_tsc.c
    (3) drivers/mfd/ti_am335x_tscadc.c
    (4) include/linux/mfd/ti_am335x_tscadc.h
    (5) include/linux/input/ti_am335x_tsc.h
    (6) include/linux/clk-provider.h

Inspection of the target kernel shows it does not have:
    include/linux/input/ti_am335x_tsc.h
'''

# Make lists of the filenames of the patches that touch each file, without duplicates
def find_patch_refs_2():
    l = h.list_patches()
    t = ["drivers/iio/adc/ti_am335x_adc.c",
         "drivers/input/touchscreen/ti_am335x_tsc.c",
         "drivers/mfd/ti_am335x_tscadc.c",
         "include/linux/mfd/ti_am335x_tscadc.h"
         "include/linux/input/ti_am335x_tsc.h",
         "include/linux/clk-provider.h"]
    p = { "root_path" : c['patchdir'], "file_paths" : l, "format" : "files" }  
    f = h.find({ "substr" : t }, p)
    f = [s[:s.find(':')] for s in f] # Extract patch name
    s = Strings(f).sort().unique()
    h.save(s, "test3.tmp")

def find_patch_refs_3():
    l = h.list_patches()
    t = ["include/linux/mfd/ti_am335x_tscadc.h"]
    p = { "root_path" : c['patchdir'], "file_paths" : l, "format" : "files" }  
    f = h.find({ "substr" : t }, p)
    f = [s[:s.find(':')] for s in f] # Extract patch name
    s = Strings(f).sort().unique()
    h.save(s, "test3.tmp")
       
def check_and_view_patches():
    f = h.load("test3.tmp")
    p = h.extend(c['defaults'], { "mode" : "complete", "find" : True })
    r = c['patchdir'] + '/'
    cf = "test3.tmp"
    for patch in f:
        print("Checking " + patch)
        m = h.check(patch, p)
        h.write(m, cf)
        h.vcpf(cf, r + patch, p, { "wait" : True })
    
if __name__ == '__main__':
    
    global c, h
    
    exception_handler = ExceptionHandler()
    
    try:
        
        h = Helper('config.json')
        c = h.config
        
        # Find patches that reference tscadc terms
        print('find_patch_refs')
        find_patch_refs()
    
        # Find patches that reference tscadc files
        print('find_patch_refs_2')
        find_patch_refs_2()
        
        
        # Find patches that reference "include/linux/mfd/ti_am335x_tscadc.h"
        print('find_patch_refs_3')
        find_patch_refs_3()
        
        # Now we have a list of the 23 patches that reference the tsc/adc files,
        # and can check each one and view its files
        print('check_and_view_patches')
        check_and_view_patches()
        
    except KeyboardInterrupt:
        pass    
    except Exception as e:
        exception_handler(e)
        exit(-1)
           
    print('done')