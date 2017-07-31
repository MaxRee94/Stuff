#Simulation Helper CORE
import maya.cmds as mc
import maya.mel as mel
import max
import random
import os
import sys
import imp
import time
import subprocess
import math


#default attributes
    ## 
    ## FLUIDS
fluidEmitterAttrs = ['fluidDensityEmission','fluidHeatEmission','fluidFuelEmission','fluidDropoff','inheritVelocity','normalSpeed','directionY',
'directionZ','directionalSpeed','directionX']
fluidContainerAttrs = ['densityScale', 'densityBuoyancy', 'densityDissipation', 'densityDiffusion', 'densityPressure', 'densityPressureThreshold', 
'densityTension', 'tensionForce', 'densityGradientForce', 'turbulenceStrength', 'turbulenceFrequency', 'temperatureScale', 'buoyancy', 
'temperaturePressure', 'temperaturePressureThreshold', 'temperatureDissipation', 'temperatureDiffusion', 'temperatureTurbulence', 'temperatureTension', 
'fuelScale', 'reactionSpeed', 'airFuelRatio', 'fuelIgnitionTemp', 'maxReactionTemp', 'heatReleased', 'gravity', 'viscosity', 'friction', 
'velocityDamp', 'colorTexture', 'incandTexture', 'opacityTexture', 'textureType', 'coordinateMethod', 'coordinateSpeed', 'opacityTexGain', 
'threshold', 'amplitude', 'ratio', 'frequencyRatio', 'depthMax', 'invertTexture', 'inflection', 'textureTime', 'zoomFactor', 'frequency', 
'textureOriginX', 'textureOriginY', 'textureOriginZ', 'textureScaleZ', 'textureScaleY', 'textureScaleX', 'textureRotateX', 'textureRotateY', 
'implode', 'textureRotateZ', 'implodeCenterX', 'implodeCenterY', 'implodeCenterZ', 'velocityScaleX', 'velocityScaleY', 'velocityScaleZ', 
'velocitySwirl', 'velocityNoise', 'turbulenceSpeed', 'temperatureNoise', 'lightReleased']

emitterRanges = [[0.000,2.000,1.000],[0.000,2.000,1.000],[0.000,2.000,1.000],[0.000,10.000,2.000],[0.000,1.000,0.500],[0.000,10.000,1.000],[-10.000,10.000,0.000],
[-10.000,10.000,0.000],[0.000,10.000,0.000],[-10.000,10.000,0.000]]
containerRanges = [[0.0, 2.0, 0.5], [-5.0, 5.0, 1.0], [0.0, 1.0, 0.0], [0.0, 2.0, 0.0], [0.0, 1.0, 0.0], 
[0.0, 1.0, 1.0], [0.0, 5.0, 0.0], [0.0, 5.0, 0.0], [-5.0, 5.0, 0], [0.0, 1.0, 0.0], [0.0, 2.0, 0.2], 
[0.0, 2.0, 1.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.1], [0.0, 2.0, 0.1], 
[0.0, 5.0, 0.1], [0.0, 5.0, 0.0], [0.0, 2.0, 0.1], [0.0, 1.0, 0.05], [0.0, 50.0, 0.0], [0.0, 1.0, 0.0], 
[0.0, 1.0, 1.0], [0.0, 1.0, 1.0], [0, 10.0], [0, 1], [0, 1.0], [0, 1.0], [0, 1], [0, 1], [0, 1], [0, 5], 
[0, 1], [0, 1], [0, 2], [0, 1], [0, 1], [0, 1], [1, 10], [1, 8], [0, 1], [0, 1], [0, 10], [0, 10], [0, 5], 
[-100, 100], [-100, 100], [-100, 100], [0, 10], [0, 10], [0, 10], [-10, 10], [-10, 10], [-10, 10], [-1, 1], 
[-10, 10], [-10, 10], [-10, 10], [-10, 10], [-10, 10], [-10, 10], [0, 10], [0, 1], [0, 2], [0, 1], [0, 1]]





testAttr = 'densityDissipation'
if testAttr not in fluidContainerAttrs:
    print('testAttr:', testAttr, 'not in container list')
if len(fluidContainerAttrs) != len(containerRanges):
    print('ATTENTION: Length of container ranges list is not equal to the fluidContainerAttrs list')

    ##
    ## nPARTICLES
