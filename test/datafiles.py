'''
Created on Oct 23, 2014

@author: milton
'''

import json

if __name__ == '__main__':
    
    inpt = open("../DATAFILES.txt", "r")
    text = inpt.read()
    inpt.close()
    data = json.loads(text)
    print('done')