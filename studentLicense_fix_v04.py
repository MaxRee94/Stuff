import maya.cmds as mc
import os
import max

#show prompt
prompt = max.errorPrompt('''       WORKING         ''', '''
             WORKING...          
''')
prompt.show()

#save as ascii file
mc.file(save = True, type = 'mayaAscii')

#query active scene fileName
fileName = mc.file(query = True, sceneName = True)
print(fileName)

#check if license is present
file = open(fileName, 'r')
currentContent = file.read()
file.close()

if 'fileInfo "license" "student";' in currentContent:

    #replace old content with new content
    newContent = currentContent.replace('fileInfo "license" "student";', '')
    file = open(fileName, 'w')
    file.write(newContent)
    file.close()
    
    #open and re-save edited file
    mc.file(fileName, open = True)
    mc.file(fileName, rename = fileName.replace('.ma', '.mb'))

mc.file(save = True, type = 'mayaBinary')

prompt.deleteLater()
    
prompt.deleteLater()



    
    
