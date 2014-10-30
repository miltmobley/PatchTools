'''
Created on May 4, 2014

@copyright 2014, Milton C Mobley

Use the Helper to investigate capemgr.c issues.

FYI, capemgr.c patch files in patchset order, as reported by "find_patch_refs" script below:

The files in patchset order:
   not-capebus/0030-capemgr-Beaglebone-capemanager.patch
   not-capebus/0070-capemgr-Remove-__devinit-__devexit.patch
   not-capebus/0103-bone-capemgr-Make-sure-cape-removal-works.patch
   not-capebus/0104-bone-capemgr-Fix-crash-when-trying-to-remove-non-exi.patch
   not-capebus/0116-bone-capemgr-Force-a-slot-to-load-unconditionally.patch
   not-capebus/0128-capemgr-Added-module-param-descriptions.patch
   not-capebus/0151-capemgr-Implement-disable-overrides-on-the-cmd-line.patch
   resetctrl/0002-capemgr-Implement-cape-priorities.patch
   resources/0001-bone-capemgr-Introduce-simple-resource-tracking.patch
   resources/0005-capemgr-Add-enable_partno-parameter.patch
   resources/0023-capemgr-Retry-loading-when-failure-to-find-firmware.patch
   capes/0008-capemgr-Priority-on-capemgr.enable_partno-option.patch
'''
from patchtools.lib.helper     import Helper
from patchtools.lib.exceptions import ExceptionHandler
from patchtools.lib.patchset   import PatchSet

def find_patch_refs():
    l = h.list_patches()
    t = { "substr" : ["cape/beaglebone/capemgr.c"] }
    f = h.find(t, { "root_path" : c['patchdir'], "file_paths" : l, "format" : "files" })
    # Note that find will not return matches in patchset order
    f = PatchSet(c['defaults']).sort_patches({ "patches" : f, "order": "patchset" })
    h.save(f, "test1.tmp")

# Apply the next patch in the series file
def apply_patch():
    h.cmd("cd ./quilt; quilt push -v")

# Apply all patches in the series file
def apply_all():
    h.cmd("cd ./quilt; quilt push -a -v")

def check_patch(patch, output, extra=None):
    p = { "sourcedir" : "quilt", "patchdir" : "quilt/patches", "find" : True }
    m = h.check(patch, p)
    h.write(m, output)
       
# Match not-capebus/0070 against the output of the previous patch
def check_ncb_0070():
    check_patch("not-capebus/0070-capemgr-Remove-__devinit-__devexit.patch",
                "quilt/checks/check_ncb_0070.tmp")

# Match not-capebus/0103 against the output of the previous patch    
def check_ncb_0103():
    check_patch("not-capebus/0103-bone-capemgr-Make-sure-cape-removal-works.patch",
                "quilt/checks/check_ncb_0103.tmp")

# Match not-capebus/0104 against the output of the previous patch 
def check_ncb_0104():
    check_patch("not-capebus/0104-bone-capemgr-Fix-crash-when-trying-to-remove-non-exi.patch",
                "quilt/checks/check_ncb_0104.tmp")
    
# Match not-capebus/0116 against the output of the previous patch 
def check_ncb_0116():
    check_patch("not-capebus/0116-bone-capemgr-Force-a-slot-to-load-unconditionally.patch",
                "quilt/checks/check_ncb_0116.tmp")

# Match not-capebus/0128 against the output of the previous patch
def check_ncb_0128():
    check_patch("not-capebus/0128-capemgr-Added-module-param-descriptions.patch",
                "quilt/checks/check_ncb_0128.tmp")

# Match not-capebus/0151 against the output of the previous patch 
def check_ncb_0151():
    check_patch("not-capebus/0151-capemgr-Implement-disable-overrides-on-the-cmd-line.patch",
                "quilt/checks/check_ncb_0151.tmp")

# Match resetctrl/0002 against the output of the previous patch 
def check_reset_0002():
    check_patch("resetctrl/0002-capemgr-Implement-cape-priorities.patch",
                "quilt/checks/check_reset_0002.tmp")

# Match resources/0001 against the output of the previous patch 
def check_rsrcs_0001():
    check_patch("resources/0001-bone-capemgr-Introduce-simple-resource-tracking.patch",
                "quilt/checks/check_rsrcs_0001.tmp")

