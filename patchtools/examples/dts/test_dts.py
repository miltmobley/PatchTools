'''
Created on May 4, 2014

@copyright 2014, Milton C Mobley

Use the Helper to investigate DTS issues. The relevant source files are:
    am335x-bone.dts
    am335x-boneblack.dts
    am335x-bone-common.dtsi
    am33xx.dtsi
    am33xx-clocks.dtsi
    tps65217.dtsi
'''
from patchtools.lib.patchset   import PatchSet
from patchtools.lib.strings    import Strings
from patchtools.lib.helper     import Helper
from patchtools.lib.exceptions import ExceptionHandler

# Find patch refs to the Beagle DTS files    
def find_patch_refs():
    l = h.list_patches(c['defaults'])
    m = { "substr" : ["am33xx.dtsi", "am335x-boneblack.dts", "am335x-bone-common.dtsi",
          "tps65217.dtsi", "am33xx-clocks.dtsi"] }
    f = h.find(m, { "root_path" : c['patchdir'], "file_paths" : l })
    f = [s for s in f if 'diff --git ' in s]
    #g = PatchSet(c['defaults']).sort_patches({ "patches" : f, "order" : "patchset" })
    h.write(f, "test1.tmp")

# Find patch refs using a regular expression. This will also capture references to
# am335x-evm.dts and other files
def find_patch_refs2():
    l = h.list_patches(c['defaults'])
    m = { "regexp" : [r"^.*am33.*\.dts.*$"], "substr" : ["tps65217.dtsi"] }
    f = h.find(m, { "root_path" : c['patchdir'], "file_paths" : l, "format" : "files" })
    f = [s for s in f if 'diff --git ' in s]
    #g = PatchSet(c['defaults']).sort_patches({ "patches" : f, "order" : "patchset" })
    h.save(f, "test2.tmp")

def find_patch_refs3():
    l = h.list_patches(c['defaults'])
    m = { "substr" : [".dts"]}
    f = h.find(m, { "root_path" : c['patchdir'], "file_paths" : l })
    f = [s for s in f if 'diff --git ' in s]
    f = Strings(f).sort().unique()
    h.write(f, "test3.tmp")
        
# Extract patch names
def trim_patch_refs():
    strings = h.read("test1.tmp")
    strings = [string[:string.find(':')] for string in strings]
    strings = Strings(strings).sort().unique()
    h.write(strings, "test3.tmp")
    
# The only source refs to the Beagle DTS files are in the files themselves   

# Verifies the Checker works on all patches
def match_all_patches():
    fl = h.load("test3.tmp")
    for patch in fl:
        #print(patch)
        h.check(patch, h.extend(c['defaults'], { "mode" : "complete", "find" : True }))

# Match each patch, then view its files        
def match_vcpf_each_patch():
    fl = h.load("test3.tmp")
    cp = h.extend(c['defaults'], { "mode" : "complete", "find" : True })
    ep = { "wait" : True }
    pd = c['patchdir'] + '/'
    for patch in fl:
        l = h.check(patch, cp)
        h.write(l, "test4.tmp")
        h.vcpf("test4.tmp", pd + patch, c['defaults'], ep)

# Match one patch, then view its files
def match_vcpf_one_patch():
    f = "resources/0018-bone-renamed-adafruit-RTC-cape.patch"
    l = h.check(f, h.extend(c['defaults'], { "mode" : "complete", "find" : True }))
    h.write(l, "test4.tmp")
    h.vcpf("test4.tmp", c['patchdir'] + '/' + f, c['defaults'])
          
if __name__ == '__main__':
    
    global c, h
    
    exception_handler = ExceptionHandler()
    
    try:
        
        h = Helper('config.json')
        c = h.config
        
        print("find patch refs")
        find_patch_refs()
        #find_patch_refs2()
        #find_patch_refs3()
        
        print("trim patch refs")
        trim_patch_refs()
        '''
        print("match_all_patches")
        match_all_patches()
        
        #print("match_each_patch")
        #match_vcpf_each_patch()
        
        print("match one patch")
        match_vcpf_one_patch()
        '''
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        exception_handler(e)
        exit(-1)
            
    print('done')