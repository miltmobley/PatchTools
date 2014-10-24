'''
Created on May 4, 2014

@copyright 2014, Milton C Mobley

Use the Helper to investigate driver issues.
'''
from patchtools.lib.strings    import Strings
from patchtools.lib.helper     import Helper
from patchtools.lib.exceptions import ExceptionHandler

# Find all ".compatible =' entries in Beagle Black dts files
def find_dts_comps():
    d = "arch/arm/boot/dts/"
    l = [(d + s) for s in ["am33xx.dtsi","am335x-bone-common.dtsi", "am335x-boneblack.dts",
         "am33xx-clocks.dtsi", "tps65217.dtsi"]]
    f = h.find({ "substr" : ["compatible = "] }, { "root_path" : c['sourcedir'], "file_paths" : l })
    h.write(f, "test3.tmp")

def trim_dts_comps():
    ''' dts_comp1.lst requires some post processing, as it contains extraneous text,
        duplicate entries, and one line with two quoted strings, i.e.:
            '"ti,am335x-bone", "ti,am33xx"'.
        Note that some source files have tabs between "compatible =" and the dts symbol.
        We will remove "compatible =" from the test patterns and left strip them to ensure
        that we find all the dts symbols.
    '''
    strings = Strings(h.read("test3.tmp"))
    for index1 in range(len(strings)):
        string = strings[index1]
        index2 = string.find("compatible =")
        if (index2 != -1):
            string = string[index2 + len("compatible ="):]
            string = string.lstrip(' \t').rstrip(';')
            strings[index1] = string
    strings = strings.sort().unique()
    h.write(strings, "test4.tmp")
    
# Make a list of kernel files that could have matching ".compatible =" entries in their of_match tables
def list_compatible_sources():
    p = { "root_path" : c['sourcedir'], "incl_files" : { "suffix" : [".c"] } }
    p1 = h.extend(p, { "incl_dirs" : ["arch/arm"] })
    p2 = h.extend(p, { "excl_dirs" : ["arch", ".git", "Documentation", "staging", "samples", "tools" ] })
    w1 = h.walk(p1)
    w2 = h.walk(p2)
    h.save(w1+w2, "test5.tmp")          

# Find files that reference the compatible items
def find_am335x_drivers():
    p = h.read("test4.tmp") # read compatible = items
    f = h.load("test5.tmp") # load candidate sources
    r = c['sourcedir']
    m = h.find({ "substr" : p },{ "root_path" : r ,"file_paths" : f })
    h.write(m, "test6.tmp")

# Extract file paths, remove duplicates
def filter_driver_list():
    strings = h.read("test6.tmp")
    strings = [string[:string.find(':')] for string in strings]
    strings = Strings(strings).sort().unique()
    h.write(strings, "alldrivers.txt")

if __name__ == '__main__':
    
    global c, h
    
    exception_handler = ExceptionHandler()
    
    try:
        
        h = Helper('config.json')
        c = h.config
        
        print('listing patches ...')
        h.save(h.list_patches(), "test1.tmp")
    
        print('listing sources ...')
        h.save(h.list_sources(), "test2.tmp")
        
        print('finding compatible = ...')
        find_dts_comps()
        
        print('trimming compatible = ...')
        trim_dts_comps()
        
        print('finding compatible = sources ...')
        list_compatible_sources()
    
        print('finding am335x drivers, please wait ...')
        find_am335x_drivers()
        
        print('filtering am335x drivers ...')
        filter_driver_list()
        
        # The final list contains names of 53 am335x related drivers and 16 for other boards
    
    except KeyboardInterrupt:
        pass     
    except Exception as e:
        exception_handler(e)
        exit(-1)
        
    print('done')