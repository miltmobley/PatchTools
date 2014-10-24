'''
Created on May 4, 2014

@copyright 2014, Milton C Mobley

Use the Helper to investigate driver issues.
'''
from patchtools.lib.strings    import Strings
from patchtools.lib.helper     import Helper
from patchtools.lib.exceptions import ExceptionHandler

DTS_TERMS = [
    "ti,am33xx-ecap"
    "ti,am33xx-ehrpwm",
    "ti,am33xx-pwmss"
    ]

PWM_DRIVERS = [
    "drivers/pwm/pwm-tiecap.c",
    "drivers/pwm/pwm-tiehrpwm.c",
    "drivers/pwm/pwm-tipwmss.c"
    ]

def find_patch_refs():
    
    p = h.list_patches()
    f = h.find({ "substr" : DTS_TERMS }, { "root_path" : c['patchdir'], "file_paths" : p })
    h.save(f, "test1.tmp")
    f = h.find({ "substr" : PWM_DRIVERS }, { "root_path" : c['patchdir'], "file_paths" : p })
    h.save(f, "test2.tmp")


if __name__ == '__main__':
    
    global c, h
    
    exception_handler = ExceptionHandler()
    
    try:
        
        h = Helper('config.json')
        c = h.config
        
        find_patch_refs()
    
    except KeyboardInterrupt:
        pass     
    except Exception as e:
        exception_handler(e)
        exit(-1)
        
    print('done')