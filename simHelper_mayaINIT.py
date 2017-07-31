import imp
import sys

def import_core():
    runModulePath = 'G:\\HBO\\scripts\\autoSimulator\\main_GUI\\main_GUI_v125.py'
    runModuleFileName = 'main_GUI_v125'
    
    intIndex = 1
    #find newest core module path
    while True:
        oldStringIndex = ''.join([runModuleFileName[-3],runModuleFileName[-2], runModuleFileName[-1] ])
        newStringIndex = str(int(oldStringIndex) + intIndex)
        newRunModuleFileName = runModuleFileName.replace(oldStringIndex, newStringIndex)
        newRunModulePath = runModulePath.replace(oldStringIndex, newStringIndex)
        if not os.path.exists(newRunModulePath):
            break
        runModuleFileName = newRunModuleFileName
        runModulePath = newRunModulePath
        
    #import core module   
    print 'core module path:', runModulePath  
    print(runModuleFileName)  
    gui = imp.load_source(runModuleFileName, runModulePath)
    del sys.modules[runModuleFileName]
    gui = imp.load_source(runModuleFileName, runModulePath)
    
    return gui

try:
    gui.delete()
except NameError:
    pass
gui = import_core()
gui.create()