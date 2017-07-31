### UPDATE REFERENCES
import maya.cmds as mc
from PySide import QtCore as qc
from PySide import QtGui as qg
from functools import partial
import max
import os


class Core():
    def __init__(self):
        print('running core')

        # get names of all references
        references = mc.ls(references = True)
        
        # for each reference:
        for reference in references:
            # get directory of origin
            location = mc.referenceQuery(reference, filename = True).split('{')[0]
            currentFile = location.split('/')[-1]
            directory = location.split(currentFile)[0]
            
            # get the filePaths of all the files in that directory
            referenceVersions = [(directory + version) for version in os.listdir(directory)]
            
            # get the ages of those files
            youngest_age = 0
            for referenceVersion in referenceVersions:
                statistics = os.stat(referenceVersion)    
                thisVersion_age = statistics.st_mtime
                
                # find which of the files is the youngest
                if youngest_age < thisVersion_age and '.mb' in referenceVersion:
                    youngest_age = thisVersion_age
                    youngest_file = referenceVersion
                
            # check if this file is the same as the one in the scene
            if youngest_file == location:
                # if True: do nothing
                pass
            else:
                # if False: replace the reference in the scene by the newer file
                mc.file(youngest_file, loadReference = reference, type = 'mayaBinary', options = 'v=0;')
            			
Core()
        