default_nPart_emitterAttrs = ['translateX','translateY','translateZ','rotateZ',
'rotateY','rotateX','scaleY','scaleZ','shearYZ',
'shearXZ','shearXY','scaleX',
'emitterType','rate','scaleRateBySpeed',
'scaleRateByObjectSize','cycleEmission','cycleInterval','minDistance','maxDistance','directionX','directionY','directionZ',
'spread','speed','speedRandom','tangentSpeed','normalSpeed','volumeShape',
'volumeOffsetX','volumeOffsetY','volumeSweep','sectionRadius',
'volumeOffsetZ','awayFromCenter','awayFromAxis','alongAxis','aroundAxis','randomDirection',
'directionalSpeed','scaleSpeedBySize']
default_nPart_partAttrs = ['lifespan','radius','radiusScaleInputMax','localForceX','localForceY',
'localForceZ','localWindX','localWindY','localWindZ','dynamicsWeight','conserve','drag','damp','pointMass','massScaleInputMax',
'massScaleRandomize','massScaleInput','pointForceField','pointFieldMagnitude','selfAttract','pointFieldDistance','pointFieldScaleInput',
'pointFieldScaleInputMax','computeRotation','rotationFriction','rotationDamp','airPushDistance','airPushVorticity',
'windShadowDistance','windShadowDiffusion']
default_nPart_nucleusAttrs = ['gravity','airDensity','windSpeed','windDirectionX','windDirectionY','windNoise',
'windDirectionZ','usePlane','planeOriginX','planeOriginY','planeOriginZ','planeNormalZ','planeNormalY','planeNormalX',
'planeBounce','planeFriction','planeStickiness','timeScale','spaceScale']
nPart_emitterRanges = [[-20, 20], [-20, 20], [-20, 20], [-360, 360], [-360, 360], [-360, 360], [0.5, 1.5], [0.5, 1.5], [0.2, 3], [0.2, 3], 
[0.2, 3], [0.5, 1.5], [0, 4], [1, 500], [0, 1], [0, 1], [0, 1], [1, 100], [0, 10], [0, 10], [-10, 10], [-10, 10], [-10, 10], [0, 1], [0, 3], 
[0, 10], [-10, 10], [-10, 10], [0, 4], [-2, 2], [-2, 2], [0, 360], [0, 1], [0, 1], [-10, 10], [-10, 10], [-10, 10], [-10, 10], [0, 1], [0, 10], 
[0, 1]]
nPart_partRanges = [[0, 100], [0, 20], [0, 50], [0, 10], [0, 10], [0, 10], [0, 10], [0, 10], [0, 10], [0, 1], [0, 1], [0, 2], [0, 10], 
[0, 10], [0, 50], [0, 1], [0, 7], [0, 2], [-10, 10], [-10, 10], [0, 100], [0, 7], [0, 50], [0, 1], [0, 1], [0, 1], [0, 50], [0, 1], [0, 50], [0, 1]]
nPart_nucleusRanges = [[0, 100], [0, 10], [0, 50], [-360, 360], [-360, 360], [0, 1], [-360, 360], 
[0, 1], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [-20, 20], [0, 1], [0, 1], [0, 2], [0, 10], [0, 10]]
    ##
    ## KEYFRAME ATTRIBUTES
keyFrame_attrs = ['rate', 'windSpeed', 'windDirectionX','windDirectionY', 'windDirectionZ', 'windNoise', 'lifespan', 'radius', 'speedRandom']

#image manipulation variables
maya_rootDirectory = mc.workspace(query = True, rootDirectory = True)
outputFolder_default = ''.join([maya_rootDirectory, 'simHelper Output']).replace('/','\\')
playblastFolder_default = '\\'.join([outputFolder_default, 'playblasts\\'])
targetImagePath_default = '\\'.join([outputFolder_default, 'images', 'backgroundPlate.psd'])
settingsFolder_default = '\\'.join([outputFolder_default, 'settings\\'])

#frame range
startFrame = int(mc.playbackOptions(query = True, minTime = True))
endFrame = int(mc.playbackOptions(query = True, maxTime = True))
frameRange = [startFrame, endFrame]
allKeyframes_list = []

for i in range(startFrame, endFrame+1):
    allKeyframes_list.append(i)


### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###



class loadSettings:

#-----------------------------------------------------------------------------------------------------------#

    def __init__(self, loadPlayblast_paths, settingsPath, shortSettingFileName, fluidContainer_node, fluidEmitter_node,
    partEmitter_node, part_node, nucleus_node, influence_list):
        self.sel = max.sel()
        self.settingsPath = settingsPath
        self.settingFileName = shortSettingFileName
        self.influence_list = influence_list
        self.playblasts = loadPlayblast_paths
        self.keyFrame_attrs = keyFrame_attrs
        
        #node names
        self.fluidContainer_node = fluidContainer_node
        self.fluidEmitter_node = fluidEmitter_node
        self.partEmitter_node = partEmitter_node
        self.part_node = part_node
        self.nucleus_node = nucleus_node
        
        self.fluidExistCheck()
 
#-----------------------------------------------------------------------------------------------------------#

    def fluidExistCheck(self):
        #import settings module      
        self.module = self.settingFileName
        self.modulePath = self.settingsPath
        
        settings = imp.load_source(self.module, self.modulePath)
        del sys.modules[self.module]
        
        #run applySettings-function for each object in the two lists
        if self.fluidContainer_node != [u'']:          
            self.applySettings(self.fluidContainer_node, 'fluid_container')
        if self.fluidEmitter_node != [u'']:          
            self.applySettings(self.fluidEmitter_node, 'fluid_emitter')
        if self.partEmitter_node != [u'']:          
            self.applySettings(self.partEmitter_node, 'partEmitter')
        if self.part_node != [u'']:          
            self.applySettings(self.part_node, 'partNode')
        if self.nucleus_node != [u'']:          
            self.applySettings(self.nucleus_node, 'nucleusNode')        
 
