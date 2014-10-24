
Introduction
============

PatchTools is a tool to evaluate patches for inclusion into source trees managed by
the GIT source code control system, notably the Linux kernel. The scenario in which
PatchTools is intended to be used is:

* You have a patch set that was developed on differences detected between an old
  source version "a" and a new source version "b".
  
* You have a different source version "c" to which you wish to apply these patches.

* You don't want to, or can't switch, to an older source version because doing so
  would make important features, bug fixes, etc. disappear.

* You may want to work with snapshot archives of GIT source trees instead of using GIT
  if you don't plan to upstream any changes you make, if you don't plan to make any
  changes, or if you don't want to use GIT for local source code management.

Using "git am" or quilt to apply the patches often will not work because:

* The lines specified in a patch are missing or elsewhere in the same file in tree "c".
* The "a" or "b" file does not exist in a tree where it is supposed to be present.
* The "a" or "b" file is present in a tree where it is supposed to be absent.
* A later patch in your set fails because it depends on an early patch that failed.

Often these problems are caused by the integration of other patches into the "c" source tree
that modified the same files as your patches, thus invalidating the line numbers in
your patches.

PatchTools is primarily designed for use with Linux patches, but can be used with any software system
that uses GIT for source code control.

PatchTools assumes you have appropriate permissions to access any of the files referenced
by PatchTools modules.

PatchTools has been tested on Linux Mint 16, using both Python 2.7.5 and 3.3.


Installation/Setup
===============================

There are two modes of installation: to one of your Python distributions, and as a
stand alone source tree.

Python Installation
-------------------

PatchTools may be installed into one of your Python distributions using pip or easy_install.
It may also be installed from source into a distribution by entering 'sudo python setup.py install'
or 'sudo python3 setup.py install' in a shell while you are located in the root source folder.

If you install to a Python2.x distribution, the Python modules will be placed, for example, in
'/usr/local/lib/Python2.7/dist-packages/patchtools', and there will be a metadata file
'patchtools-1.0-egg-info' file in the same folder to describe the package. The doc and examples
data files will be placed in a '/usr/local/patchtools' folder.

If you install to a Python3.x distribution, the Python modules will be placed, for example,
in '/usr/local/lib/Python3.3/site-packages/patchtools, and there will be a metadata file
'patchtools-1.0-egg-info' file in the same folder to describe the package. The doc and 
examples data files will be placed in the same '/usr/local/patchtools' folder.

Standalone Source
-----------------

To use PatchTools as a stand alone source tree, download the tarball, and extract its files to a suitable
location. Then you must create a PYTHONPATH environment variable as described in the "System Considerations"
section below.

The software may also be imported into an Eclipse-PyDev project using the 'File:Import' menu and the
'File System' option. Ensure that the Eclipse value of PYTHONPATH is set to the parent folder of the
source tree. Note that if you select a Python3 interpreter, the Command module, which is used by the
Viewer, will not be able to launch a gedit that is not Python3 compatible. The causes for this are
unknown, but PyDev is suspected, since such requests work properly in a shell. 

Data Files
----------

After installing PatchTools, you must set up some test data. Due to the large number of files contained
in a Linux kernel, and in some patch sets, test data is not included in the release.
   
In a suitable location create a 'data' folder with these sub folders:
   
   archives
       To hold any patch archive files you download from kernel.org, etc.
   
   patchset
       A folder to contain a tree of patches. You may have more than one such folder,
       if they have different names.
   
Download any patch archive files to the archives folder.
   
Download any patch sets to the patchset folder(s).
   
Download any source trees (e.g. Linux kernels) to convenient locations. It is not
recommended to store a Linux kernel in an Eclipse workspace, due to the large number
of files a kernel contains.
  
Finally create suitable config.json files to describe and link to the data. See the config.json files
in the examples folders for typical contents.
       
    
Modules
=======

You can use PatchTools can speed up the process of determining suitability of your patches
to a new kernel by:

* Using the *Walker* to enumerate a useful subset of files in your kernel tree.

* Using the *Finder* to identify files that have specific content.

* Using the *Checker* to determine the compatibility of the patch info to your target kernel.
  
* Using the *Watcher* to monitor patch archive files distributed with newer kernels.

* Using the *Viewer* to edit related files simultaneously.

* Using the *Helper* utilities to speed development of these procedures.

	
Major Modules
-------------

The finder module implements a class *Finder* to facilitate searching file trees for patterns of interest to you.

The checker module implements a class *Checker* to compare the contents of patch
files to the source files they reference. *Checker* objects can be used to determine if
the changes in a patch are compatible with your target kernel.

The viewer module implements a class *Viewer* to facilitate editing patches and the files they
reference. Methods are implemented to handle special cases such as displaying a patch and
the files referenced by the patch.

The walker module implements a class *Walker* to allow enumeration of selected directories and files
in a file tree. Both directories and specific file types may be included in or excluded from the results.

The watcher module implements a class *Watcher* to compare the contents of patch
files to a "patch archive" file associated with a kernel release. You can use the *Watcher*
to determine if any of your patches have been integrated into newer kernels than the one on
which the patches were developed.

The helper module implements a class *Helper* to ease the task of assembling the fairly
numerous required and optional parameters of the modules listed above. It provides wrapper
functions for the modules, and some useful utility functions.

Supporting Modules
------------------

The archive module implements a class *Archive* to extract information from "patch archive" files
associated with kernel releases.

The command module implements a class *Command* to provide a simple wrapper for the Python subprocess module.

The functions module implements a class *Functions* to provide various utility functions.

The jsonconfig module implements a class *JSONConfig* to allow application configuration
using enhanced JSON data files.

The strings module implements a class *Strings* to provide useful string like methods for
lists of strings.


Archive
-------

Archive objects are used by the *Watcher* to extract information from "patch archive" files
provided by kernel.org for their kernel releases. The files contain a list of the patch diff
sections that were applied to obtain the release version. See Appendix B for more information.


Checker
-------

*Checker* objects compare the contents of patch files to the source files they reference.
Checker objects are used to determine if the changes in a patch are compatible with your target kernel.

The *Checker* class accomplishes its goals by the following steps:

* The patch file is read and parsed into a Patch object.

* The path specifications in the 'diff' sections are verified to match, and the files
  they reference to exist or not exist in the source tree as appropriate.

* The line number specifications in the 'hunks' are verified to fall within
  the numbers of actual lines in the files they reference.

* The edit changes are tested against the "c" version of file.

The *Checker* has two primary modes of operation:

* In 'full' mode, all errors are reported, but lines that passed testing are not.

* In 'complete' mode, a status is reported for each hunk edit line.

The *Checker* has several optional features:

* If the 'find' option is True, the code will attempt to find missing lines in the
  target file. If no matches are found in a hunk, the program will attempt to find
  instances of the hunk's 'note' in the target file. But the search is limited to
  'landmark' lines, i.e. those lines that are expected to be unique in the file.
  Due to the complexity of typical C code, non relevant matches may be reported
  even for complicated expressions.

* The 'targets' option can be used to limit checking to diffs that reference specific files.

See the 'Checker' section of the API documentation for call details.
  
Additional Notes
................

Since various mail systems and editors can corrupt the patch files as they are in transit,
the *Checker* normalizes the patch path lines ("--- ...", "+++ ..."), the 'diff' lines
("diff --git ...") and the hunk range lines ("@@ ...") before splitting them
for extraction. The normalization consists of replacing all tabs by spaces
and replacing multiple spaces between words of a line by single spaces.

The *Patch* parsing logic will discard any patch lines that have been commented out by surrounding them
with lines containing only '"""'. See the 'Patch' section of the API documentation for
more details. This feature can be used to narrow the focus of your investigation to a small
set of patches and files. But if you plan to use 'git am' on a patch later, you should do
the commenting in a copy of the patch.

Usage
.....

To start a test against your target kernel, you may execute::

    f = h.load("dts_patch_refs.lst")
    m = h.check(f, h.extend(c['defaults'], { "mode" : "full", "find" : False, }))
    h.write(m, "match_dts.txt")
    
Assuming that you have used the *Finder* to locate patches that refer to some DTS files,
and saved the results into "dts_patch_refs.lst", this code will check those patches against
your kernel version.

See the 'Checker' section of the API documentation for further info on its parameters
and methods.

See 'Appendix E - Checker Output' for explanation of *Checker* output.
 

Recommended Usage Strategy
..........................

If the *Checker* is used on all patches in a large set, it can provide you with a very large amount
of bad news concerning the state of your patches, in part because it does not take into account
dependencies between patches. It is useful to narrow the scope of your investigations to a subsystem,
group of patches or group of files to analyze. If you decide to fix a series of related patches,
you should fix the first one in commit order, test the others again to see if any problems have been
resolved, and repeat this process down to the last patch.

