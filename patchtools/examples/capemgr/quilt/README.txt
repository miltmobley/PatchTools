Modified not-capebus/0030 patch to start from an existent but empty capemgr.c file,
so we won't have to delete capemgr.c each time we run quilt from the first patch.

Note that when quilt is run it will create a '.pc' folder in this directory to hold the results.