#-----------------------------------------------------------------------------------------------------------#

    def applySettings(self, objectNames, objectType):
        #re-import module and get settings from module
        settingsFile = imp.load_source(self.module, self.modulePath)
        
        #get general settings
        all_objectSpecific_settings = []
        for playblast in self.playblasts:
            #remove double slashes
            playblast = playblast.decode('string_escape')

            general_settings = settingsFile.getSettings(playblast)

            #get object-specific settings       
            if objectType == 'fluid_emitter':
                objectSpecificSettings_dictionary = general_settings[0]
            elif objectType == 'fluid_container':
                objectSpecificSettings_dictionary = general_settings[1]
            elif objectType == 'partEmitter':
                objectSpecificSettings_dictionary = general_settings[2]
            elif objectType == 'partNode':
                objectSpecificSettings_dictionary = general_settings[3]
            elif objectType == 'nucleusNode':
                objectSpecificSettings_dictionary = general_settings[4]

            all_objectSpecific_settings.append(objectSpecificSettings_dictionary)
        
        attrList = objectSpecificSettings_dictionary.keys()

        #apply settings
        print('objectNames:', str(objectNames))
        for objectName in objectNames:
            for attr in attrList:
                #calculate average value
                if not attr in self.keyFrame_attrs:
                    sumValue = 0
                    main_playblast_setting = all_objectSpecific_settings[0]
                    main_playblast_value = main_playblast_setting[attr]
                    blendSum = 0
                    for specificSetting, influence in zip(all_objectSpecific_settings, self.influence_list):
                        current_value = specificSetting[attr]
                        if not current_value == main_playblast_value:
                            blendValue = current_value
                            deltaValue = (main_playblast_value - blendValue) * (float(influence) / 100.0)
                            blendSum += deltaValue
                    value = main_playblast_value - blendSum
                else:
                    value = objectSpecificSettings_dictionary[attr]

                objectAttribute = ''.join([objectName, '.', attr])
                
                # add keyframe functionality to appropriate attrs
                if attr in self.keyFrame_attrs:
                    # delete old keyframes
                    mc.cutKey(objectName, attribute = attr)
                    
                    for this_keyframe in value:
                        this_value = this_keyframe[1]
                        this_time = this_keyframe[0]
                        mc.setAttr(objectAttribute, this_value)
                        mc.setKeyframe(objectName, time = this_time, attribute = attr, respectKeyable = True)
                else:
                    mc.setAttr(objectAttribute, value)
                  
### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###

class produceSettings:
    def __init__(self, userDefinedEmitterAttrs, userDefinedContainerAttrs, playblastFolder, playblastName,
    randomPercentage, allocatedTime, settingFolder, fluidCont_name, fluidEmit_name, partEmit_name, 
    part_name, nucleus_name, userDefined_nPart_emitterAttrs, userDefined_nPart_partAttrs, 
    userDefined_nPart_nucleusAttrs, multiAttr):
        
        ## RANGES
        self.emitterRanges = emitterRanges
        self.containerRanges = containerRanges
        self.nPart_emitterRanges = nPart_emitterRanges
        self.nPart_partRanges = nPart_partRanges
        self.nPart_nucleusRanges = nPart_nucleusRanges
        self.frameRange = frameRange
        self.allKeyframes_list = allKeyframes_list
        
        ## DEFAULT ATTRS
        self.defaultEmitterAttrs = fluidEmitterAttrs
        self.defaultContainerAttrs = fluidContainerAttrs
        self.default_nPart_emitterAttrs = default_nPart_emitterAttrs
        self.default_nPart_partAttrs = default_nPart_partAttrs
        self.default_nPart_nucleusAttrs = default_nPart_nucleusAttrs
        self.keyFrame_attrs = keyFrame_attrs
        
        ## USER-DEFINED ATTRS
        self.userDefinedContainerAttrs = userDefinedContainerAttrs
        self.userDefinedEmitterAttrs = userDefinedEmitterAttrs
        self.userDefined_nPart_emitterAttrs = userDefined_nPart_emitterAttrs
        self.userDefined_nPart_partAttrs = userDefined_nPart_partAttrs
        self.userDefined_nPart_nucleusAttrs = userDefined_nPart_nucleusAttrs
        
        ## NODES
            ## all node names
        self.emitterNode = fluidEmit_name
        self.containerNode = fluidCont_name
        self.nPart_emitterNode = partEmit_name
        self.nPart_partNode = part_name
        self.nPart_nucleusNode = nucleus_name

            ## list of not-empty node names
        def filterOut_emptyLists(inputNodes, userAttrCollection, defaultAttrCollection):
            nodeList = []
            allUserAttrs = []
            allDefaultAttrs = []
            for node, userAttrs, defaultAttrs in zip(inputNodes, userAttrCollection, defaultAttrCollection):
                if node != '':
                    allUserAttrs.append(userAttrs)
                    allDefaultAttrs.append(defaultAttrs)
                    nodeList.append(node)
            return [nodeList, allUserAttrs, allDefaultAttrs]
        self.filteredLists = filterOut_emptyLists([fluidCont_name, fluidEmit_name, partEmit_name,
            part_name, nucleus_name], [userDefinedContainerAttrs, userDefinedEmitterAttrs, 
            userDefined_nPart_emitterAttrs, userDefined_nPart_partAttrs, userDefined_nPart_nucleusAttrs],
            [fluidContainerAttrs, fluidEmitterAttrs, default_nPart_emitterAttrs, default_nPart_partAttrs,
            default_nPart_nucleusAttrs])
        self.allDefaultAttrs = self.filteredLists[2]
        self.allUserAttrs = self.filteredLists[1]
        self.nodeList = self.filteredLists[0]

        ## FOLDERS AND FILENAMES
        self.settingFolder = settingFolder
        self.playblastFolder = playblastFolder
        self.playblastName = playblastName
        self.settingList = []
        self.playblastPaths = []
        
        ## OTHER USER SETTINGS
        self.randomPercentage = randomPercentage
        self.allocatedTime = float(allocatedTime)
        self.multiAttr = multiAttr
        print('core multiAttr value:', str(multiAttr))
        
        #get most recent existing path of settings file
        self.settingFileName = 'fluidTrials_settings'
        self.settingsPath = ''.join([self.settingFolder, '\\', self.settingFileName, '.py'])
        if os.path.exists(self.settingsPath):
            self.pathExists = True
        else:
            self.pathExists = False
        
        #set container to dynamic grid
        if self.containerNode != '':
            mc.setAttr(''.join([self.containerNode, '.temperatureMethod']), 2) 
            mc.setAttr(''.join([self.containerNode, '.fuelMethod']), 2) 
        
        #run production session
        self.change_visibility(0)
        self.getCurrentVals()

        self.start_time = time.time()
        self.elapsed_time = 0.0
        self.simulationCount = 0
        print('allocated time:', str(self.elapsed_time))
        if self.multiAttr:
            self.runCycle()
        else:
            enough_time = True
            while enough_time:
                for userAttrs, defaultAttrs in zip(self.allUserAttrs , self.allDefaultAttrs):
                    userAttrIndex = 0
                    userAttrs_listLength = len(userAttrs)
                    for userAttr, defaultAttr in zip(userAttrs, defaultAttrs):
                        #correct index values which are larger than the total list length
                        i = 0
                        while True:
                            try:
                                inputAttr = userAttrs[userAttrIndex - (userAttrs_listLength*i)]
                                break
                            except:
                                i += 1

                        #get default attr index by searching for the inputAttr in the defaultAttrs list
                        defaultAttrIndex = defaultAttrs.index(inputAttr)

                        #initiate single-attr production
                        self.singleAttr_production(inputAttr, defaultAttrIndex)

                        #if there's no more time, break the loops
                        if (self.elapsed_time + 0.5) >= self.allocatedTime:
                            enough_time = False
                            break
                        userAttrIndex += 1
                    if not enough_time:
                        break

        #conclude cycle
        self.cycleConclusion()
 
