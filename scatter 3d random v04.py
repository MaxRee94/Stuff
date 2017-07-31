import maya.cmds as mc
import random

sel = mc.ls(sl = True)

eindFrame = 300
beginFrame = 1

moveAmount = 1.0
rotateAmount = 80

maximumDistance = 2
scaleRange = [1.0, 1.0]

amountOfCopies = 20

for object in sel:
    for i in range(amountOfCopies): 
        mc.select(object)   
        mc.duplicate(object)
        
        moveValues = [random.uniform(-maximumDistance,maximumDistance),random.uniform(-maximumDistance,maximumDistance),random.uniform(-maximumDistance,maximumDistance)]
        rotateValues = [random.uniform(0,360),random.uniform(0,360),random.uniform(0,360)]
        scaleValue = random.uniform(scaleRange[0],scaleRange[1])
        
        moveOffsets = [random.uniform(-moveAmount,moveAmount),random.uniform(-moveAmount,moveAmount),random.uniform(-moveAmount,moveAmount)]
        rotateOffsets = [random.uniform(-rotateAmount,rotateAmount),random.uniform(-rotateAmount,rotateAmount),random.uniform(-rotateAmount,rotateAmount)]
        
        mc.currentTime(beginFrame)
        mc.move(moveValues[0],moveValues[1],moveValues[2], relative = True)
        mc.rotate(rotateValues[0],rotateValues[1],rotateValues[2], relative = True)
        mc.scale(scaleValue,scaleValue,scaleValue, relative = True)
        
        mc.setKeyframe()
        
        newObject = mc.ls(sl = True)[0]
        
        mc.currentTime(eindFrame)
        mc.move(moveOffsets[0],moveOffsets[1],moveOffsets[2], newObject, relative = True)
        mc.rotate(rotateOffsets[0],rotateOffsets[1],rotateOffsets[2], newObject, relative = True)
        
        mc.setKeyframe()
        
        mc.keyTangent(newObject, animation = 'objects', inTangentType = 'linear', outTangentType = 'linear')
    
    
