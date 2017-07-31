# TRANSFER ATTRIBUTES TOOL
import maya.cmds as mc
import max
from PySide import QtCore as qc
from PySide import QtGui as qg
from functools import partial

def Core(checkbox_values):
    print('Running Script: Transfer Attributes')
    
    # vraag selectie op
    selectie = mc.ls(orderedSelection = True)
    
    # check of er tenminste 2 objecten geselecteerd zijn
    if len(selectie) >= 2:
        
        # vind eerstgeselecteerde object
        eersteObject = selectie[0]
        
        # maak attribute lijst
        attributes = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ',
        'scaleX', 'scaleY', 'scaleZ']
        
        # vraag attribuut waardes op en pas ze toe op de doelobjecten
        for attribute, value in zip(attributes, checkbox_values):
            print(value)
            if not value == 0:
                waarde = mc.getAttr(eersteObject + '.' + attribute)
                
                for doelObject in selectie:
                    mc.setAttr(doelObject + '.' + attribute, waarde)
            

class GUI(qg.QDialog):
    def __init__(self):
        qg.QDialog.__init__(self)
        
        # window setup
        self.setWindowTitle('TransferAttrs')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setMinimumWidth(250)
        
        # main layout
        self.mainLayout = qg.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        # add widgets
        self.checkbox_list = []
        for attribute in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ',
            'scaleX', 'scaleY', 'scaleZ']:
            checkbox = max.CheckBox_custom(attribute)
            checkbox.setChecked(True)
            self.mainLayout.addWidget(checkbox)
            self.checkbox_list.append(checkbox)
            
        # add button
        self.mainLayout.addWidget(qg.QLabel(''))
        button = max.PushButton_custom('Transfer')
        self.mainLayout.addWidget(button)
        
        # connections
        button.clicked.connect(partial(self.runCore))
        
    def runCore(self):
        # get user input
        checkbox_values = []
        for checkbox in self.checkbox_list:
            value = checkbox.checkState()
            checkbox_values.append(value)
        
        print(checkbox_values)
        
        # run Core 
        Core(checkbox_values)
        
        
GUI().show()
        
        
        
        
        
        
        
        
          