#-----------------------------------------------------------------------------------------------------------#
        
    def change_visibility(self, visibility):
        if self.emitterNode != '':
            fullAttribute = ''.join([self.emitterNode, '.visibility'])
            mc.setAttr(fullAttribute, visibility)
                
        if self.containerNode != '':
            fullAttribute = ''.join([self.containerNode, '.boundaryDraw'])
            mc.setAttr(fullAttribute, 5 - visibility)
                
        if self.nPart_emitterNode != '':
            fullAttribute = ''.join([self.nPart_emitterNode, '.visibility'])
            mc.setAttr(fullAttribute, visibility)
                
        if self.nPart_partNode != '':
            fullAttribute = ''.join([self.nPart_partNode, '.visibility'])
            mc.setAttr(fullAttribute, visibility)
                
        if self.nPart_nucleusNode != '':
            fullAttribute = ''.join([self.nPart_nucleusNode, '.visibility'])
            mc.setAttr(fullAttribute, visibility)
            
        if visibility == 0:
            mel.eval('modelEditor -e -grid false modelPanel1;')
            mel.eval('modelEditor -e -grid false modelPanel2;')
            mel.eval('modelEditor -e -grid false modelPanel3;')
            mel.eval('modelEditor -e -grid false modelPanel4;')
            self.user_backgroundColor = mc.displayRGBColor("background", query = True)
            black_background_color = [0, 0, 0]
            mc.displayRGBColor("background", black_background_color[0], black_background_color[1], black_background_color[2])
            mel.eval('modelEditor -e -hud false modelPanel1;')
            mel.eval('modelEditor -e -hud false modelPanel2;')
            mel.eval('modelEditor -e -hud false modelPanel3;')
            mel.eval('modelEditor -e -hud false modelPanel4;')
        else:
            mel.eval('modelEditor -e -grid true modelPanel1;')
            mel.eval('modelEditor -e -grid true modelPanel2;')
            mel.eval('modelEditor -e -grid true modelPanel3;')
            mel.eval('modelEditor -e -grid true modelPanel4;')
            mc.displayRGBColor("background", self.user_backgroundColor[0], self.user_backgroundColor[1], self.user_backgroundColor[2])
            mel.eval('modelEditor -e -hud true modelPanel1;')
            mel.eval('modelEditor -e -hud true modelPanel2;')
            mel.eval('modelEditor -e -hud true modelPanel3;')
            mel.eval('modelEditor -e -hud true modelPanel4;')
 