# Match resources/0005 against the output of the previous patch 
def check_rsrcs_0005():
    check_patch("resources/0005-capemgr-Add-enable_partno-parameter.patch",
                "quilt/checks/check_rsrcs_0005.tmp")

# Match resources/0023 against the output of the previous patch 
def check_rsrcs_0023():
    check_patch("resources/0023-capemgr-Retry-loading-when-failure-to-find-firmware.patch",
                "quilt/checks/check_rsrcs_0023.tmp",  { "mode" : "complete" })

# Match capes/0008 against the output of the previous patch 
def check_capes_0008():
    check_patch("capes/0008-capemgr-Priority-on-capemgr.enable_partno-option.patch",
                "quilt/checks/check_capes_0008.tmp", { "mode" : "complete" })

def reset_quilt():
    ''' Reset quilt. This must be done each time you start from the first patch.
        Our local copy of the first patch was modified from '--- /dev/null' to
        '--- drivers/.../capemgr.c' to allow this to work.
        '''
    h.cmd("echo \'\' > ./quilt/drivers/misc/cape/beaglebone/capemgr.c")
    h.cmd("echo \'\' > ./quilt/.pc/applied-patches")
        
if __name__ == '__main__':
    
    global c, h
    
    exception_handler = ExceptionHandler()
    
    try:
        
        h = Helper('config.json')
        c = h.config
    
        find_patch_refs()
        
        '''
        # In this section we alternate between applying patches and matching
        # the result against the next patch:
        
        reset_quilt()
        apply_patch()   # Apply not-capebus/0030
        
        check_ncb_0070()
        apply_patch()   # Apply not-capebus/0070
        
        check_ncb_0103()
        apply_patch()   # Apply not-capebus/0103
        
        check_ncb_0104()
        apply_patch()   # Apply not-capebus/0104
        
        check_ncb_0116()
        apply_patch()   # Apply not-capebus/0116
        
        check_ncb_0128()
        apply_patch()   # Apply not-capebus/0128
        
        check_ncb_0151()
        apply_patch()   # Apply not-capebus/0151
        
        check_reset_0002()
        apply_patch()   # Apply resetctrl/0002
        
        check_rsrcs_0001()
        apply_patch()   # Apply resources/0001
        
        check_rsrcs_0005() 
        apply_patch()   # Apply resources/0005
        
        check_rsrcs_0023()
        apply_patch()   # Apply resources/0023
        
        check_capes_0008()
        apply_patch()   # Apply capes/0008
        
        # capemgr.c is now in ./quilt/drivers/misc/cape/beaglebone
        '''
        
        # In this section we use "git am" to apply the patches to the actual kernel source tree
    
        '''
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/not-capebus/0030-capemgr-Beaglebone-capemanager.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/not-capebus/0070-capemgr-Remove-__devinit-__devexit.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/not-capebus/0103-bone-capemgr-Make-sure-cape-removal-works.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/not-capebus/0104-bone-capemgr-Fix-crash-when-trying-to-remove-non-exi.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/not-capebus/0116-bone-capemgr-Force-a-slot-to-load-unconditionally.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/not-capebus/0128-capemgr-Added-module-param-descriptions.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/not-capebus/0151-capemgr-Implement-disable-overrides-on-the-h.cmd-line.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/resetctrl/0002-capemgr-Implement-cape-priorities.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/resources/0001-bone-capemgr-Introduce-simple-resource-tracking.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/resources/0005-capemgr-Add-enable_partno-parameter.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/resources/0023-capemgr-Retry-loading-when-failure-to-find-firmware.patch")
        h.cmd("cd " + c['sourcedir'] + "; git am ../patches/capes/0008-capemgr-Priority-on-capemgr.enable_partno-option.patch")
    
        # capemgr.c is now in drivers/misc/cape/beaglebone under c['sourcedir']
        '''
        '''
        quilt output:
            all patches succeeded, but quilt reported that the last six or so hunks of the last patch
            were shifted to fit, by about 71 lines.
        git am output:
            ...
            resetctrl/0002: warning: 1 line adds whitespace errors.
            ...
            resources/0005: warning: 1 line adds whitespace errors.
                ...
        But all the patches applied successfully
        '''
    
    except KeyboardInterrupt:
        pass 
    except Exception as e:
        exception_handler(e)
        exit(-1)
    
    print('done')