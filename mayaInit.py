import imp
import sys
import os.path

def import_core():
    runModulePath = 'F:\\HBO\\scripts\\damProgramma\\damProgramma_GUI_v05.py'
    runModuleFileName = 'damProgramma_GUI_v05'
    
    intIndex = 1
    #find newest core module path
    while True:
        oldStringIndex = ''.join([runModuleFileName[-2], runModuleFileName[-1] ])
        newStringIndex = '0' + str(int(oldStringIndex) + intIndex)
        newRunModuleFileName = runModuleFileName.replace(oldStringIndex, newStringIndex)
        newRunModulePath = runModulePath.replace(oldStringIndex, newStringIndex)
        print(newRunModulePath)
        if not os.path.exists(newRunModulePath):
            break
        runModuleFileName = newRunModuleFileName
        runModulePath = newRunModulePath
        
    #import core module   
    print 'gui module path:', runModulePath  
    stront = imp.load_source(runModuleFileName, runModulePath)
    del sys.modules[runModuleFileName]
    stront = imp.load_source(runModuleFileName, runModulePath)
    
    return stront

try:
	dammen.delete()
except NameError:
	pass
dammen = import_core()
dammen.create()