#-----------------------------------------------------------------------------------------------------------#
            
    def getCurrentVals(self): 
        def getValues(attrList,node):
            currentValueLibrary = {}
            for attr in attrList:
                attrName = ''.join([node, '.', attr])
                attrVal = mc.getAttr(attrName)
                currentValueLibrary[attr] = attrVal
            return currentValueLibrary
        
        if self.emitterNode != '':    
            self.currentEmitterVals_library = getValues(self.defaultEmitterAttrs,self.emitterNode)
        if self.containerNode != '':
            self.currentContainerVals_library = getValues(self.defaultContainerAttrs,self.containerNode)
        if self.nPart_emitterNode != '':
            self.current_nPart_emitterVals_library = getValues(self.default_nPart_emitterAttrs,self.nPart_emitterNode)
        if self.nPart_partNode != '':
            self.current_nPart_partVals_library = getValues(self.default_nPart_partAttrs,self.nPart_partNode)
        if self.nPart_nucleusNode != '':
            self.current_nPart_nucleusVals_library = getValues(self.default_nPart_nucleusAttrs,self.nPart_nucleusNode)
 
#-----------------------------------------------------------------------------------------------------------#
            
    def runCycle(self): 
        while (self.elapsed_time + 0.5) <= self.allocatedTime:
            #create random values
            def calculateRangeLength(rangeList, currentVal_library, defaultAttrList):
                randomVals_library = {}
                for this_range, attr in zip(rangeList, defaultAttrList):
                    currentValue = currentVal_library[attr]
                    minimum = this_range[0]
                    maximum = this_range[1]
                    lowerHalfLength = currentValue - minimum
                    upperHalfLength = maximum - currentValue
                    
                    newMinimum = lowerHalfLength / 100 * self.randomPercentage
                    newMaximum = upperHalfLength / 100 * self.randomPercentage
                    
                    #add keyframing functionality for appropriate attrs
                    if attr in self.keyFrame_attrs:
                        maximum_amount_of_frames = len(self.allKeyframes_list)
                        keyframe_amount = random.randint(1, 10)
                        keyframe_list = []
                        
                        for i in range(keyframe_amount):
                            current_frameNumber = random.randint(0, maximum_amount_of_frames)
                            randomVal = random.uniform(-newMinimum, newMaximum)
                            keyframe_list.append([current_frameNumber, randomVal])
                        randomVals_library[attr] = keyframe_list
                    else:
                        randomVal = random.uniform(-newMinimum, newMaximum)
                        randomVals_library[attr] = randomVal
                        
                return randomVals_library
            
            if self.emitterNode != '':
                self.emitterRandVals_library = calculateRangeLength(self.emitterRanges, self.currentEmitterVals_library, self.defaultEmitterAttrs)
            if self.containerNode != '':
                self.containerRandVals_library = calculateRangeLength(self.containerRanges, self.currentContainerVals_library, self.defaultContainerAttrs)
            if self.nPart_emitterNode != '':
                self.nPart_emitterRandVals_library = calculateRangeLength(self.nPart_emitterRanges, self.current_nPart_emitterVals_library, self.default_nPart_emitterAttrs)
            if self.nPart_partNode != '':
                self.nPart_partRandVals_library = calculateRangeLength(self.nPart_partRanges, self.current_nPart_partVals_library, self.default_nPart_partAttrs)
            if self.nPart_nucleusNode != '':
                self.nPart_nucleusRandVals_library = calculateRangeLength(self.nPart_nucleusRanges, self.current_nPart_nucleusVals_library, self.default_nPart_nucleusAttrs)
                
            #generate new assignments
            def generateAssignments(userDefinedAttrs, library, randomVal_library) :
                newAssignments_library = {}
                leftoverAttrs = library.keys()

                def calc_correctionFactor(power):
                    x = random.uniform(0.0, 1.0)
                    y = math.pow(x,power)
                    return y

                for userAttr, randVal in zip(userDefinedAttrs, randomVal_library):
                    #remove attr from default attr list
                    leftoverAttrs.remove(userAttr)
                    
                    randVal = randomVal_library[userAttr]
                    currentVal = library[userAttr]
                    
                    ## EXCEPTIONS
                        ##
                        ## add keyframe functionality for appropriate attrs
                    if userAttr in self.keyFrame_attrs:  
                        keyframe_list = []
                        for this_keyframe in randVal:
                            keyframe_randVal = this_keyframe[1]
                            keyframe_number = this_keyframe[0]
                            new_keyframeValue = currentVal + keyframe_randVal
                            
                            #apply correction to value
                            correction_factor = random.uniform(.2,1)
                            new_keyframeValue = new_keyframeValue * correction_factor
                            
                            #reduce extremes of highly disruptive attributes
                            if (userAttr == 'windSpeed'):
                                power = 4
                                correctionFactor = calc_correctionFactor(power)
                                new_keyframeVajlue = new_keyframeValue * correctionFactor
                            
                            keyframe_list.append([keyframe_number, new_keyframeValue])
                        newAssignments_library[userAttr] = keyframe_list
                    else:
                        new_value = currentVal + randVal
                        
                        ##
                        ## reduce extremes of highly disruptive attributes
                    if (userAttr == 'gravity' or userAttr == 'airDensity'):
                        if userAttr == 'gravity':
                            new_value = new_value / 5
                            power = 5
                        else:
                            power = 3
                        correctionFactor = calc_correctionFactor(power)
                        new_value = new_value * correctionFactor
                        
                        ##
                        ## remove problematic values of nparticle 'emitterType' attribute:
                    if userAttr == 'emitterType' and ((new_value == 2) or (new_value == 3)):
                        if new_value == 2:
                            new_value = 1
                        else:
                            new_value = 4
                    
                    #add exception for keyframed attributes
                    if not userAttr in self.keyFrame_attrs:     
                        newAssignments_library[userAttr] = new_value
                          
                #add default attrs that have not yet been included in the assignment list
                for attr in leftoverAttrs:
                    value = library[attr]
                    
                    #add keyframe functionality for appropriate attrs
                    if attr in self.keyFrame_attrs:
                        currentFrame = int(mc.currentTime(query = True))
                        value = [[currentFrame, value]]
                    
                    newAssignments_library[attr] = value
                        
                return newAssignments_library
            
            if self.emitterNode != '':
                self.newEmitterAssignments = generateAssignments(self.userDefinedEmitterAttrs, self.currentEmitterVals_library, self.emitterRandVals_library)
            if self.containerNode != '':
                self.newContainerAssignments = generateAssignments(self.userDefinedContainerAttrs, self.currentContainerVals_library, self.containerRandVals_library)
            if self.nPart_emitterNode != '':
                self.new_nPart_emitterAssignments = generateAssignments(self.userDefined_nPart_emitterAttrs, self.current_nPart_emitterVals_library, self.nPart_emitterRandVals_library)
            if self.nPart_partNode != '':
                self.new_nPart_partAssignments = generateAssignments(self.userDefined_nPart_partAttrs, self.current_nPart_partVals_library, self.nPart_partRandVals_library)
            if self.nPart_nucleusNode != '':
                self.new_nPart_nucleusAssignments = generateAssignments(self.userDefined_nPart_nucleusAttrs, self.current_nPart_nucleusVals_library, self.nPart_nucleusRandVals_library)
 
            #set attributes
            def setAttributes(node, assignmentDictionary, userAttrs):
                for userAttr in userAttrs:
                    fullAttribute = ''.join([node, '.', userAttr])
                    value = assignmentDictionary[userAttr]
                    
                    # add keyframe functionality to appropriate attrs
                    if userAttr in self.keyFrame_attrs:
                        #delete old keyframes
                        mc.cutKey(node, attribute = userAttr)
                        
                        for this_keyframe in value:
                            this_value = this_keyframe[1]
                            this_time = this_keyframe[0]
                            mc.setAttr(fullAttribute, this_value)
                            mc.setKeyframe(node, time = this_time, attribute = userAttr, respectKeyable = True)
                    else:
                        mc.setAttr(fullAttribute, value)
            
            if self.emitterNode != '':
                setAttributes(self.emitterNode, self.newEmitterAssignments, self.userDefinedEmitterAttrs)
            if self.containerNode != '':
                setAttributes(self.containerNode, self.newContainerAssignments, self.userDefinedContainerAttrs)
            if self.nPart_emitterNode != '':
                setAttributes(self.nPart_emitterNode, self.new_nPart_emitterAssignments, self.userDefined_nPart_emitterAttrs)
            if self.nPart_partNode != '':
                setAttributes(self.nPart_partNode, self.new_nPart_partAssignments, self.userDefined_nPart_partAttrs)
            if self.nPart_nucleusNode != '':
                setAttributes(self.nPart_nucleusNode, self.new_nPart_nucleusAssignments, self.userDefined_nPart_nucleusAttrs)
            
            #write playblast
            playblastPath = self.create_playblast(self.playblastName)

            #append current settings to settings list
            current_settingsList = []
            if self.emitterNode != '':
                current_settingsList.append(self.newEmitterAssignments)
            else:
                current_settingsList.append({})
                
            if self.containerNode != '':
                current_settingsList.append(self.newContainerAssignments)
            else:
                current_settingsList.append({})
                
            if self.nPart_emitterNode != '':
                current_settingsList.append(self.new_nPart_emitterAssignments)
            else:
                current_settingsList.append({})
                
            if self.nPart_partNode != '':
                current_settingsList.append(self.new_nPart_partAssignments)
            else:
                current_settingsList.append({})
                
            if self.nPart_nucleusNode != '':
                current_settingsList.append(self.new_nPart_nucleusAssignments)
            else:
                current_settingsList.append({})
            
            #update elapsed time
            current_time = time.time()
            self.elapsed_time = (current_time - self.start_time) / 60.0
            print('Sim number:', str(self.simulationCount))
            print('elapsed time (seconds):', str(self.elapsed_time * 60))
            
            #save current settings
            self.saveSettings(current_settingsList, playblastPath)

    def create_playblast(self, playblastName):
        ## check if playblast file exists
        j=0
        pathExists=True 
        while True:
            #print('playblastPath while-loop')
            playblastIndex = str(j+1)
            while len(playblastIndex) < 4:
                playblastIndex = '0' + playblastIndex
            j += 1
            playblastPath = self.playblastFolder + playblastName + '_' + playblastIndex + '.mov'
            if not os.path.isfile(playblastPath):
                break
        
            ## create fileName and write playblasts        
        self.playblastPaths.append(playblastPath)
        print 'filePath: ' + playblastPath
        
        self.simulationCount += 1
        mc.playblast(format = 'qt', widthHeight = [1280, 720], viewer = False, filename = playblastPath, sequenceTime = 0, 
        clearCache = 1, showOrnaments = 1, fp = 4, percent = 100, compression = 'H.264', quality = 100)
        
        return playblastPath

    def cycleConclusion(self):
        #return nodes to original settings
        if self.emitterNode != '':
            for attr in self.defaultEmitterAttrs:
                value = self.currentEmitterVals_library[attr]
                fullAttr = ''.join([self.emitterNode, '.', attr])
                mc.setAttr(fullAttr, value)
        if self.containerNode != '':
            for attr in self.defaultContainerAttrs:
                value = self.currentContainerVals_library[attr]
                fullAttr = ''.join([self.containerNode, '.', attr])
                mc.setAttr(fullAttr, value)
        if self.nPart_emitterNode != '':
            for attr in self.default_nPart_emitterAttrs:
                value = self.current_nPart_emitterVals_library[attr]
                fullAttr = ''.join([self.nPart_emitterNode, '.', attr])
                mc.setAttr(fullAttr, value)
        if self.nPart_partNode != '':
            for attr in self.default_nPart_partAttrs:
                value = self.current_nPart_partVals_library[attr]
                fullAttr = ''.join([self.nPart_partNode, '.', attr])
                mc.setAttr(fullAttr, value)
        if self.nPart_nucleusNode != '':
            for attr in self.default_nPart_nucleusAttrs:
                value = self.current_nPart_nucleusVals_library[attr]
                fullAttr = ''.join([self.nPart_nucleusNode, '.', attr])
                mc.setAttr(fullAttr, value)

        #return UI elements to original states after runcycle is done
        self.change_visibility(1)
 
