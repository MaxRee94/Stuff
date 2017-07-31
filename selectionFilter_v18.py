#selection filter
import maya.cmds as mc
from functools import partial
import max8 as max
import random

def calculatePercentage(inputList,percentageCheck,selectionMode):
    #expand component names
    for item in inputList:
        vertices = mc.filterExpand(item,sm = 31)
        edges = mc.filterExpand(item,sm = 32)
        faces = mc.filterExpand(item,sm = 34)
        for components in [vertices, edges, faces]:
            if components != None:
                inputList.remove(item)
                for component in components:
                    inputList.append(component)
    
    #print('inputList incl. expanded components:',str(inputList))    
    
    percentMatches=[]
    if percentageCheck==1:
        percentage=mc.floatSliderGrp('slider',query=True,value=True)
        i=0
        convertedCount=int(round(float(len(inputList))*(percentage/100.0),0))
        while i < convertedCount:
            objectIndex = random.randint(0,(len(inputList)-1)) 
            if inputList[objectIndex] not in percentMatches: 
                percentMatches.append(inputList[objectIndex])
                i=i+1   
    else:  
        percentMatches=inputList
        
    #print('percentMatches:',str(percentMatches))
        
    #select objects in list
    if selectionMode==2:
        mc.select(clear=True)
    if not selectionMode==3:
        for item in percentMatches:
            try:  
                mc.select(item,add=True)
            except:
                max.errorPrompt('Error', 'The specified object could not be found')
    else:
        for item in percentMatches:
            mc.select(item,deselect=True)  

class applySelection:
    def __init__(self):
        #user input
        self.selectionMode=mc.radioButtonGrp('radioGrp',query=True,select=True)
        self.scroller=mc.textScrollList('objectType_scroller',query=True,selectItem=True)
        self.name=mc.textFieldButtonGrp('nameField',query=True,text=True)
        self.iterationCheck=mc.checkBox('iterations',query=True,value=True)
        self.widenFilterCheck=mc.checkBox('widenFilter',query=True,value=True)
        self.percentageCheck=mc.checkBox('percentage',query=True,value=True)
        #self.interactiveCheck=mc.checkBox('interactive',query=True,value=True)
        
        self.compute()
         
    def compute(self):
        allDag=[]
        #scroller filter
        for item in self.scroller:
            for s in mc.ls(type=item):
                allDag.append(s)
        print 'All objects of selected type(s): '+ str(allDag)
        
        #name filter
        matches=[]
        if not self.name=='':
            if self.widenFilterCheck==1:
                for item in allDag:
                    if all(s in item for s in self.name.split(' ')):
                        matches.append(item)
            else:
                for item in allDag:
                    if self.name==item:
                        matches.append(item)
            if self.iterationCheck==1:
                intlessName=['klwerjlsjbnolsdfjlkj']
                for letter in self.name:
                    try:
                        int(letter)
                        intlessName=self.name.split(letter)
                    except:
                        pass
                print 'intlessName: '+str(intlessName)
                for item in allDag:
                    if all(s in item for s in intlessName):
                        if not item in matches:
                            matches.append(item)
                if matches==[]:
                    matches.append(self.name)
        else:
            matches=allDag
        print 'Selecting objects: '+str(matches)
        
        #percentage
        calculatePercentage(matches,self.percentageCheck,self.selectionMode)
                                            

class GUI:
    def __init__(self,GUI_title):
        self.winname='_ID'
        self.currentSelection=mc.ls(sl=True)
        self.renewSelectionList=0
        self.scrollerContents=[]
        allNodes=mc.ls(dag=True)
        self.scrollerContents=[]
        for item in allNodes:
            item=mc.nodeType(item)
            if not any(item==s for s in self.scrollerContents):
                self.scrollerContents.append(item) 
                
        self.mainUIFunc(GUI_title)
    
    def changeVar(self,state):
        self.renewSelectionList=state
    
    def visibility(self,value,*args):
        mc.floatSliderGrp(self.slider,edit=True,enable=value)
        mc.checkBox('interactive', edit=True,enable=value)
        if value:
            self.renewSelectionList=1
        
    def interactive(self,*args):
        interactiveCheck=mc.checkBox('interactive',query=True,value=True)
        if interactiveCheck==1:
            if self.renewSelectionList==1:
                self.currentSelection=mc.ls(sl=True)
                self.renewSelectionList=0
            calculatePercentage(self.currentSelection,1,mc.radioButtonGrp('radioGrp',query=True,select=True))
        
    def mainUIFunc(self,GUI_title):
        max.windowExist(self.winname)
        mc.window(self.winname, title = GUI_title, rtf=1, menuBar = True, mbv = True)
        max.column()

        mc.radioButtonGrp('radioGrp',label='Selection Mode:',numberOfRadioButtons=3,select=2,l1='Add',l2='Replace',l3='Remove',cl4=['left','left','left','left'],cw=[1,100])
        mc.text(label='')
        mc.frameLayout(label='Object Types',collapsable=True)
        mc.textScrollList('objectType_scroller', height=100,ams=True)
        for item in self.scrollerContents:
            mc.textScrollList('objectType_scroller',edit=True,a=item)
            if item=='transform':
                mc.textScrollList('objectType_scroller',edit=True,si=item)
        mc.setParent('..')
        
        self.nameField=mc.textFieldButtonGrp('nameField',label='Object Name:',buttonLabel='Get Selection',cl3=('left','left','left'), cw3=(80,245,70), buttonCommand = partial(max.txtFieldButton,'nameField','sel'))
        mc.checkBox('iterations',label='Include Iterations')
        mc.checkBox('widenFilter',label='Include all objects containing word')
        mc.separator()
        mc.checkBox('percentage',label='Select Percentage',onCommand=partial(self.visibility,True),offCommand=partial(self.visibility,False))
        self.slider=mc.floatSliderGrp('slider',cw=[1,0],label='',enable=False,field=True,value=100.0,changeCommand=partial(self.interactive))
        mc.checkBox('interactive', label='Make Slider Interactive',enable=False,value=1,onCommand=lambda*_:self.changeVar(1), offCommand=lambda*_:self.changeVar(0))
        mc.text(label='')
        mc.button(label='Apply',command=lambda*_:applySelection())
            
        mc.showWindow(self.winname)
        
GUI('Selection Filter')

















