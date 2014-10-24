'''
Created on Oct 8, 2014

@author: milton
'''
import subprocess

def mq_patches_applied():
    """Check if there are any applied MQ patches."""
    try:
        #cmd = 'hg qapplied'
        cmd = 'gedit foo'
        with subprocess.Popen(cmd.split(),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as st:
            bstdout, bstderr = st.communicate()
            return (st.returncode, bstdout, bstderr)
    
    except Exception as e:
        print(str(e))
        
if __name__ == '__main__':
    
    print(mq_patches_applied())