#-----------------------------------------------------------------------------------------------------------#
 
    def singleAttr_production(self, inputAttr, attrIndex):
        #calculate correction factor
        def calc_correctionFactor(power):
            x = random.uniform(0.0, 1.0)
            y = math.pow(x,power)
            return y

        ## CREATE NEW SINGLE ASSIGNMENT
        def generate_singleAssignment(range, currentValue, attr):
            ## CREATE RANDOM VALUE
            minimum = range[0]
            maximum = range[1]
            lowerHalfLength = currentValue - minimum
            upperHalfLength = maximum - currentValue
            
            newMinimum = lowerHalfLength / 100 * self.randomPercentage
            newMaximum = upperHalfLength / 100 * self.randomPercentage

                ## add keyframing functionality for appropriate attrs
            if attr in self.keyFrame_attrs:
                timeLine_length = len(self.allKeyframes_list)
                keyframe_amount = random.randint(1, 10)
                keyframe_list = []
                
                for i in range(keyframe_amount):
                    current_frameNumber = random.randint(0, timeLine_length)
                    randomVal = random.uniform(-newMinimum, newMaximum)
                    keyframe_list.append([current_frameNumber, randomVal])
                randomVal = keyframe_list
            else:
                randomVal = random.uniform(-newMinimum, newMaximum)

            ## CREATE ASSIGNMENT
                ## add keyframe functionality for appropriate attrs
            if attr in self.keyFrame_attrs:  
                keyframe_list = []
                for this_keyframe in randomVal:
                    keyframe_randVal = this_keyframe[1]
                    keyframe_number = this_keyframe[0]
                    new_keyframeValue = currentValue + keyframe_randVal
                    
                    #apply correction to value
                    correction_factor = random.uniform(.2,1)
                    new_keyframeValue = new_keyframeValue * correction_factor
                    
                    #reduce extremes of highly disruptive attributes
                    if (attr == 'windSpeed'):
                        power = 4
                        extra_correctionFactor = calc_correctionFactor(power)
                        new_keyframeValue = new_keyframeValue * extra_correctionFactor
                    
                    keyframe_list.append([keyframe_number, new_keyframeValue])
                new_value = keyframe_list
            else:
                new_value = currentValue + randomVal

                ##
                ## reduce extremes of highly disruptive attributes
            if (attr == 'gravity' or attr == 'airDensity'):
                if attr == 'gravity':
                    new_value = new_value / 5
                    power = 5
                else:
                    power = 3
                correctionFactor = calc_correctionFactor(power)
                new_value = new_value * correctionFactor
                
                ##
                ## remove problematic values of nParticle 'emitterType' attribute:
            if attr == 'emitterType' and ((new_value == 2) or (new_value == 3)):
                if new_value == 2:
                    new_value = 1
                else:
                    new_value = 4

            return new_value

        if inputAttr in self.defaultEmitterAttrs:
            inputAttr_value = generate_singleAssignment(self.emitterRanges[attrIndex], 
                self.currentEmitterVals_library[inputAttr], inputAttr)
        elif inputAttr in self.defaultContainerAttrs:
            inputAttr_value = generate_singleAssignment(self.containerRanges[attrIndex], 
                self.currentContainerVals_library[inputAttr], inputAttr)
        elif inputAttr in self.default_nPart_emitterAttrs:
            inputAttr_value = generate_singleAssignment(self.nPart_emitterRanges[attrIndex], 
                self.current_nPart_emitterVals_library[inputAttr], inputAttr)
        elif inputAttr in self.default_nPart_partAttrs:
            inputAttr_value = generate_singleAssignment(self.nPart_partRanges[attrIndex], 
                self.current_nPart_partVals_library[inputAttr], inputAttr)
        elif inputAttr in self.default_nPart_nucleusAttrs:
            inputAttr_value = generate_singleAssignment(self.nPart_nucleusRanges[attrIndex], 
                self.current_nPart_nucleusVals_library[inputAttr], inputAttr)
        else:
            max.errorPrompt('''
                Error: Specified Attribute was not found (Single-Attr Trial Session Aborted).
                ''', '''Aborted''').show()
            return

        ## CREATE NEW SETTINGS LIST
        def createAndApply_settings(inputAttr_value, currentVals_library, node, defaultAttrs):
            settingsDictionary = dict(currentVals_library)
            if inputAttr in currentVals_library:
                del settingsDictionary[inputAttr]
                settingsDictionary[inputAttr] = inputAttr_value
                print('changing value on ', inputAttr, str(inputAttr_value))

            for attr in defaultAttrs:
                fullAttribute = ''.join([node, '.', attr])
                value = settingsDictionary[attr]
                
                # add keyframe functionality to appropriate attrs
                if attr in self.keyFrame_attrs:
                    #delete old keyframes
                    mc.cutKey(node, attribute = attr)
                    
                    for this_keyframe in value:
                        this_value = this_keyframe[1]
                        this_time = this_keyframe[0]
                        mc.setAttr(fullAttribute, this_value)
                        mc.setKeyframe(node, time = this_time, attribute = attr, respectKeyable = True)
                else:
                    mc.setAttr(fullAttribute, value)  

            return settingsDictionary  
        
        current_settingsList = []    
        if self.emitterNode != '':
            self.newEmitterAssignments = createAndApply_settings(inputAttr_value, 
                self.currentEmitterVals_library, self.emitterNode, self.defaultEmitterAttrs)
            current_settingsList.append(self.newEmitterAssignments)
        else:
            current_settingsList.append({})
        if self.containerNode != '':
            self.newContainerAssignments = createAndApply_settings(inputAttr_value, 
                self.currentContainerVals_library, self.containerNode, self.defaultContainerAttrs)
            current_settingsList.append(self.newContainerAssignments)
        else:
            current_settingsList.append({})
        if self.nPart_emitterNode != '':
            self.new_nPart_emitterAssignments = createAndApply_settings(inputAttr_value, 
                self.current_nPart_emitterVals_library, self.nPart_emitterNode, self.default_nPart_emitterAttrs)
            current_settingsList.append(self.new_nPart_emitterAssignments)
        else:
            current_settingsList.append({})
        if self.nPart_partNode != '':
            self.new_nPart_partAssignments = createAndApply_settings(inputAttr_value, 
                self.current_nPart_partVals_library, self.nPart_partNode, self.default_nPart_partAttrs)
            current_settingsList.append(self.new_nPart_partAssignments)
        else:
            current_settingsList.append({})
        if self.nPart_nucleusNode != '':
            self.new_nPart_nucleusAssignments = createAndApply_settings(inputAttr_value, 
                self.current_nPart_nucleusVals_library, self.nPart_nucleusNode, self.default_nPart_nucleusAttrs)
            current_settingsList.append(self.new_nPart_nucleusAssignments)
        else:
            current_settingsList.append({})

        #write playblast
        playblastName = ''.join([inputAttr, '--', self.playblastName, ])
        playblastPath = self.create_playblast(playblastName)

        #update elapsed time
        current_time = time.time()
        self.elapsed_time = (current_time - self.start_time) / 60.0
        print('Sim number:', str(self.simulationCount))
        print('elapsed time (mins:secs):', str(int(round(self.elapsed_time, 0))), ':', 
            str((self.elapsed_time - round(self.elapsed_time, 0)) * 60))
        
        #save current settings
        self.saveSettings(current_settingsList, playblastPath)