The *Walker* and *Finder* can be used to generate small lists of files related to specific subsystems, based
on matches to text strings such as "am33xx", etc::

    l = h.load("patch_names.lst")
    m = { "substr" : ["am335x-bone", "am33xx.dtsi", "tps65217.dtsi" ],
    f = h.find(m, { "root_path" : c['patchdir'], "file_paths" : l, "format" : "files" })',
    h.save(f, "dts_patch_refs.lst")'

The *Checker* can be used on one or a few of these files at a time::

    f = h.load("dts_patch_refs.lst")
    g = h.PatchSet(c['defaults']).sort_patches({ "patches" : f, "order" : "patchset" })
    h = h.check(g, c['defaults'] + { "find" : True })

Note that the *Walker* and *Finder* do not return lists of patch names in patchset order, which is supposed
to be the commit order needed for successful use of 'git am'.

If the *Checker* 'targets' option is used, the *Checker* will only scan diff sections that modify the files
specified in the targets list. For example, you could select BeagleBoard related device tree files for investigation::

    f = h.load("dts_patch_refs.lst")
    g = h.PatchSet(c['defaults']).sort_patches({ "patches" : f, "order" : "patchset" })
    t = ["am335x-bone.dts", "am335x-boneblack.dts", "am335x-bone-common.dtsi",
         "am33xx.dtsi", "am33xx-clocks.dtsi", "tps65217.dtsi", "Makefile"]
    d = h.check(g, h.extend(c['defaults'], { "find" : True, "targets" : t }))
    h.write(d, "dts_matches.txt")'

When the *Checker* encounters a diff file name that is not in its targets list, it will issue a message like::

    # SKIPPING DIFF: "diff --git a/arch/arm/boot/dts/am335x-bone.dts ...

The *Patch* module used by the *Checker* to parse patches will discard any patch lines that are surrounded
by lines containing only '"""'. If you observe that an initial *Checker* report indicates that all the errors
in a hunk are like '"delete" line not found' or '"merge" line not found' and that the target file does not have
the specified "delete" lines, or that "add" lines are already in the target file, you can comment out the diff
or hunk to further narrow the scope of your investigation to hunks or diffs that actually need to be fixed.
This strategy was used heavily in Example 5 described below.

If all diffs in a patch are commented out, the *Checker* will issue a message like::

    INFO:  skipping empty patch

Some example uses of this feature are:

    To comment out a diff for a file in which you are not interested::

        """
        N/U not BeagleBone Black files
        diff --git a/arch/arm/boot/dts/am335x-bone.dts b/arch/arm/boot/dts/am335x-bone.dts
        ...
        """

    To comment out a diff or a hunk which is not needed::

        """
        N/N am33xx.dtsi has the add lines and more values
        diff --git a/arch/arm/boot/dts/am33xx.dtsi b/arch/arm/boot/dts/am33xx.dtsi
        ...
        """

The use of 'N/N' and other codes to start explanatory notes is conventional, and is not interpreted by the software.

The 'vcpf' (view checker output, patch and its files) function of the *Helper* can be very helpful in determining
if a patch is correct or if it is needed.

See the files in the "examples" folder for complete usage examples.


Command
-------

Command objects provide a simple wrapper for the Python subprocess module.
Command execution can be synchronous, or asynchronous. Normally, synchronous mode
will be used by the *Helper*, except that most of its view commands use asynchronous mode.

Commands may be passed as strings or as lists of arguments.

Command strings are executed in shell mode::

    cd ~;pwd;ls

There appear to be some limitations to this approach, as in a command string like::
        
    cd ~; source .profile;cdlsk
    
where 'cdlsk' is an alias defined in .profile:

* The shell will not be able to find .profile unless you reference it as './.profile'
    or '~/.profile'.

* The 'cdlsk' alias will not be recognized.

* You cannot split the command into multiple invocations because the environment created
  by 'source ./.profile' will be lost when the sub process exits.

* Commands that normally produce output organized in columns in an interactive shell,
  e.g. 'ls', will instead produce a list of items separated by '\\n' characters.

The usage of stdout and stderr by Linux programs is variable, for example:

   * bash may return zero, indicating success, but also return error output.
   * wget returns normal output on stderr.

Some programs use extended ASCII (aka Latin-1) characters (i.e. ord(ch) >= \x80 in Python terms)
in their output. For example, certain commands surround filenames with left single
quote and right single quote characters. Even though Eclipse and PyDev can display such
characters, Python3 will convert them to hexadecimal escape sequences (e.g. lsquo is represented as '\\xe2\\x80\\x98').
The *Command* class converts lsquo and rsquo to ' as needed.

Python2.7 returns stdout and stderr data as strings, while Python3.x returns them as byte arrays.
Command translates the values to strings as needed.

See the 'Command' section of the API for call details.


Finder
------

*Finder* objects try to find references to patterns you specify in a file or a file tree.
For each pattern you select, the *Finder* will return a list of references it finds in the target file or folder.

Unlike programs such as ctags and cscope, the *Finder* does not attempt to index your entire software tree,
but instead focuses on the folders, files and text patterns you specify.

Either absolute or relative paths may be used in specifying the search root.
When relative paths are used, they must be accessible from the caller's current directory.
    
Using common patterns such as 'dma' may produce a large amount of output,
particularly if you set the search root to the root of a kernel tree, so your choices of
root and patterns should be made with care.

See the 'Finder' section of the API documentation for more information on the class methods.


JSONConfig
----------

A *JSONConfig* object holds application configuration data taken from enhanced JSON encoded files.

The JSON files may contain line comments and block comments.

Line comments are lines that start with '#' (ignoring leading white space),
and will be removed in file loading.

Block comments are coded by inserting a line with only """ before and after the lines to be commented out.
Any lines between such lines are removed in file loading.

Once loaded the object may be accessed by key indexing of its dict super class instance, or by use of
the get and set methods. These two methods support convenient multilevel indexing by the use of
"path expressions". For example, '...get("mysql_options/admin_profile/data_base"' will
return the value of self["mysql_options"]["admin_profile"]["data_base"]. The user can specify the path
separator character in the 'separator' option passed to the constructor.

Python's JSON loader strictly requires the data to have correct JSON syntax, and will
generate exceptions if it doesn't. To avoid confusing users by presenting them with
line numbers in the stripped line set, JSONConfig will catch exceptions raised by the JSON decoder,
map the exception line numbers back to their equivalents in the original file,
and reraise the exceptions as JSONConfigError objects.

On Python 2.x, the get method will translate unicode dict values to str objects.

See the 'JSONConfig' section of the API doumentation for call details.

See the test*.py programs in the examples folder, and the '__init__' method of the *Helper* for typical usage.


Matcher
-------

*Matcher* objects match strings to patterns. Used by the *Walker* to filter file names
and the *Finder* to filter text strings, the *Filter* allows you to specify match patterns by:

    match
        a list of exact match patterns
    prefix
        a list of prefix patterns
    suffix
        a list of suffix patterns
    substr
        a list of substring patterns
    regexp
        a list of regular expression patterns
    funcs
        a list of callback functions
        
Patterns are tested against strings in the order shown above.

Some examples::

    f1 = Matcher({ "prefix" : ["Kconfig", "Makefile"] })
    f2 = Matcher({ "suffix" : [".dts",".dtsi"] })   
    f3 = Matcher({ "substr" : ["am33xx.dtsi", "am335x-bone.dts", "am335x-boneblack.dts",
          "am335x-bone-common.dtsi", "am33xx_pwm-00A0.dts", "bone_pwm_P8_13-00A0.dts" ] })
    f4 = Matcher({ "regexp" : [r".*am335x\-b.*\.dts.*", r".*am33xx.*\.dts.*", r".*bone.*\.dts.*"] })

Parameters like f1 can be used by the *Walker* to find all files whose names begin with "Kconfig" or "Makefile"
in the folders you told it to search.

Parameters like f2 can be used by the *Walker* to find all files whose names end with ".dts" or ".dtsi".

Parameters like f3 or f4 can be used by the *Finder* to find all references to the specified strings in your patch
or source files.

Using regular expressions may eliminate the need to use line continuations, but it can be difficult to formulate
expressions that produce exactly the same result as simpler combinations of 'substr', etc.

The 'encoding' example shows how to use callback functions to select files for testing.

See the 'Matcher' section of the API documentation for call details.


Patch
-----

Patch objects parse the strings of a patch file into an object suitable for analysis.
The object will contain a list of Diff objects.

Patch objects will discard any patch lines that have been commented out by surrounding them
with lines containing only '"""'. If you plan to use 'git am' on a patch later, you should
do the commenting in a copy of the patch.

See the 'Patch' section of the API documentation for call details.

See checker.py for example usage of the Patch class.


PatchSet
--------

Patch sets are normally organized in two level trees, with a root folder and sub directories
for specific topics, e.g. 'dma'. The 'name' of a patch consists of its subdirectory name
joined to its file name by  '/'.

A patch set description is a dict that specifes the order in which the patches are to be applied.
Its 'groups' element is a list of the topic specific sub folders mentioned above. Within each
sub folder, patches are intended to be applied in the order indicated by the first four characters
of the patch file names. This order was encoded by using 'git format-patch' or quilt to format
the patches.


Strings
-------

Strings objects provide useful string like methods for lists of strings.

Note that taking a slice of a Strings object will always return a Strings object.

Strings is used by the Watcher class, as well as by the Diff, Hunk and Patch classes.
See those files and the examples files for more usage examples.


Viewer
------

Viewer objects allow you to view sets of related files, using graphical or nongraphical editors.

The default editor on Linux is 'gedit', which allows numerous files to be displayed in a single window.

The editor default can be overridden by passing an editor specification to the constructor,
as shown in the API section below.


Walker
------

Walker objects walk a file tree and return the path of each discovered file.
Directory and file filters may be applied to narrow the scope of a search in a large file tree.


Watcher
-------

Watcher objects facilitate viewing diff sections in your patch files, diff sections in "patch archive"
files, and the source files they reference. Patch archive files contain all the diff sections that
were applied to the previous version of a kernel to obtain a new version.

See the 'archives' folder in the examples for typical usage.

Helper
------

Helper objects facilitate use of PatchTools's tools, which have many required and
optional parameters. The *Helper* provides wrapper functions for PatchTools classes,
and some useful utility functions.

Command Summary
...............

Utility functions
~~~~~~~~~~~~~~~~~

load
    load JSON data into a variable from a file
save
    save a variable to a file as JSON string
read
    read list of strings from a file into a variable
write
    write a variable to a file as a list of strings

Wrapper functions
~~~~~~~~~~~~~~~~~

cmd
    run *Command* to execute shell command synchronously
find
    run *Finder* to find patterns in files
check
    run *Checker* to check patch file(s) against source tree
view
    display selected file[s]
vp2f
    display patch and files it uses
vf2p
    display file and patches that use it
vp2p
    display patch and other patches that use the same files
vp2a
    display patch and related patch archive diff sections
vcpf
    display *Checker* output file, one patch file and the files referenced by the patch file
walk
    run *Walker*  to generate a list of files for *Finder*, etc.
watch
    run *Watcher* to detect integration of patches into released kernels

The *Helper* constructor creates a 'defaults' item in the application's config data object,
using the values of 'sourcedir', 'patchdir', etc., found in the data, and subsequently
uses it in calls to wrapper functions where the caller does not provide a parameters object.

See the 'Helper'  section of the API documentation for futher info.


Configuration
=============

Many operations use configuration data that is loaded into a JSONConfig object during
initialization. Items specified in the configuration data include the location of the
source tree and of the patches directory. A description of the patch set may also be
stored there.

See the 'config.json' file for an example, and the 'JSONConfig' section of the
API documentation.


Exceptions
==========

PatchTools objects are intended to be embedded in Python scripts, which can have various
exception reporting and logging schemes. Consequently PatchTools classes generally do not
catch exceptions except to translate them to other exceptions. For example, JSONConfig objects
catch 'KeyError' exceptions generated by Python's json module, and map their line numbers to
those used in the source file, which may have different line numbers due to comment lines.

The exceptions.py file provides an ExceptionHandler class which can be used to print
exception reports.

PatchTools classes uniformly use exceptions to report errors, for example parameter errors,
while return values are used to deliver valid result data to the caller. The exceptions are defined
in exception.py.

See the example files for a simple exception handling scheme.


System Considerations
=====================

All modules encode file paths in Unix style using '/' characters.

The functions module determines if the Python version is 3.x when it is loaded.
The Python version can then be obtained by other modules by calling the Functions.is_python3 method.

If PatchTools is not installed in your Python installation, and you are not using Eclipse,
you must specify the PYTHONPATH environment variable to allow Python to find the PatchTools modules.
The easiest way to do this is to export the definition from your .profile file::

   export PYTHONPATH="$HOME/Projects/Eclipse/Linux/PatchTools"

Then you can run test programs from any location.

Eclipse-PyDev will define a PYTHONPATH variously according to the settings you choose when creating
your project. The PYTHONPATH value should include the parent folder of the 'patchtools' source
folder, as in the setting above.

Linux reportedly has adopted UTF-8 as the default text encoding, but some Linux kernel files contain
'Latin_1' characters whose numeric values are greater than 127, and are not valid UTF-8 start bytes.
Consequently the file access methods in the Functions class default to 'Latin_1' encoding.

Examples
========

This section shows typical usage of PatchTools classes and the *Helper* class.

See the folders in the 'examples' tree for the example code referenced below.

Example 1 -- Basic Features
---------------------------

This example shows the usage of many of the features described above.

Suppose we want to create a source file list for the *Finder* that enumerates selected files
in the kernel tree, but excludes the '.git' folder and any folders in 'arch' other than
'arch/arm'. This script will do the job::

    f = { "suffix" : [".c","h"], "prefix": ["Makefile","Kconfig"] }
    p = { "root_path" : c['sourcedir'], "incl_files" : f }
    excl = { "excl_dirs" : [".git","arch"] }
    incl = { "incl_dirs" : ["arch/arm"] }
    p1 = h.extend(p, incl)
    p2 = h.extend(p, excl)
    w = h.walk(p1) + walk(p2)
    h.save(w, c['logdir'] + "/src_files.txt")
    
Lines 1-4 create some dict variables to include in the parameters for the walk operations.

Lines 5 and 6 combine these dicts to make the final parameter dicts.

Line 7 executes the walk function on each parameter dict and combines their output.

Line 8 writes the data to a file for future use.

Running a script like this at the start of a project can substantially reduce the time required
for subsequent *Finder* operations.

Example 2 -- Viewer 1
---------------------

In this example we want to assess the difficulty of porting some patch changes to our kernel by displaying
a *Checker* output file, a kernel source file, and the patches that modify the source file::

    h.view(c['logdir'] + "/match_a.log")
    h.vf2p("arch/arm/boot/dts/am33xx.dtsi")
    
If the 'gedit' editor is used (the Linux default editor), all the files will be displayed in a single window,
in the following order for this example:

    * The source file
    * The patch files in patchset group order, which is presumably their commit order.
  
We observe that searching for 'am33xx.dtsi' at the top of the *Checker* output file takes us to the report
for patch "dma/0018...", which is the first patch file displayed by gedit.

The Viewer classes normally launch the editor in asynchronous (nowait) mode, which allows users to enter two commands
like the ones above without being blocked at the first command.

Example 3 -- Viewer 2
---------------------

This example shows how the wait/nowait feature of the Viewer classes could be used to display a patch file,
its corresponding *Checker* output file, and the files referenced by the patch, one at a time::

    p = c['patchdir'] + "/adc/0002-input-ti_am33x_tsc-Step-enable-bits-made-configurabl.patch"
    m = h.check(p)
    f = "matcher.txt"
    h.write(m, f)
    v = { "wait" : True }
    a = c['sourcedir'] + "/drivers/iio/adc/ti_am335x_adc.c"
    b = c['sourcedir'] + "/drivers/input/touchscreen/ti_am335x_tsc.c"
    c = c['sourcedir'] + "/drivers/mfd/ti_am335x_tscadc.c"
    d = c['sourcedir'] + "/include/linux/mfd/ti_am335x_tscadc.h"
    h.view([p,f,a],v)
    h.view([p,f,b],v)
    h.view([p,f,c],v)
    h.view([p,f,d],v)

In this scenario, each view command will block until its editor is closed.

Example 4 -- AM33XX Drivers
---------------------------

In this example we will identify all the drivers used to control the Beagle's AM335X processor by cross referencing
"compatible =" items in the Beagle's .dts files to ".compatible =" items in the "of_match" tables of the kernel source files.

First we will find the dts compatible items::

    d = "arch/arm/boot/dts/"
    l = [(d + s) for s in ["am33xx.dtsi","am335x-bone-common.dtsi", "am335x-boneblack.dts",
         "am33xx-clocks.dtsi", "tps65217.dtsi"]]
    f = h.find({ "substr" : ["compatible = "] }, { "root_path" : c['sourcedir'], "file_paths" : l })
    h.write(f, "test3.txt")

test3.txt requires some post processing, as it contains extraneous text and duplicate entries.
The *Helper's* write method was used to save the list as '\\n' terminated strings, so this task can be
automated::

    strings = Strings(h.read("test3.txt"))
    strings = strings.ltrim("compatible = ").rtrim(';').sort().unique()
    h.write(strings, "test4.txt")

Next we will list the kernel source files that might contain the corresponding entries in their of_match tables::

    p = { "root_path" : c['sourcedir'], "incl_files" : { "suffix" : [".c"] } }
    p1 = h.extend(p, { "incl_dirs" : ["arch/arm"] })
    p2 = h.extend(p, { "excl_dirs" : ["arch", ".git", "Documentation", "staging", "samples", "tools" ] })
    w1 = h.walk(p1)
    w2 = h.walk(p2)
    h.save(w1+w2, "test5.txt")

In this code the output was saved as a JSON object to allow using it as pattern parameters for the
following find operation.          

Finally we will match the patterns in "test4.txt" to the source files::

    p = h.read("test4.txt") # read compatible = items
    f = h.load("test5.txt") # load candidate sources
    r = c['sourcedir']
    m = h.find({ "substr" : p },{ "root_path" : r ,"file_paths" : f })
    h.write(m, "test6.txt")

Again some editing of the output file "test6.txt" is needed to eliminate extraneous
text and duplicates::

    strings = h.read("test6.txt")
    strings = [string[:string.find(':')] for string in strings]
    strings = Strings(strings).sort().unique()
    h.write(strings, "am335x_drivers.lst")

The final list contains 36 am335x related drivers that are used to control the Beagle board.
The list can be saved and passed to the *Checker* as a 'targets' option, or to the *Watcher*
to be run whenever a new kernel version is released by kernel.org.

Example 5 -- DTS Study
----------------------

The ARM community, including Texas Instruments and the Beagle developers, have been making substantial
progress in the last year or two in adopting the "Device Tree" system for their products. It is possible that,
although they have submitted many patches related to this effort, not all the patches have been integrated
into our target kernel. In this example we will investigate the state of Beagle related .dts and .dtsi files
in the patches and the kernel.

Examination of the kernel's '/arch/arm/boot/dts' folder shows that there are several files related to our
target device, the BeagleBone Black:

    * am335x-boneblack.dts
    * am335x-bone-common.dtsi
    * am33xx.dtsi
    * am33xx-clocks.dtsi
    * tps65217.dtsi

We can find all the patches that touch these files with this *Helper* script::

    l = h.list_patches()
    p = { "substr" : ["am33xx.dtsi", "am335x-boneblack.dts", "am335x-bone-common.dtsi",
                      "tps65217.dtsi", "am33xx-clocks.dtsi"] }
    f = find(p, { "root_path" : c['patchdir'], "file_paths" : l, "format" : "files" })
    g = h.PatchSet(c['defaults']).sort_patches({ "patches" : f, "order" : "patchset" })
    h.save(g, "dts_patch_refs.lst")

The first and sixth lines show use of the *Helper's* utility functions, 'list_patches' and 'save'.

The fourth line shows use of one of the *Helper's* class wrapper functions, 'find'. The "files"
option tells the *Finder* to return only filenames, with no duplicates.

See the API sections for descriptions of the functions, classes and parameters used.

Now we have the file "dts_patch_refs.lst", which contains the names of 76 patches that touch the files.
From here we can use the *Helper*'s view commands to view the patches individually, and the files they use.
For example::

    h.vp2f("pm/0062-ARM-OMAP2-AM33XX-timer-Interchance-clkevt-and-clksrc.patch")

The files can also be compared against a *Checker* output file by using the 'vcpf' command::

    h.vcpf("check.log", "pm/0062-ARM-OMAP2-AM33XX-timer-Interchance-clkevt-and-clksrc.patch")
   
If the default editor 'gedit' is used, all the files for a single command will appear in one window.

Inspecting the files in this way could take considerable time, but this process can be accelerated
by using a *Helper* script like this::

   fl = h.load("dts_patch_refs.lst")
   cp = h.extend(c['defaults'], { "mode" : "complete", "find" : True })
   ep = { "wait" : True }
   pd = c['patchdir'] + '/'
   for patch in fl:
       l = h.check(patch, cp)
       h.write(l, test6.txt")
       h.vcpf("test6.txt", pd + patch, c['defaults'], ep)

After checking the 76 patches we find that:

    * 27 of the patches specify changes that are already in the kernel, so the patches can be ignored.
    * Another 28 of the patches relate to features we won't use, i.e. certain capes, so these patches can also be ignored.
    * One patch definitely needs to be fixed.
    * 21 patches need fixing if we will use their features, e.g. AM335 reset control or TI's PM firmware.
    * One patch has an undesirable modification of generic kernel files to work around a device specific problem,
      and should be redone.

See the 'report.txt' file in the examples/alldrivers folder for details.

Similar investigations can be done for subsystems you may be interested in, e.g. dma, adc, gpio, etc.,
with comparable results.


Example 6 -- TSC/ADC Study
--------------------------

In this example we look into the appropriateness of patches that modify the touch screen control (TSC)
and analog-digital converter (ADC) control logic in the kernel and driver files. We will use the *Helper*
to facilitate the investigation.

First we find patches that relate to terms such as "tscadc","tsc" and "adc". But we use search terms
such as "adc.c" to exclude extraneous matches to words containing those terms::

   l = h.list_patches()
   p = { "substr" : ["tscadc.c","tscadc.h","tsc.c","tsc.h","adc.c","adc.h"] }
   f = h.find(p, { "root_path" : c['patchdir'], "file_paths" : l, "format" : "full" })
   h.save(f, "patch_refs.lst")
   
Inspection of "patch_refs.lst" shows these files are touched by the patches:
   (1) drivers/iio/adc/ti_am335x_adc.c
   (2) drivers/input/touchscreen/ti_am335x_tsc.c
   (3) drivers/mfd/ti_am335x_tscadc.c
   (4) include/linux/mfd/ti_am335x_tscadc.h
   (5) include/linux/input/ti_am335x_tsc.h
   (6) include/linux/clk-provider.h   

Next we make a list of the  patches that touch each file, without duplicates::

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
   h.save(s, "patch_refs2.lst")
   
The "patch_refs2.lst" file now contains the names of 23 patches that touch the files. We can use
the *Checker* and *Viewer* to examine the patches and files::

    f = h.load("patch_refs2.lst")
    p = h.extend(c['defaults'], { "mode" : "complete", "find" : True })
    r = c['patchdir'] + '/'
    cf = "../test/test6.txt"
    for patch in f:
        m = h.check(patch, p)
        h.write(m, cf)
        h.vcpf(cf, r + patch, p, { "wait" : True })

The results have been summarized in the file "report.txt" in the examples/tsc_adc folder. See the Notes
section at the bottom of that file for an explanation of the codes used.

We see that although the majority of diff and hunk sections are marked "N/N" (not needed), a significant
minority are indicated to need fixing. Some of these only need to have their line numbers adjusted to fit
the target code, but others have more serious problems. In particular, certain features such as enhancing
interrupt logic and adding work queues have not been integrated into the target kernel drivers. In other cases,
the changes requested by some patches may have been obsoleted by other patches that were integrated into
the kernel.

The situation is more complicated than was the case in the DTS study, and more investigation is needed.
However we can drop further consideration of all the patch sections marked "N/N" or "N/U", and focus on the
remaining sections. The best approach may be to use the existing versions of the target files,
and only fix and apply the patch sections that affect our project.

Example 7 -- Cape Manager Study
-------------------------------

The BeagleBone board developers have devised a sytem to allow accessory boards that to be plugged into
a Beagle board using its GPIO connectors, and have supported the development of a kernel mode file
'capemgr.c' to provide some control of such boards. The patches that created and enhanced the file have
not been integrated into the target kernel, so the file is not found there. In this example, we
investigate the use of 'git am' command and the patch utility to recreate the file from the patches.

See the examples/capemgr folder for the code, and Appendix D - Checker vs. quilt vs 'git am'
for a discussion of the results. The generated file is found under the examples/capemgr/quilt folder.


Classes API
===========

Complete documentation of the API's of the *Helper* and PatchTools classes is provided below.


Archive
-------

Extract information from "patch archive" files

Archive(path)
.............

Constructor

|        Args:
|            path (string): path to patch archive file
|            
|        Raises:
|            PT_ParameterError, PT_NotFoundError
|        
|        Notes:
|             A "patch archive" file lists diff sections from patches that were applied to
|             produce the associated kernel version. Since the patch archive files can be very large,
|             we take care to avoid copying or storing data that is not of interest to the user.

sections(filenames)
...................

Find archive file sections that modify files also modified by our patches

|        Args:
|            filenames (list): file names referenced in our patches
|            
|        Returns:
|            A list of sections. Each section is a list of strings, in which
|            the first string identifies the start line number of a diff section,
|            and the remaining strings are the content of the diff section.
|            
|        Raises:
|            None


Checker
-------

Validate the contents of Linux kernel patch files against
the files specified in them

Checker(params)
...............

Constructor

|        Args:
|            params (dict): parameters
|                sourcedir  (string,required):       path to source directory
|                patchdir   (string,required):       path to patch directory
|                targets    (string/list, optional): target file(s)
|                indent     (int, optional):         indentation
|                    default = 3
|                mode (string, optional): scanning mode
|                    'full'     : report edit errors only
|                    'complete' : report status of all edits
|                    default is 'full' 
|                find (bool, optional): find missing strings
|                    default is True
|                debug (int, optional) debug options
|                    default is 0
|            
|        Raises:
|            PT_ParameterError
|                    
|        Notes:
|            If '' is passed as sourcedir or patchdir, the caller must supply file
|            paths to the match method that are accessible from the caller's current dircectory.
|                
|            If 'targets' is specified the code will only scan diff sections that
|            modify the filenames in params['targets]

match(param)
............

Validate the contents of one or more Linux kernel patch files against a kernel

|        Args:
|            param (choice):
|                (string): path to patch file
|                (list): paths to patch files
|                
|        Returns:
|            A list of strings describing the results of analysis
|        
|        Raises:
|            PT_ParameterError
|            PT_ParsingError


Finder
------

Find references to patterns you specify in a Linux kernel tree,
a patch archive file, or in a set of patches

Finder(params)
..............

Constructor

|        Args:
|            params (dict): parameters
|                root_path   (string, required): path of file tree root
|                file_paths  (list, required):   relative paths of files to search
|                options (string, optional): display format
|                    'terse'    show count of matching lines
|                    'compact'  show line numbers of matching lines
|                    'full'     show line number and text of matching lines
|                    'complete' also show matching pattern
|                    'match'    list only matching text
|                        default is 'full'
|                mode (string, optional) search mode
|                    'file' report results by file
|                    'pattern' report results by pattern
|                
|                trim_paths (bool, optional): remove root portion of paths from returned paths
|                    default is True
|                      
|        Raises:
|            PT_ParameterError
|            PT_NotFoundError

match(params)
.............

Report matches by file to (patterns) found in selected files

|        Args:
|            filter (dict): Filter parameters
|                
|        Returns:
|            A list of matches in the format specified above
|        
|        Raises:
|            PT_ParameterError
|                
|        Notes:
|            See the Filter object for a description of Filter parameters.


Viewer
------

Display a set of files in a user selected editor

Viewer(params=None)
...................

Constructor

|        Args:
|            params (dict, optional): parameters
|                editor (dict, optional): editor specification
|                    target    (string, required): name or path for target program
|                    multifile (bool, required):   can open multiple files in a single invocation
|                    multiview (bool, required):   can display multiple files in a single window
|                root (string, optional): a path to prefix to all filenames
|                wait (bool, optional):   wait for subprocess to exit
|                    default is False
|            
|        Raises:
|            PT_ParameterError
|                
|        Notes:
|            If editor is not specified, the default editor for the host system is used.
|            The default editor for Linux is gedit. The default editor for Windows is write
|            (aka 'WordPad').
|            If any method is called in a loop, the wait option should be True.

view(files)
...........

Launch specified editor to view the file(s)

|        Args:
|            files (list): paths of files to display
|            check_files(bool): verify target files exist
|                          
|        Raises:
|            PT_ParameterError for any missing files

vp2f(patchname, params)
.......................

List patch and files it uses

|        Args:
|            patchname (string): name of patch file
|            params    (dict):   parameters
|                patchdir  (string, required): path of patches folder
|                
|        Raises:
|            PT_ParameterError for any missing files

vp2p(patchname, params)
.......................

Display a patch file and the other patch files that use the same source files

|        Args:
|            patchname (string): name of patch file
|            params    (dict):   parameters
|                patchdir  (string, required): path of patches folder
|                patchset  (dict, required):   patchset description
|                
|        Raises:    
|            PT_ParameterError for any missing files

vp2a(patchname, archpath, params)
.................................

Display patch and archive diff sections that use its files

|        Args:
|            patchname (string): name of patch file
|            archpath  (string): path to archive file
|            params    (dict):   parameters
|                patchdir (string, required): path of patches folder
|                tempdir  (string, required): path to store temporary data
|                
|        Raises:    
|            PT_ParameterError for any missing files
|        
|        Notes:
|            Launches the editor synchronously, since a temporary file is created to hold
|            the archive sections.

vcpf(checkpath, patchname, params)
..................................

List checker output file, patch and files it uses

|        Args:
|            checkpath (string): path to Checker output file
|            patchname (string): patch name
|            params (dict) parameters:
|                sourcedir (string, required): path of sources folder
|                patchdir  (string, required): path of patches folder
|            
|        Raises:    
|            PT_ParameterError
|            PT_NotFoundError


Walker
------

Enumerate paths of selected files in a source tree

Walker(params)
..............

Constructor

|        Args:
|            params (dict, required)  parameters:
|                root_path  (string, required): search root path
|                incl_dirs  (list, optional):   top level subdirs to include
|                excl_dirs  (list, optional):   top level subdirs to exclude
|                incl_files (dict, optional):   include file name filters
|                excl_files (dict, optional):   exclude file name filters
|                test_dirs  (bool, optional):   True = include dir in tests
|                    
|        Raises:
|            PT_ParameterError
|            
|        Notes:
|            The "root_path" parameter specifies the root of the search.
|            If the "incl_dirs" option is specified, only those subdirs of the root will be searched.
|            If the "excl_dirs" option is specified, those subdirs of the root will not be searched.
|            If the "incl_files" option is specified, only those filetypes will be enumerated.
|            If the "excl_files" option is specified, those filetypes will not be enumerated.
|            If it is desired to search a folder that is a subfolder of an excluded folder,
|            the search must be split into two operations.
|            When callback functions need the containing directory to test a file name,
|            the 'test_dirs' option should be set to True
|            
|            Walking a large file tree can take significant time and produce a large amount of data,
|            but this tendency can be reduced by cleaning the tree of generated files beforehand,
|            and by applying suitable directory and file filters.   

walk()
......

The walk starts here

|        Args:
|            None
|            
|        Returns:
|            A list of matching file paths
|            
|        Raises:
|            None


Watcher
-------

Determine if your patches have been integrated into released kernel versions

Watcher(params)
...............

Constructor

|        Args:
|            params (dict): parameters
|                patchdir  (string, required): path to patch folder
|                sourcedir (string, required): path to source folder
|                datadir   (string, required): path to data folder
|                tempdir   (string, required): path to temp file folder
|                patchset  (dict, required):   description of patches
|                
|        Raises:
|            PT_ParameterError
|            PT_NotFoundError
|        
|        Notes:
|            Experience in testing shows a very low probability that an archive
|            diff section will match any of our patches exactly, so we merely
|            display the related files.

watch(archpath)
...............

View files related to archive diff sections

|        Args:
|            archpath (string): path to patch archive file
|            
|        Returns:
|            None. Output is a series of launches of the Viewer to view the files.
|            
|        Raises:
|            PT_ParameterError
|            PT_NotFoundError


Diff
----

Extract information from a diff section of a patch file

Diff(strings)
.............

Constructor

|        Args:
|            strings (Strings): diff section from a patch file or archive file
|            
|        Raises:
|            PT_ParameterError


Hunk
----

Extract information from a hunk section of a patch file

Hunk(strings)
.............

Constructor

|        Args:
|            strings (Strings): hunk section from a patch file or archive file


JSONConfig
----------

Store configuration data obtained from enhanced JSON input files

JSONConfig(params=None)
.......................

Constructor

|        Args:
|            params (dict, optional): parameters
|                filepath  (string, required): path to file with enhanced JSON encoded string, or None
|                separator (string, optional): char to use as separator in path expressions
|                    default is '/'
|                
|        Raises:
|            JSONConfigParameterError

__getitem__(key)
................

Ensure that a slice of our data is returned as a str object,
when the value is a unicode string, on Python2.x

|        Args:
|            k (str/unicode):   item index
|            
|        Returns:
|            str(value) when Python is 2.x and value is unicode
|            otherwise, value
|            
|        Raises:
|            JSONConfigTypeError, JSONConfigKeyError

get(key)
........

Get top level value or internal value

|        Args:
|            key (string): path to internal value
|                        
|        Returns:
|            The value addressed by key
|            
|        Raises:
|            JSONConfigTypeError, JSONConfigKeyError
|            
|        Notes:
|            The key argument may be the name of a top level key in the data, or a "path expression".
|            Such an expression contains one or more instances of '/' or of a user defined separator,
|            and encodes a path to a node in the dict.
|            For example, self.get("/mysql_options/admin_profile/data_base") will get the value at
|                self["mysql_options"]["admin_profile"]["data_base"]
|                
|            Values may also be accessed by normal Python indexing of the dict superclass.

set(key, value)
...............

Set top level value or internal value

|        Args:
|            key   (string): path to internal value
|            value (any Python value)
|                
|        Returns:
|            None
|            
|        Raises:
|            JSONConfigTypeError, JSONConfigKeyError
|            
|        Notes:
|            See notes for get method.

add(data)
.........

Add data to the current config

|        Args:
|            data (choice):
|                A string path to a file to load
|                A string representation of a JSON object
|                A Python dict
|        
|        Returns:
|            None
|            
|        Raises:
|            OSError or IOError when a file has problems
|            JSONConfigTypeError, etc, when JSON string is incorrectly formatted

has(key)
........

Determine if item is in the config data

|            Args:
|                key (string): path to internal value
|            
|            Returns:
|                True if item was found, else False


Patch
-----

Extract information from a patch file

Patch(path)
...........

Constructor

|        Args:
|            path (string): path to patch file
|            
|        Raises:
|            PT_ParameterError
|            PT_NotFoundError
|        
|        Notes:
|            Commented out diff and hunk sections are omitted.

list_files(patchpath) <staticmethod>
....................................

List the files referenced by a patch, without duplicates

|        Args:
|            patchpath (string) path to patch file
|            
|        Returns:
|            list of filenames
|            
|        Notes:
|            A "filename" is the portion of the file's path after the kernel root,
|            e.g. "drivers/iio/...".


PatchSet
--------

Extract information from a set of patch files

PatchSet(params)
................

Constructor

|        Args:
|            params (dict):  parameters
|                patchdir  (string, required): path to patch directory
|                patchset  (dict, required):   description of patches in patchdir
|            
|        Raises:
|            PT_ParameterError     

get_file_data()
...............

Get source file data for patches

|        Args:
|            None
|        
|        Returns:
|            A mapping of patch names to file names.

get_patch_data()
................

Get patch data for source files

|        Args:
|            None
|        
|        Returns:
|            A mapping of file names to patch names.

get_patch_names(params=None)
............................

Return list of names of patches in our patch set

|        Args:
|            params (dict, optional): parameters
|                excl_dirs (list, optional): directories to exclude
|                incl_dirs (list, optional): directories to include
|            
|        Returns:
|            list of patch names in the order found in patchset
|                
|        Notes:
|            The "name" of a patch is the concatenation of the name of its parent folder
|            and its filename, as shown in the patchset description.
|                
|            If params is None, names of all patches are returned.

get_patch_files(patchname)
..........................

Return a list of source files referenced in one patch file

|        Args:
|            patchname (string): name of patch file
|            
|        Raises:
|            PT_ParameterError, PT_NotFoundError
|            
|        Notes:
|            This function may be used to generate file lists for the *Finder*.                     

get_file_patches(filename)
..........................

Return a list of patch files that refer to one source file

|        Args:
|            filename (string): name of source file
|            
|        Raises:
|            PT_ParameterError, PT_NotFoundError
|                
|        Notes:
|            This function may be used to generate file lists for the *Matcher*. 

get_patch_patches(patchname)
............................

Get a list of patches that patchname depends on

|        Args:
|            patchname (string): name of patch file
|        
|        Returns:
|            A list of names of the parent patches in patchset order
|            
|        Raises:
|            PT_ParameterError, PT_NotFoundError
|            
|        Notes:
|            Patch A depends on patch B when they modify the same files
|            and patch B precedes patch A in the patch list.


PTObject
--------

PatchTools super class

Provides an identifiable super class for all PatchTools classes.
Implements common parameter checking functions for the sub classes.


Strings
-------

Provide some useful string like methods for lists of strings

Strings(data=None)
..................

Constructor

|        Args:
|            data (list, optional): a list of strings 
|            
|        Raises:
|            StringsParameterError

__getitem__(i)
..............

Ensure that slices of Strings objects are returned as Strings objects, not lists

|        Args:
|            i (int):   item index
|            i (tuple): (start, stop, [step])
|            
|        Returns:
|            Strings(self[i:j])
|        
|        Notes:
|            For mysterious reasons, slice keys can be passed as tuples, not slice objects.
|            In such cases, we convert the tuples to slices.

find(pattern, begin=None, end=None)
...................................

Find the first string in our data that starts with (pattern)

|        Args:
|            pattern (str):  the substring to match
|            begin   (int):  start index
|            end     (int):  stop index
|            
|        Returns:
|            Found: the index of matching string
|            Not found: -1
|            
|        Raises:
|            StringsParameterError
|                
|        Notes:
|            If begin is not specified, it is set to 0
|            If end is not specified, it is set to len(self).
|            All strings are left stripped before testing.

match(patterns, begin=None, end=None)
.....................................

Find the first string in our data that starts with a pattern in (patterns)

|        Args:
|            patterns (list): The substring to match
|            begin    (int):  Start index
|            end      (int):  Stop index
|            
|        Returns:
|            Found: the index of matching string, and the matching pattern
|            Not found: -1, ''
|            
|        Raises:
|            StringsParameterError
|                
|        Notes:
|            If begin is not specified, it is set to 0
|            If end is not specified, it is set to len(self).
|            All strings are left stripped before testing.

rfind(pattern, begin=None, end=None)
....................................

Find the last string in our data that starts with (pattern)

|        Args:
|            pattern (str):  the substring to match
|            begin   (int):  start index
|            end     (int):  stop index
|            
|        Returns:
|            Found: the index of matching string
|            Not found: -1
|            
|        Raises:
|            StringsParameterError
|                    
|        Notes:
|            If end is not specified, it is set to -1.
|            len(self) is added to the value of begin.
|            All strings are left stripped before testing.

rmatch(patterns, begin=None, end=None)
......................................

Find the last string in our data that starts with a string in (patterns)

|        Args:
|            patterns (str): The substrings to match
|            begin    (int):  Start index
|            end      (int):  Stop index
|            
|        Returns:
|            Found: the index of matching string, and the matching pattern
|            Not found: -1, ''
|            
|        Raises:
|            StringsParameterError
|                    
|        Notes:
|            If end is not specified, it is set to -1.
|            len(self) is added to the value of begin.
|            All strings are left stripped before testing.

filter(pattern, begin=None, end=None)
.....................................

Find all strings in our data that start with (pattern)

|        Args:
|            pattern (str):  the substring to match
|            begin   (int):  start index
|            end     (int):  stop index
|            
|        Returns:
|            Found: A list of the indices of the matching strings
|            Not found: None
|            
|        Raises:
|            StringsParameterError
|                    
|        Notes:
|            If begin is not specified, it is set to 0
|            If end is not specified, it is set to len(self).
|            All strings are left stripped before testing.

index(pattern)
..............

Return indices of strings that exactly match (pattern)

|        Args:
|            pattern (string): search text
|            
|        Raises:
|            StringsParameterError

lstrip()
........

Remove leading lines that are empty or whitespace

|        Args:
|            none
|            
|        Returns:
|            self, to allow chaining to slices, other methods

rstrip()
........

Remove trailing lines that are empty or whitespace.

|        Args:
|            none
|            
|        Returns:
|            self, to allow chaining to slices, other methods

partition(splitter)
...................

Split our data into two parts at a splitter pattern, searching forwards

|        Args:
|            splitter (str): The substring that splits the parts
|                
|        Returns:
|            splitter was found:
|                A tuple (head, tail) where head is a Strings object containing the first part,
|                and tail is a Strings object containing the second part.
|            splitter was not found:
|                (self, None)
|            
|        Notes:
|            Example: (head, body) = patch.partition('diff --git ')  

rpartition(splitter)
....................

Split our data into two parts at a splitter pattern, searching backwards

|        Args:
|            splitter (str): The substring that splits the parts
|                
|        Returns:
|            splitter was found:
|                A tuple (body, tail) where body is a Strings object containing the first part,
|                and tail is a Strings object containing the second part
|            splitter was not found:
|                (None, self)
|            
|        Notes:
|            Example: (body, tail) = patch.rpartition('-- ')

split(splitter)
...............

Split our data into two or more parts at occurrences of a splitter pattern

|        Args:
|            splitter (str): The substring that splits the parts
|                
|        Returns:
|            A list of Strings objects, each of which contains a part
|            
|        Raises:
|            StringsParameterError
|                    
|        Notes:
|            Example: diffs = body.split('diff --git ') 
|            This code will split the Strings object 'body' into a list of sections,
|            each of which starts with a string beginning with ('diff --git ').

extract(begin, end)
...................

Extract a list of sections tagged by (begin) and (end)

|        Args:
|            begin (str): section start marker
|            end   (str): section end marker
|            
|        Returns:
|            A list of Strings objects, one for each extracted section
|                
|        Notes:
|            The begin and end markers are not returned in the output
|            
|            Example: sections = strlist.extract('#++', '#--')
|            This code will extract all strings between '#++' and '#--' in strings.py
|            (this file) if the file has been read into strlist.

discard(begin, end)
...................

Remove a list of sections tagged by (begin) and (end)

|        Args:
|            begin (str): section start marker
|            end   (str): section end marker
|            
|        Returns:
|            A Strings object.
|                
|        Notes:
|            The begin and end markers are not returned in the output

sort()
......

Sort our data.

|        Args:
|            none

unique()
........

Remove duplicate successive instances of strings in  our data.

|        Args:
|            none
|            
|        Notes:
|            To remove all duplicates, sort the data first

join(lists) <staticmethod>
..........................

Join a list of objects into a single Strings object.
Each object is a list of strings or a Strings object.

|        Args:
|            lists (list): list of list or Strings objects
|                
|        Returns:
|            A Strings object containing all strings in the lists
|            
|        Raises:
|            StringsParameterError
|            
|        Notes:
|            Example:
|                list1 = Strings(['a','b'])
|                list2 = ['c','d']
|                list3 = Strings.join([list, list2])
|            This code will join the contents of list1 and list2 in list3.


Command
-------

Execute command in subprocess

Command()
.........

Constructor

|        Args:
|            None

sync(cmd)
.........

Execute subprocess synchronously

|        Args:
|            cmd (string): shell command to execute
|            cmd (list):   command arguments to pass
|                
|        Returns:
|            A list of strings:
|                ['retcode' : 0,
|                 'output' : '...',
|                 'errors' : '...'
|                 ]
|                 
|        Raises:
|            CommandParameterError when command is not a string type
|                
|        Notes:
|            Shell command  is a string like "cd tmp && ls".
|            Command arguments is a list like ['gedit', 'file1', file2',...]
|            Output and errors strings are only returned to the caller
|            when the subprocess returns output or errors.

async(cmd)
..........

Execute subprocess asynchronously

|        Args:
|            cmd (string): shell command to execute
|           
|        Returns:
|            None
|            
|        Raises:
|            see sync method above.
|                
|        Notes:
|            see sync method above. 

wait()
......

Wait for asynchronous subprocess to exit

|        Args:
|            None
|            
|        Returns:
|            list of result strings
|            
|        Raises:
|            CommandStateError when no subprocess is active    


ExceptionHandler
----------------

Handle exceptions

ExceptionHandler(params=None)
.............................

Constructor

|        Args:
|            params (dict): parameters
|                trace (bool, optional): format exception traceback
|                    default is True
|                print (bool): print results
|                    default is True


Helper
------

Facilitate use of PatchTools's classes

Helper(configpath)
..................

Constructor

|        Args:
|            config (dict): configuration data

cmd(command)
............

Handle Command request

|        Args:
|            command (string) shell command to execute

find(patterns, params)
......................

Handle Finder request

|        Args:
|             patterns (dict) Matcher parameters
|             params   (dict) Finder parameters 

check(patches, params=None)
...........................

Handle Checker request

|        Args:
|            patches (string/list, required) patch file(s)
|            params  (dict, optional) Checker parameters

walk(params)
............

Handle Walker request

|        Args:
|            params (dict, required) Walker parameters

watch(archives, params=None)
............................

Handle Watcher request

|        Args:
|            archives (string/list)    archive file path(s)
|            params   (dict, optional) Watcher parameters

view(files, params=None)
........................

View specified file(s)

|        Args:
|            files  (string/list) file path(s)
|            params (dict, optional) Viewer parameters
|                
|        Notes:
|            If params is not specified, the default file viewer is used.

vp2f(patchname, params=None)
............................

View patch and the source files it references

|        Args:
|            patchname (string) patch file name
|            params    (dict, optional) Viewer parameters

vf2p(filepath, params=None)
...........................

View source file and the patches that reference it

|        Args:
|            filepath (string) file path
|            params   (dict, optional) Viewer parameters

vp2p(patchname, params=None)
............................

View patch and other patches that reference its files

|        Args:
|            patchname   (string) patch name
|            params      (dict, optional) Viewer parameters

vp2a(patchname, archivepath, params=None)
.........................................

View patch and archive diff sections that reference its files:

|        Args:
|            patchname   (string) patch name
|            archivepath (string) archive file path
|            params      (dict, optional) Viewer parameters

vcpf(checkpath, patchname, context=None, params=None)
.....................................................

View Checker output, patch file and the source files it references,
one at a time.

|        Args:
|            checkpath (string) checker output file path
|            patchname (string) patch name
|            context   (dict)   source, dir, patchdir, etc.
|            params    (dict, optional) Viewer parameters
|        
|        Notes:
|            If context is not passed, config['defaults'] is used.


Matcher
-------

Implement filter selection of strings

Matcher(params)
...............

Constructor

|        Args:
|            params (dict): parameters
|                match    (list, optional): string match pattern(s)
|                prefix   (list, optional): string start pattern(s)
|                suffix   (list, optional): string end pattern(s)
|                substr   (list, optional): substring pattern(s)
|                regexp   (list, optional): regular expression pattern(s)
|                funcs    (list, optional): callback function(s)
|            
|        Raises:
|            PT_ParameterError on invalid parameters
|                
|        Notes:
|            At least one option must be specified for the filter to have an effect.         
|            Regular expression pattern strings should be coded using the r"..." string form.

__call__(string)
................

Try to match string to stored filter

|        Args:
|            string (string): string to match
|            
|        Returns:
|            text of the matching pattern, or None


Functions
---------

Utility functions

Linux source files and patches that describe them may contain byte values
that are legal 'Latin-1' (aka ISO-8859-1) character codes, but not legal
'UTF-8' start bytes. For example, 0xb3 is the 'Latin-1' character for the
cube symbol, i.e. a superscript 3. For this reason the file access functions
below default to the 'latin_1' encoding.

is_windows() <staticmethod>
...........................

Report whether the host system is Windows

|        Args:
|            None
|        
|        Returns:
|            True if running on Windows, else False

is_python3() <staticmethod>
...........................

Report whether the Python version is >= 3

|        Args:
|            None
|        
|        Returns:
|            True if running on Python 3, else False

file_size(path) <staticmethod>
..............................

Determine size of the file/folder at (path)

|        Args:
|            path (string): file path
|        
|        Returns:
|            size (int): file size in bytes

is_dir(path) <staticmethod>
...........................

Determine whether the object at (path) is a directory

|        Args:
|            path (string): file path
|        
|        Returns:
|            True if the path exists and is a directory.

is_file(path) <staticmethod>
............................

Determine whether the object at (path) is a file

|        Args:
|            path (string): file path
|        
|        Returns:
|            True if the path exists and is a regular file.

join_path(head, tail) <staticmethod>
....................................

Form a path from (head) and (tail).

|        Args:
|            head (string): path prefix
|            tail (string): path suffix
|        
|        Returns:
|            string: the resulting path
|        
|        Notes:
|            This function allows head and tail to contain embedded '/' characters.

trim_path(head, path) <staticmethod>
....................................

remove (head) from (path.

|        Args:
|            head (string): path prefix
|            path (string): path
|        
|        Returns:
|            string: the resulting path

read_file(path, enc='latin_1') <staticmethod>
.............................................

Read file data.

|        Args:
|            path (string): file path
|        
|        Returns:
|            File data as a single object.

read_lines(path, enc='latin_1') <staticmethod>
..............................................

Read file lines.

|        Args:
|            path (string): file path
|        
|        Returns:
|            File data as a list of '\n' terminated strings.

read_strings(path, enc='latin_1') <staticmethod>
................................................

Read file strings.

|        Args:
|            path (string): file path
|        
|        Returns:
|            File data as a list of strings.

write_file(text, path, enc='latin_1') <staticmethod>
....................................................

Write text to file at path

|        Args:
|            path (string): file path
|        
|        Returns:
|            None

write_strings(strings, path, enc='latin_1') <staticmethod>
..........................................................

Write strings to file at(path)

|        Args:
|            path (string): file path
|        
|        Returns:
|            None
|        
|        Notes:
|            If (strings) intentionally has empty strings, using str.join() would
|            delete them, which may cause problems for readers of the file.
|            Here we write the strings one at a time.

get_string_filename(string) <staticmethod>
..........................................

Extract filename from string

|        Args:
|            string (string): input string
|        
|        Returns:
|            filename (string): filename substring
|        
|        Notes:
|            Supported string formats:
|                In patches:
|                    'diff --git a/foo... b/foo...'
|                    'diff -u -R -n foo... foo...'
|                    '--- foo...'
|                    '+++ foo...
|                In a Checker output file:
|                    'DIFF: diff --git a/arch/powerpc/mm/numa.c b/arch/powerpc/mm/numa.c'

normalize_string(string, strip=True) <staticmethod>
...................................................

Replace all internal string whitespace by single spaces

|        Args:
|            string (string): input string
|            strip  (bool):   True = strip the string first

string_to_words(string) <staticmethod>
......................................

Split a string into words on space boundaries.

|        Args:
|            string (string): input string
|        
|        Notes:
|            After splitting, words are stripped of whitespace and empty words
|            are removed.

is_string_type(param) <staticmethod>
....................................

Determine if an object is a string

|        Args:
|            param (unknown): input object
|        
|        Returns:
|            True if the object is a string, else False
|        
|        Notes:
|            Python2 has str, unicode and StringTypes, while Python3
|            has only str.


Appendix A -- Patch Basics
==========================

For a number of years, the Linux kernel source has been managed by the GIT source
code control system. Normally you will use GIT commands to obtain and update kernels.
GIT uses patches to modify the kernel sources. Linux kernel patches are usually produced
by running the 'git format-patch' command, which commits your changes if needed,
and also generates the patches.

A typical patch file is "0002-ARM-OMAP-Hack-AM33xx-clock-data-to-allow-JTAG-use.patch"::

	From ac9bb90cbb8c81dd384e339063e72d2fc90221c2 Mon Sep 17 00:00:00 2001
	From: Matt Porter <mporter@ti.com>
	Date: Mon, 7 Jan 2013 11:55:00 -0500
	Subject: [PATCH 02/35] ARM: OMAP: Hack AM33xx clock data to allow JTAG use

	The debugss interface clock must remain enabled at init
	in order to prevent an attached JTAG probe from hanging.

	Signed-off-by: Matt Porter <mporter@ti.com>
	---
	arch/arm/mach-omap2/cclock33xx_data.c |    2 +-
	 1 file changed, 1 insertion(+), 1 deletion(-)

	diff --git a/arch/arm/mach-omap2/cclock33xx_data.c b/arch/arm/mach-omap2/cclock33xx_data.c
	index ea64ad6..a09d6d7 100644
	--- a/arch/arm/mach-omap2/cclock33xx_data.c
	+++ b/arch/arm/mach-omap2/cclock33xx_data.c
	@@ -428,7 +428,7 @@ DEFINE_STRUCT_CLK(smartreflex1_fck, dpll_core_ck_parents, clk_ops_null);
 	 *     - usbotg_fck (its additional clock and not really a modulemode)
	 *     - ieee5000
	 */
	-DEFINE_CLK_GATE(debugss_ick, "dpll_core_m4_ck", &dpll_core_m4_ck, 0x0,
	+DEFINE_CLK_GATE(debugss_ick, "dpll_core_m4_ck", &dpll_core_m4_ck, ENABLE_ON_INIT,
	 				 AM33XX_CM_WKUP_DEBUGSS_CLKCTRL, AM33XX_MODULEMODE_SWCTRL_SHIFT,
	 				 0x0, NULL);
	 
	-- 
	1.7.10.4
	
This format is a variation on the 'diff -urN' format that is sometimes described in the literature,
and is still used in application packages. The patch content in this format is the body of an email
message. The patch may have one or more 'diff' sections that refer to the same or different
files, and each diff section may have one or more 'hunk' sections (marked by lines starting with '@@').

See <http://wikipedia.org/wiki/Diff> for basic information on diff formats.

Note that:

* The 'a' at the start of a path denotes the original/old version of the kernel tree.
* The 'b' at the start of a path denotes the patched/new version of the kernel tree.
* Paths in the diff line are nominal paths.
* The index line identifies the commit state before and after applying the patch (see below).
* A '---' line contains the actual path of an "a" file, or '/dev/null'.
* A '+++' line contains the actual path of a "b" file, or '/dev/null'.
* The '@@' lines indicate 'hunks' (ranges over which following edit lines are to be applied).
* The -m,n values indicate the start line number and length of the hunk information in the "a" (old) file.
* The +m,n values indicate the start line number and length of the hunk information in the "b" (new) file.
* Line numbers are 1-based.
* An edit line starting with '+' indicates an addition to the old version to obtain the new version.
* An edit line starting with '-' indicates a deletion from the old version to obtain the new version.
* An edit line that starts with ' ' is in both files, but possibly at different line numbers.
  Such lines are called 'merge' lines in the *Checker* output.
* Lines that appear to be blank in a hunk are part of the hunk data.
* A 'delete' line followed by an 'add' line constitutes a 'change' request.

In hunk lines (that begin with '@@') the text after the second '@@' is termed a 'hunk note' in the
PatchTools source code. Hunk notes appear to be copies of the closest previous source line that
has a character in the first column, e.g. function declaration lines and label lines in a .c file.
Hunk notes are useful in finding text that is not in the location expected by a patch, but may not
be unique if the file uses conditional compilation (e.g. "#ifdef FOO").

The index line contains values obtained from the SHA1 checksums computed on the commit states before
and after applying the patch on the patch developer's system. When possible, a short unique prefix
of a checksum is used.

Some special cases are handled differently by GIT than by 'diff -urN':

Addition of a new file to the tree::

	diff --git ...
	new file mode 100644
	index ea64ad6..a09d6d7 100644
	--- /dev/null
	+++ b/arch/arm/mach-omap2/cclock33xx_data.c
	@@ -0,0 +1,n @@ ...
	...
    
where n is the number of lines in the new file.

Removal of an old file from the tree::

	diff --git ...
	deleted file mode 100644
	index ea64ad6..a09d6d7 100644
	--- a/arch/arm/mach-omap2/cclock33xx_data.c
	+++ /dev/null
	@@ -1,n  +0,0 @@ ...
	...

where n is the number of lines in the old file.

Addition of a binary file to the tree::

	diff --git ...
	new file mode 100755
	index <old git index> .. <new git index>
	GIT binary patch
	literal 11764
	zcmds7eQ;dWb-! ...

The *Checker* does not handle binary patches.

Appendix B -- Patch Archives
============================

Each kernel released by kernel.org has an associated "patch" file shown on the site's
main page, which you can download. The file is an 'xz' archive that contains a single
text file which is the concatenation of the diff sections from all the patches that
were applied to produce the kernel version. Note that the file does not contain patch
file names, since the patches were submitted to kernel.org as email messages. The archive
also does not contain other information from the patch headers such as 'Author', 'Date', etc.

Some data values in the diffs may be different than the corresponding values in the submitted patch files.
A patch is submitted by an author as an email message. If the patch is accepted for inclusion into the kernel,
the author will later receive some message like "please rebase your patch to the tip of branch x". Rebasing may
involve changing the hunk line numbers and possibly the text of edits. The kernel developer/maintainer will
apply the changed patch. Consequently the index checksums will be different than those in the patch,
and the hunk line numbers and edits may also differ.

Appendix C - Examples
=====================

Examples are found in the examples folder, and are coded using the *Helper* class for convenience.

PatchTools was developed using a fairly large set of patches assembled by eLinux.org
to create an embedded Ubuntu version based on Linux kernel version 3.8.13
that could be used with the well known "BeagleBone" embedded computers, which use ARM based
processors provided by Texas Instruments. Contact eLinux.org to get the patches.

We have used various other kernels for testing; most recently a stable kernel with
version number 3.16.1 was used.

The source files 'config.json' shows how to set up configuration data for the *Helper*,
which uses a JSONConfig object to store and access the data.

After studying the *Helper* documentation, you can embark on experiments related to your project.


Appendix D - Software Design
============================

Program structure
-----------------

PatchTools is implemented with Python new style classes, for consistency of style, and to allow
integration of its components into other scripts or processes.

Class constructors process parameters that are expected not to change between invocations,
while instance methods process parameters that are different in each invocation.
For example::

    c = Checker({ 'patchdir' : <path to patch dir>, 'sourcedir' : <path to kernel dir> })
    r = c.check(<patchname1>)
    s = c.check(<patchname2>)

Class constructors have a single dict argument to receive parameters. 

Instance methods usually have one or two target file parameters, and may have a dict argument to receive context data.

Since parameter values are provided by end users, extensive validation is performed on the values.

The *Helper* class provides convenient wrappers for the classes and useful utility functions.
It can be used as shown in the examples.


Implementation
--------------

The software has been implemented using the Kepler version of Eclipse with the PyDev plugin on a Linux Mint16
system. Use of these tools for further development is not required, but if they are not used, some additional
setup may be needed.

All import statements use this form::

    from patchtools.lib.utils.functions import Functions as ut

This verbose form will prevent components in other packages from being found in the Python path
when the intention is to import a PatchTools component. On launching a program the Python interpreter
builds a sys.path variable including some standard locations and the value of the environment
variable PYTHONPATH if it is defined. 

If PatchTools is not installed in your Python system, Python will only be able to find it if PYTHONPATH is set
correctly. To match the absolute paths as shown above, PYTHONPATH should point to the directory that includes
the patchtools, not to the patchtools directory itself.

Eclipse-PyDev may not configure PYTHONPATH correctly if you are not careful, and also adds a large set of folders
to the Python path. You can edit the Eclipse PYTHONPATH variable on the project's properties page.

PYTHONPATH won't normally be defined in your environment when, for example, you try to launch an application
in a shell. On Linux, you can overcome this problem by exporting a value from your .profile file or by wrapping
calls to the application file in a script (call it 'do_run')::

    PYTHONPATH=`pwd` ; $@
  
which may be used like so::

    ./do_run test_app.py
    
The do_run script should be located in the parent directory of patchtools to get a correct value for PYTHONPATH.


Appendix D - Checker vs. quilt vs 'git am'
==========================================

The *Checker* analyzes patches and source code, and reports problems to the user. It does not try to fix a patch
or make it fit the source. 

Quilt and 'git am' will detect the same sort of problems as the the *Checker* does in their analysis of patches
and sources. Quilt and 'git am' will try to resolve some of these problems by shifting patch lines elsewhere in
the source file, sometimes by a large distance. But they will reject patches that cannot be fixed in this simple
way.

Quilt will notify you that it has shifted lines to make a hunk fit the source, but 'git am' does not.

Inspection of typical *Checker* output gathered on the 'patches-3.8' patch set shows a sizable number of
different patterns of mismatch between patches and source files. Many of these patterns will be too complex
for quilt or 'git am' to fix. But the *Checker* can show you in great detail what is wrong with the patches,
and can allow you to develop a strategy to fix them.

It is also possible that the simplistic fixing strategies pursued by quilt and 'git am' may not produce a
correct result, or may hide from you that there is a problem in the code. In the 'capemgr' tests in the
'examples' folder, it was observed that quilt shifted the last few hunks in the last patch by about 71 lines,
and that 'git am' probably did also, but did not report doing so. Both programs claimed to have applied the
patches successfully.

From the *Checker* output it appears that the next to last version of capemgr.c (produced by the 'resources/0023...'
patch) had about 70 lines of extra text that was not expected to be present by the last patch. And examining the
last two patches shows they both have the same 'before' checksum value in their index lines, which is incorrect.
You may wish to investigate why this is so.

The *Checker* does not create any work files in the source tree, modify either the source or the patch files,
require you to use a specific folder structure, or require you to have GIT metadata in the source tree.

Quilt requires you to create a tree of work files including the patches and kernel directory, and also requires
you to reset the source files targeted by the patches to their original versions each time you run it to test
a set of patches. It also requires you to reset the 'applied-patches' file to the empty state.

'git am', of course, can only be used in a "working directory", i.e. a source tree that has been obtained
from a GIT repo, and has GIT metadata.


Appendix E - Checker Output
===========================

The *Checker* emits various kinds of error messages:

* "a" files missing from the target source tree.

* "b" files incorrectly present in the target tree.

* Format errors in the patch file.

* Incorrect start or count values in the hunk specification lines.

* Lines that are supposed to be in "a" source files, but are not at the specified locations.

* Lines that are supposed to be absent from "a" source files, but are in the files.

Aside from errors in the patches themselves, there some common reasons for failures:

* Patches should be applied in commit sequence. If an early patch fails to add or delete
  a file, a later patch may get a file error by referring to the file.
  
* If a patch has several hunks that add lines to the file, the later hunks may appear to have
  incorrect start and count values because the early hunks were not applied.

* Similarly, a later patch may get an edit error by referring to lines that
  were not inserted or deleted by a previous patch that failed.

These problems can sometimes be resolved by fixing and applying the early patch that failed.
The 'get_patch_patches' method of the *PatchSet* object can be used to reveal dependencies
between patches.

The most serious cause of failures is that other kernel developers have submitted patches
that modify some of the same files as your patches, and that some of these patches have been
integrated into Linux before yours. The most difficult case to resolve will be one in which
another patch has partly fixed the same problem your patch is intended to fix, but does so
with incompatible logic. You may only be able to resolve such a problem by rewriting
your patches to work with your new kernel version. Alternately you may use the procedures shown
in Example 5 of the *Helper* documentation to determine if you really need the patch.

Examples
--------

For a file that is not in the target tree::

   DIFF: "diff --git a/include/linux/input/ti_am335x_tsc.h b/include/linux/input/ti_am335x_tsc.h"
      ERROR: "a" file not found: include/linux/input/ti_am335x_tsc.h

For a file with invalid length::

   DIFF: "diff --git a/arch/arm/common/Kconfig b/arch/arm/common/Kconfig"
      HUNK: "@@ -40,3 +40,6 @@ config SHARP_PARAM"
         ERROR: invalid old start or count for file: start=40, count=3, length=22
         
   Presumably the file previously had a greater length in the "a" version of the sources.
   As it happens, the addition specified by the hunk ('+config TI_PRIV_EDMA') is in the target
   file. So the hunk is not needed.
         
For a hunk whose lines can be shifted::

   DIFF: "diff --git a/include/linux/mfd/ti_am335x_tscadc.h b/include/linux/mfd/ti_am335x_tscadc.h"
      HUNK: "@@ -71,8 +71,6 @@"
         WARN:  "merge"  line not found at 71: "#define STEPCONFIG_INM_ADCREFM	STEPCONFIG_INM(8)"
         WARN:  "merge"  line not found at 72: "#define STEPCONFIG_INP_MASK	(0xF << 19)"
         WARN:  "merge"  line not found at 73: "#define STEPCONFIG_INP(val)	((val) << 19)"
         WARN:  "merge"  line not found at 74: "#define STEPCONFIG_INP_AN4	STEPCONFIG_INP(4)"
         WARN:  "merge"  line not found at 75: "#define STEPCONFIG_INP_ADCREFM	STEPCONFIG_INP(8)"
         WARN:  "merge"  line not found at 76: "#define STEPCONFIG_FIFO1	BIT(26)"
         FIND:  "merge"  line found at 79: "#define STEPCONFIG_INM_ADCREFM	STEPCONFIG_INM(8)"
         FIND:  "merge"  line found at 80: "#define STEPCONFIG_INP_MASK	(0xF << 19)"
         FIND:  "merge"  line found at 81: "#define STEPCONFIG_INP(val)	((val) << 19)"
         FIND:  "merge"  line found at 82: "#define STEPCONFIG_INP_AN4	STEPCONFIG_INP(4)"
         FIND:  "merge"  line found at 83: "#define STEPCONFIG_INP_ADCREFM	STEPCONFIG_INP(8)"
         FIND:  "merge"  line found at 84: "#define STEPCONFIG_FIFO1	BIT(26)"

 For a patch whose additions have been applied::
 
    PATCH: "arm/0005-ARM-DTS-AM33XX-Add-PMU-support.patch"
       DIFF: "diff --git a/arch/arm/boot/dts/am33xx.dtsi b/arch/arm/boot/dts/am33xx.dtsi"
            HUNK: "@@ -48,6 +48,11 @@"
               WARN:  "merge"  line not found at 48: "		};"
               WARN:  "merge"  line not found at 49: "	};"
               WARN:  "merge"  line not found at 50: ""
               INFO:  "add"    line not found at next line: "	pmu {"
               INFO:  "add"    line not found at next line: "		compatible = "arm,cortex-a8-pmu";"
               INFO:  "add"    line not found at next line: "		interrupts = <3>;"
               INFO:  "add"    line not found at next line: "	};"
               INFO:  "add"    line not found at next line: ""
               WARN:  "merge"  line not found at 51: "	/*"
               WARN:  "merge"  line not found at 52: "	 * The soc node represents the soc top level view. It is uses for IPs"
               WARN:  "merge"  line not found at 53: "	 * that are not memory mapped in the MPU view or for the MPU itself."
               FIND:  "add" line found at 69: "	pmu {"
               FIND:  "add" line found at 70: "		compatible = "arm,cortex-a8-pmu";"
               FIND:  "add" line found at 71: "		interrupts = <3>;"
               FIND:  "merge" line found at 76: "	 * that are not memory mapped in the MPU view or for the MPU itself."
        INFO:  1 patch errors
   
   All of the "add" lines were found in the source file, although not at the locations where the patch expected
   to insert them. Thus the patch is not needed.
   
   For a patch whose deletions have been applied::
   
       HUNK: "@@ -127,7 +138,7 @@ static int tiadc_read_raw(struct iio_dev *indio_dev,"
         WARN:  "merge"  line not found at 127: "		if (i == chan->channel)"
         WARN:  "merge"  line not found at 128: "			*val = readx1 & 0xfff;"
         WARN:  "merge"  line not found at 129: "	}"
         ERROR: "delete" line not found at 130: "	am335x_tsc_se_update(adc_dev->mfd_tscadc);"
         WARN:  "merge"  line not found at 131: ""
         WARN:  "merge"  line not found at 132: "	return IIO_VAL_INT;"
         WARN:  "merge"  line not found at 133: "}"
         
   Note that the *Checker's* find logic only looks for significant lines, so it did not search for '};', etc.
   The logic also did not find the line starting with '* The soc node', which is in the file, but with a slightly
   different spelling.
   
   

    