#-----------------------------------------------------------------------------------------------------------#

    def saveSettings(self, current_settingsList, playblastPath):
        print('---------- saving current settings ----------')
        if not self.pathExists:
            f = open(self.settingsPath,'w')
            f.write('#Fluid Settings Module \n')
            f = open(self.settingsPath,'a')
            f.write('def getSettings(playblast): \n')
            self.pathExists = True
        else:
            f = open(self.settingsPath,'a')
        f.write(''.join(['    if playblast == "', playblastPath,'" : ','\n']))
        f.write(''.join(['        ', 'return ', str(current_settingsList), ' \n']))
        f.close()
        
        print '---------- SETTINGS SAVED ----------'


### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###
### --------------------------------------------------------------------------- ###


class create_backgroundPlate:
    def __init__(self, outDirectory = "\\".join([outputFolder_default, 'images'])):
        #variables
        backGroundPlate_fullPath = ''.join([outDirectory,'\\backgroundPlate', '.psd'])
        currentFrame_int = int(mc.currentTime(query = True))
        
        #check if outDir exists and take snapshot
        if not os.path.isdir(outDirectory):
            os.makedirs(outDirectory)
        mc.playblast(format = 'image', viewer = False, completeFilename = backGroundPlate_fullPath, forceOverwrite = True, sequenceTime = 0, startTime = currentFrame_int, compression = 'PSD', widthHeight = [1280, 720], endTime = currentFrame_int, clearCache = 1, showOrnaments = 1, fp=4, percent = 100, quality = 100)
    
        print('background plate fullpath:', backGroundPlate_fullPath)
        subprocess.Popen(r'explorer /select, ' + backGroundPlate_fullPath)









