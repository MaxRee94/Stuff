#main GUI of auto simulator
from PySide import QtCore as qc
from PySide import QtGui as qg
from functools import partial
import max; reload(max)
import sys
import time
import os.path
import maya.mel as mel
import imp
import maya.cmds as mc
import math

#variables
dialog = None
maya_rootDirectory = mc.workspace(query = True, rootDirectory = True)


#-----------------------------------------------------------------------------------------------------------#

class simulationHelper_GUI(qg.QDialog):
    def __init__(self, dialogTitle):
        qg.QDialog.__init__(self)
        
        #input variables
        self.maya_rootDirectory = maya_rootDirectory.replace('/', '\\')
        
        #update directory names
        self.update_directories(self.maya_rootDirectory)
        
        #create color palettes
        self.orange = [150, 90, 50]
        self.cyan = [0, 130, 140]
        self.purple = [70, 30, 120]
        self.darkGrey = [20, 20, 20]
        
        #set background color
        palette = self.palette()
        custom_color = qg.QColor()
        custom_color.setRgb(53,53,53)
        palette.setColor(self.backgroundRole(), custom_color)
        self.setPalette(palette)
        
        #influence list
        self.influenceList = []

        #window setup
        self.setWindowTitle(dialogTitle)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setGeometry(1000,250,412,520)
        
        #stacked layout
        self.mainLayout = qg.QStackedLayout()
        self.setLayout(self.mainLayout)
        
        #run subLayout functions
        self.create_productionWidget()
        self.create_applicationWidget()
        self.create_homeWidget()

#-----------------------------------------------------------------------------------------------------------#
    
    def create_productionWidget(self):
        #add production widget
        self.productionWidget = qg.QWidget()
        self.productionWidget.setLayout(qg.QVBoxLayout())
        self.productionWidget.layout().setContentsMargins(5,5,5,5)
        self.productionWidget.layout().setSpacing(2) 
        self.mainLayout.addWidget(self.productionWidget)
        
        #random widgets
        emptyLineLabel2 = qg.QLabel('') 
        emptyLineLabel3 = qg.QLabel('') 
        
        #return_button
            #
            #create layout + widgets
        return_layout = qg.QWidget()
        return_layout.setLayout(qg.QHBoxLayout())
        return_button = max.PushButton_custom('<---  Back', 'SansSerif')
        return_button.setSizePolicy(qg.QSizePolicy.Expanding, qg.QSizePolicy.Expanding)
        advanced_button = max.PushButton_custom('Advanced --->')
        advanced_button.setSizePolicy(qg.QSizePolicy.Expanding, qg.QSizePolicy.Expanding)

        return_layout.layout().addWidget(return_button)
        return_layout.layout().addWidget(advanced_button)

        self.productionWidget.layout().addWidget(return_layout)
        
        #nodeFields layouts
            ##
            ## NODE FIELDS GETSELECTED LAYOUT
        nodeField_mainButton_layout = qg.QWidget()
        nodeField_mainButton_layout.setLayout(max.HBoxLayout())
        self.productionWidget.layout().addWidget(nodeField_mainButton_layout)
            ##
            ## FLUID CONTAINER NODE LAYOUT
        fluidContainer_nodeLayout = qg.QWidget()
        fluidContainer_nodeLayout.setLayout(max.HBoxLayout())
        self.productionWidget.layout().addWidget(fluidContainer_nodeLayout)
            ##
            ## FLUID EMITTER NODE LAYOUT
        fluidEmitter_nodeLayout = qg.QWidget()
        fluidEmitter_nodeLayout.setLayout(max.HBoxLayout())
        self.productionWidget.layout().addWidget(fluidEmitter_nodeLayout)
        
            ##
            ## PARTICLE EMITTER NODE LAYOUT
        particleEmitter_nodeLayout = qg.QWidget()
        particleEmitter_nodeLayout.setLayout(max.HBoxLayout())
        splitter = max.Splitter()
        self.productionWidget.layout().addWidget(splitter)
        self.productionWidget.layout().addWidget(particleEmitter_nodeLayout)
            ##
            ## PARTICLE NODE LAYOUT
        particle_nodeLayout = qg.QWidget()
        particle_nodeLayout.setLayout(max.HBoxLayout())   
        self.productionWidget.layout().addWidget(particle_nodeLayout) 
            ##
            ## NUCLEUS LAYOUT
        #emptyLine_4 = max.Label_custom()
        nucleus_nodeLayout = qg.QWidget()
        nucleus_nodeLayout.setLayout(max.HBoxLayout())
        self.productionWidget.layout().addWidget(nucleus_nodeLayout)
        #self.productionWidget.layout().addWidget(emptyLine_4)
        
        #fluid list layout
        self.listLayout = qg.QFrame()
        self.listLayout.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
        self.listLayout.setLineWidth(1)
        self.listLayout.setLayout(qg.QVBoxLayout())
        self.listLayout.setFixedHeight(40)
        self.listLayout.layout().setContentsMargins(4,4,4,6)
        self.productionWidget.layout().addWidget(self.listLayout)
        
        #particle list layout
        self.particleListLayout = qg.QFrame()
        emptyLineLabel = max.Label_custom('', 'SansSerif', 12)
        self.particleListLayout.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
        self.particleListLayout.setLineWidth(1)
        self.particleListLayout.setLayout(qg.QVBoxLayout())
        self.particleListLayout.setFixedHeight(40)
        self.particleListLayout.layout().setContentsMargins(4,4,4,6)
        self.productionWidget.layout().addWidget(self.particleListLayout)
        self.productionWidget.layout().addWidget(emptyLineLabel)
                
        #name playblast layout
        self.namingLayout = qg.QHBoxLayout()
        self.productionWidget.layout().addLayout(self.namingLayout)
        self.productionWidget.layout().addWidget(emptyLineLabel2)
        
        #simCount layout
        self.allocatedTime_layout = qg.QHBoxLayout()
        self.productionWidget.layout().addLayout(self.allocatedTime_layout)
        
        #percentage layout
        self.randomPercentageLayout = qg.QHBoxLayout()
        self.productionWidget.layout().addLayout(self.randomPercentageLayout)
        self.productionWidget.layout().addStretch()
        
        #lower button layout
        self.buttonLayout = qg.QHBoxLayout()
        self.productionWidget.layout().addLayout(self.buttonLayout)
            
        ### WIDGET GROUPS
        ###
        # Node Field Widgets
            ##
            ## MAIN BUTTON
        nodeField_main_button = max.PushButton_custom('Get Selected Objects', 'SansSerif', 12, self.cyan)
        nodeField_main_button.setMinimumWidth(240)
        nodeField_mainButton_layout.layout().addStretch()
        nodeField_mainButton_layout.layout().addWidget(nodeField_main_button)
            ##
            ## FLUID CONTAINER NODE
        fluidCont_label = max.Label_custom('Fluid Shape: ')
        self.fluidCont_lineEdit = max.LineEdit_custom()
        self.fluidCont_lineEdit.setMinimumWidth(240)
        fluidContainer_nodeLayout.layout().addWidget(fluidCont_label)
        fluidContainer_nodeLayout.layout().addStretch()
        fluidContainer_nodeLayout.layout().addWidget(self.fluidCont_lineEdit)
        
            ##
            ## FLUID EMITTER NODE
        fluidEmit_label = max.Label_custom('Fluid Emitter: ')
        self.fluidEmit_lineEdit = max.LineEdit_custom()
        self.fluidEmit_lineEdit.setMinimumWidth(240)
        fluidEmitter_nodeLayout.layout().addWidget(fluidEmit_label)
        fluidEmitter_nodeLayout.layout().addStretch()
        fluidEmitter_nodeLayout.layout().addWidget(self.fluidEmit_lineEdit)
        
            ##
            ## PARTICLE EMITTER NODE
        partEmit_label = max.Label_custom('nParticle Emitter: ')
        self.partEmit_lineEdit = max.LineEdit_custom()
        self.partEmit_lineEdit.setMinimumWidth(240)
        particleEmitter_nodeLayout.layout().addWidget(partEmit_label)
        particleEmitter_nodeLayout.layout().addStretch()
        particleEmitter_nodeLayout.layout().addWidget(self.partEmit_lineEdit)
        
            ##
            ## PARTICLE NODE
        part_label = max.Label_custom('nParticle Object: ')
        self.part_lineEdit = max.LineEdit_custom()
        self.part_lineEdit.setMinimumWidth(240)
        particle_nodeLayout.layout().addWidget(part_label)
        particle_nodeLayout.layout().addStretch()
        particle_nodeLayout.layout().addWidget(self.part_lineEdit)
        
            ##
            ## NUCLEUS NODE
        nucleus_label = max.Label_custom('Nucleus Object: ')
        self.nucleus_lineEdit = max.LineEdit_custom()
        self.nucleus_lineEdit.setMinimumWidth(240)
        nucleus_nodeLayout.layout().addWidget(nucleus_label)
        nucleus_nodeLayout.layout().addStretch()
        nucleus_nodeLayout.layout().addWidget(self.nucleus_lineEdit)
        
        ###### FLUID ATTRIBUTE LIST
        ######
            ## 
            ## LABEL LAYOUT
        self.expand_button = max.PushButton_custom('Show Fluid Attributes', 'SansSerif', 12, self.orange)
        self.listLayout.layout().addWidget(self.expand_button)
        self.listLayout.layout().addStretch(1)
        
            ##
            ## ATTRIBUTE LIST
        self.attributeListWidget = qg.QListWidget()
        self.attributeListWidget.setVisible(False) 
        self.attributeListWidget.setSelectionMode(qg.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.attributeListWidget.setFont(qg.QFont('SansSerif', 12))
        
        #add to list
        m = 0
        self.getAttributes()
        for item in self.attributeList:
            self.attributeListWidget.addItem(item)
            self.attributeListWidget.item(m).setSelected(True)
            m += 1
        
        self.listLayout.layout().addWidget(self.attributeListWidget)
        self.listLayout.layout().addStretch()
        
        ###### PARTICLE ATTRIBUTE LIST
        ######
            ##
            ## LABEL LAYOUT
        self.particle_expand_button = max.PushButton_custom('Show Particle Attributes', 'SansSerif', 12, self.cyan)
        self.particleListLayout.layout().addWidget(self.particle_expand_button)
        self.particleListLayout.layout().addStretch(1)
        
            ##
            ## ATTRIBUTE LIST
        self.particleAttributeListWidget = qg.QListWidget()
        self.particleAttributeListWidget.setVisible(False) 
        self.particleAttributeListWidget.setSelectionMode(qg.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.particleAttributeListWidget.setFont(qg.QFont('SansSerif', 12))
        
        #add to list
        n = 0
        self.getParticleAttributes()
        for item in self.particleAttributeList:
            self.particleAttributeListWidget.addItem(item)
            self.particleAttributeListWidget.item(n).setSelected(True)
            n += 1
        
        self.particleListLayout.layout().addWidget(self.particleAttributeListWidget)
        self.particleListLayout.layout().addStretch()
        
        #name playblast widgets
        self.namingLabel = max.Label_custom('Playblast Name: ', 'SansSerif', 12)
        self.namingLineEdit = max.LineEdit_custom('', 'SansSerif', 12)
        self.namingLayout.addWidget(self.namingLabel)
        self.namingLayout.addWidget(self.namingLineEdit)
        
        #allocated time widget
        self.allocatedTime_label = max.Label_custom('Allocated Time (minutes): ', 'SansSerif', 12)
        self.allocatedTime_spin = qg.QSpinBox()
        self.allocatedTime_spin.setFont(qg.QFont('SansSerif', 12))
        self.allocatedTime_spin.setRange(1, 600)
        
        self.allocatedTime_slider = qg.QSlider()
        self.allocatedTime_slider.setOrientation(qc.Qt.Horizontal)
        self.allocatedTime_slider.setRange(1, 600)
        
        self.allocatedTime_layout.addWidget(self.allocatedTime_label)
        self.allocatedTime_layout.addWidget(self.allocatedTime_slider)
        self.allocatedTime_layout.addWidget(self.allocatedTime_spin)
        
        #random percentage widget
        self.randomPercentageLabel = max.Label_custom('Amount of Randomness: ', 'SansSerif', 12)
        self.randomPercentageSpin = qg.QSpinBox()
        self.randomPercentageSpin.setFont(qg.QFont('SansSerif', 12))
        self.randomPercentageSpin.setRange(0, 100)
        
        self.randomPercentageSlider = qg.QSlider()
        self.randomPercentageSlider.setOrientation(qc.Qt.Horizontal)
        self.randomPercentageSlider.setRange(0, 100)
        
        self.randomPercentageLayout.addWidget(self.randomPercentageLabel)
        self.randomPercentageLayout.addWidget(self.randomPercentageSlider)
        self.randomPercentageLayout.addWidget(self.randomPercentageSpin)
        
        #lowest buttons
        self.whiteLabel = qg.QLabel('')
        self.trySettingsButton = max.PushButton_custom('Try Settings', 'SansSerif', 12, self.purple)
        self.productionWidget.layout().addWidget(self.trySettingsButton)
        
        def create_advancedProduction_widget():
            self.advancedApplication_widget = qg.QWidget()
            self.advancedApplication_widget.setLayout(qg.QVBoxLayout())
            self.advancedApplication_widget.setSizePolicy(qg.QSizePolicy.Maximum, qg.QSizePolicy.Maximum)
            self.advancedApplication_widget.layout().setContentsMargins(5,5,5,5)
            self.advancedApplication_widget.layout().setSpacing(0) 
            self.advancedApplication_widget.layout().setAlignment(qc.Qt.AlignTop)
            self.mainLayout.addWidget(self.advancedApplication_widget)

            #return_button
                ##
                ## create layout + widgets
            return_layout = qg.QWidget()
            return_layout.setLayout(qg.QHBoxLayout())
            return_button = max.PushButton_custom('<---  Back', 'SansSerif')
            return_button.setSizePolicy(qg.QSizePolicy.Expanding, qg.QSizePolicy.Maximum)
            return_layout.layout().addWidget(return_button)
            return_layout.layout().addStretch()

            self.advancedApplication_widget.layout().addWidget(return_layout)

            #add splitter
            splitter = max.Splitter()
            self.advancedApplication_widget.layout().addWidget(splitter)

            #add radiobutton
                ## create widgets and layout
            single_or_multiAttr_layout = qg.QWidget()
            single_or_multiAttr_layout.setLayout(qg.QHBoxLayout())
            single_or_multiAttr_layout.layout().setAlignment(qc.Qt.AlignTop)
            self.single_or_multiAttr_radioButton_multi = max.RadioButton_custom('Try all attributes at once')
            self.single_or_multiAttr_radioButton_single = max.RadioButton_custom('Try one attribute at a time')
            self.single_or_multiAttr_radioButton_multi.setChecked(True)

                ## add to layout
            single_or_multiAttr_layout.layout().addWidget(self.single_or_multiAttr_radioButton_multi)
            single_or_multiAttr_layout.layout().addWidget(self.single_or_multiAttr_radioButton_single)

                ## add layout to parentLayout
            self.advancedApplication_widget.layout().addWidget(single_or_multiAttr_layout)

            # CONNECTIONS
                ##
                ## connect return button to mainLayout
            return_button.clicked.connect(partial(self.mainLayout.setCurrentIndex, 0))    

        create_advancedProduction_widget()

        ### CONNECTIONS
            ###
            ### connect return - and advanced settings buttons to stackedlayout index
        return_button.clicked.connect(partial(self.mainLayout.setCurrentIndex, 4))
        advanced_button.clicked.connect(partial(self.mainLayout.setCurrentIndex, 1))
            ###
            ### connect widgets
        def connect_allocatedTimeWidgets(targetWidget, inputValue):
            if targetWidget == 'slider':
                if self.updateSlider:
                    converted_value = int(round(math.sqrt(inputValue * 600.0), 0))
                    self.allocatedTime_slider.setValue(converted_value)
                    self.updateSpinbox = False
                else:
                    self.updateSlider = True
            else:
                if self.updateSpinbox:
                    converted_value = math.pow((inputValue / 600.0), 2) * 600.0
                    self.allocatedTime_spin.setValue(converted_value)
                    self.updateSlider = False
                else:
                    self.updateSpinbox = True
        
        self.updateSpinbox = True
        self.updateSlider = True
        self.allocatedTime_slider.valueChanged.connect(partial(connect_allocatedTimeWidgets, 'spinbox'))
        self.allocatedTime_spin.valueChanged.connect(partial(connect_allocatedTimeWidgets, 'slider'))
        
        self.randomPercentageSlider.valueChanged.connect(self.randomPercentageSpin.setValue)
        self.randomPercentageSpin.valueChanged.connect(self.randomPercentageSlider.setValue)
        
        ## connect fluid attribute button
        def fluidExpandButton_clicked():
            #if particleList is set to expand, collapse it 
            if self.particleExpandState == 1:
                self.particle_expand_button.setText('Show Particle Attributes')
                self.particleListLayout.setFixedHeight(40)
                self.particleAttributeListWidget.setVisible(0)
                self.particleExpandState = 0
            
            if self.fluidExpandState == 1:
                self.expand_button.setText('Show Fluid Attributes')
                self.listLayout.setFixedHeight(40)
                self.attributeListWidget.setVisible(0)
                self.fluidExpandState = 0
            else:
                self.expand_button.setText('Hide Fluid Attributes')
                self.listLayout.setFixedHeight(200)
                self.attributeListWidget.setVisible(1)
                self.fluidExpandState = 1
        
        self.fluidExpandState = 0
        self.expand_button.clicked.connect(partial(fluidExpandButton_clicked))
        
        ## connect particle attribute button
        def particleExpandButton_clicked():
            #if fluidList is set to expand, collapse it
            if self.fluidExpandState == 1:
                self.expand_button.setText('Show Fluid Attributes')
                self.listLayout.setFixedHeight(40)
                self.attributeListWidget.setVisible(0)
                self.fluidExpandState = 0
                
            if self.particleExpandState == 1:
                self.particle_expand_button.setText('Show Particle Attributes')
                self.particleListLayout.setFixedHeight(40)
                self.particleAttributeListWidget.setVisible(0)
                self.particleExpandState = 0
            else:
                self.particle_expand_button.setText('Hide Particle Attributes')
                self.particleAttributeListWidget.setVisible(1)
                self.particleListLayout.setFixedHeight(200)
                self.particleExpandState = 1
            
        self.particleExpandState = 0
        self.particle_expand_button.clicked.connect(partial(particleExpandButton_clicked))

        ## connect buttons
            ##
            ## node name buttons
        nodeField_main_button.clicked.connect(partial(self.getSelected, self.fluidCont_lineEdit, self.fluidEmit_lineEdit,
        self.partEmit_lineEdit, self.part_lineEdit, self.nucleus_lineEdit, False))

        self.trySettingsButton.clicked.connect(partial(self.productionCore, self.fluidCont_lineEdit, self.fluidEmit_lineEdit, 
        self.partEmit_lineEdit, self.part_lineEdit, self.nucleus_lineEdit))
        
#-----------------------------------------------------------------------------------------------------------#
        
    def create_applicationWidget(self):
        #add application widget
        self.applicationWidget = qg.QWidget()
        self.applicationWidget.setLayout(qg.QVBoxLayout())
        self.applicationWidget.setSizePolicy(qg.QSizePolicy.Maximum, qg.QSizePolicy.Maximum)
        self.applicationWidget.layout().setContentsMargins(5,5,5,5)
        self.applicationWidget.layout().setSpacing(2) 
        self.mainLayout.addWidget(self.applicationWidget)
        
        #empty line widget
        emptyLineLabel = qg.QLabel('')
        emptyLineLabel2 = qg.QLabel('')
        
        #return_button
            #
            #create layout + widgets
        return_layout = qg.QWidget()
        return_layout.setLayout(qg.QHBoxLayout())
        return_button = max.PushButton_custom('<---  Back', 'SansSerif')
        return_button.setSizePolicy(qg.QSizePolicy.Expanding, qg.QSizePolicy.Maximum)
        advanced_button = max.PushButton_custom('Advanced --->')
        advanced_button.setSizePolicy(qg.QSizePolicy.Expanding, qg.QSizePolicy.Maximum)

        return_layout.layout().addWidget(return_button)
        return_layout.layout().addWidget(advanced_button)

        Splitter = max.Splitter()
            #
            #add widgets to subLayout
        self.applicationWidget.layout().addWidget(return_layout)
        self.applicationWidget.layout().addWidget(Splitter)
        self.applicationWidget.layout().addStretch()

        # -- NODE FIELDS LAYOUTS --
            ##
            ## NODE FIELDS GETSELECTED LAYOUT
        nodeField_mainButton_layout = qg.QWidget()
        nodeField_mainButton_layout.setLayout(max.HBoxLayout())
        self.applicationWidget.layout().addWidget(nodeField_mainButton_layout)
            ##
            ## FLUID CONTAINER NODE LAYOUT
        fluidContainer_nodeLayout = qg.QWidget()
        fluidContainer_nodeLayout.setLayout(max.HBoxLayout())
        self.applicationWidget.layout().addWidget(fluidContainer_nodeLayout)
            ##
            ## FLUID EMITTER NODE LAYOUT
        fluidEmitter_nodeLayout = qg.QWidget()
        fluidEmitter_nodeLayout.setLayout(max.HBoxLayout())
        self.applicationWidget.layout().addWidget(fluidEmitter_nodeLayout)
            ##
            ## PARTICLE EMITTER NODE LAYOUT
        particleEmitter_nodeLayout = qg.QWidget()
        particleEmitter_nodeLayout.setLayout(max.HBoxLayout())
        splitter = max.Splitter()
        self.applicationWidget.layout().addWidget(splitter)
        self.applicationWidget.layout().addWidget(particleEmitter_nodeLayout)
            ##
            ## PARTICLE NODE LAYOUT
        particle_nodeLayout = qg.QWidget()
        particle_nodeLayout.setLayout(max.HBoxLayout())   
        self.applicationWidget.layout().addWidget(particle_nodeLayout) 
            ##
            ## NUCLEUS LAYOUT
        #emptyLine_4 = max.Label_custom()
        nucleus_nodeLayout = qg.QWidget()
        nucleus_nodeLayout.setLayout(max.HBoxLayout())
        self.applicationWidget.layout().addWidget(nucleus_nodeLayout)
        
        # -- NODE FIELD WIDGETS --
            ##
            ## MAIN BUTTON
        nodeField_main_button = max.PushButton_custom('Get Selected Objects', 'SansSerif', 12, self.cyan)
        nodeField_main_button.setMinimumWidth(240)
        nodeField_mainButton_layout.layout().addStretch()
        nodeField_mainButton_layout.layout().addWidget(nodeField_main_button)
            ##
            ## FLUID CONTAINER NODE
        fluidCont_label = max.Label_custom('Fluid Shape: ')
        self.fluidCont_lineEdit2 = max.LineEdit_custom()
        self.fluidCont_lineEdit2.setMinimumWidth(240)
        fluidContainer_nodeLayout.layout().addWidget(fluidCont_label)
        fluidContainer_nodeLayout.layout().addStretch()
        fluidContainer_nodeLayout.layout().addWidget(self.fluidCont_lineEdit2)
            ##
            ## FLUID EMITTER NODE
        fluidEmit_label = max.Label_custom('Fluid Emitter: ')
        self.fluidEmit_lineEdit2 = max.LineEdit_custom()
        self.fluidEmit_lineEdit2.setMinimumWidth(240)
        fluidEmitter_nodeLayout.layout().addWidget(fluidEmit_label)
        fluidEmitter_nodeLayout.layout().addStretch()
        fluidEmitter_nodeLayout.layout().addWidget(self.fluidEmit_lineEdit2)
            ##
            ## PARTICLE EMITTER NODE
        partEmit_label = max.Label_custom('nParticle Emitter: ')
        self.partEmit_lineEdit2 = max.LineEdit_custom()
        self.partEmit_lineEdit2.setMinimumWidth(240)
        particleEmitter_nodeLayout.layout().addWidget(partEmit_label)
        particleEmitter_nodeLayout.layout().addStretch()
        particleEmitter_nodeLayout.layout().addWidget(self.partEmit_lineEdit2)
            ##
            ## PARTICLE NODE
        part_label = max.Label_custom('nParticle Object: ')
        self.part_lineEdit2 = max.LineEdit_custom()
        self.part_lineEdit2.setMinimumWidth(240)
        particle_nodeLayout.layout().addWidget(part_label)
        particle_nodeLayout.layout().addStretch()
        particle_nodeLayout.layout().addWidget(self.part_lineEdit2)
            ##
            ## NUCLEUS NODE
        nucleus_label = max.Label_custom('Nucleus Object: ')
        self.nucleus_lineEdit2 = max.LineEdit_custom()
        self.nucleus_lineEdit2.setMinimumWidth(240)
        nucleus_nodeLayout.layout().addWidget(nucleus_label)
        nucleus_nodeLayout.layout().addStretch()
        nucleus_nodeLayout.layout().addWidget(self.nucleus_lineEdit2)
        
        #playblast layout
        self.playblastLayout = qg.QHBoxLayout()
        self.playblastLayout.setAlignment(qc.Qt.AlignHCenter)
        self.browse_playblast_Label = max.Label_custom('Playblast File:', 'SansSerif', 12)
        self.browse_playblast_Label.setAlignment(qc.Qt.AlignCenter)

        self.applicationWidget.layout().addStretch()
        self.applicationWidget.layout().addWidget(self.browse_playblast_Label)
        self.applicationWidget.layout().addLayout(self.playblastLayout) 
        
        #playblast widgets
        self.playblast_lineEdits_list = []
        self.playblast_browseLineEdit = max.LineEdit_custom('', 'SansSerif', 12)
        self.playblast_lineEdits_list.append(self.playblast_browseLineEdit)
        self.playblast_browseButton = max.PushButton_custom('Browse...', 'SansSerif', 12, self.purple)
        self.playblast_browseButton.setFixedWidth(100)
        self.playblastLayout.addWidget(self.playblast_browseLineEdit)
        self.playblastLayout.addWidget(self.playblast_browseButton)
        self.applicationWidget.layout().addWidget(emptyLineLabel)        
        
        #lowest buttons
        self.applySettingsButton = max.PushButton_custom('Apply Playblast Settings', 'SansSerif', 12, self.purple)
        self.applicationWidget.layout().addStretch()
        self.applicationWidget.layout().addWidget(self.applySettingsButton)

        def create_blendWidget(parentLayout, button_metaLayout):
            #check whether the main playblast lineEdit has been filled in
            if self.playblast_browseLineEdit.text() == '':
                max.errorPrompt('''
                    Please specify a main simulation with
                    which you want to blend another simulation
                    ''', '''Error''').show()
                self.mainLayout.setCurrentIndex(2)
                self.playblast_browseLineEdit.setPlaceholderText('>>ENTER MAIN SIMULATION HERE<<')
                return

            #create main frame layout
            blend_frame = qg.QFrame()
            blend_frame.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
            blend_frame.setSizePolicy(qg.QSizePolicy.Minimum, qg.QSizePolicy.Maximum)
            blend_frame.setMaximumHeight(100)
            blend_frame.setLayout(qg.QVBoxLayout())
            blend_frame.layout().setContentsMargins(2,2,2,2)
            blend_frame.layout().setSpacing(0)

            #playblast subLayout
            self.blend_playblastLayout = qg.QHBoxLayout()
            self.blend_playblastLayout.setAlignment(qc.Qt.AlignHCenter)

            #label subLayout
                ##
                ## layout + widget creation
            label_layout = qg.QWidget()
            label_layout.setLayout(qg.QHBoxLayout())
            label_layout.layout().setContentsMargins(2,2,2,2)
            label_layout.layout().setSpacing(0)
            blend_browse_playblast_Label = max.Label_custom('Blend Sim Playblast:', 'SansSerif', 12)
            close_button = max.PushButton_custom('X')
            close_button.setFixedWidth(30)
                ##
                ## add widgets to layout
            label_layout.layout().addStretch()
            label_layout.layout().addWidget(blend_browse_playblast_Label)
            label_layout.layout().addStretch()
            label_layout.layout().addWidget(close_button)

            #influence subLayout
                ##
                ## layout + widget creation
            influence_layout = qg.QWidget()
            influence_layout.setLayout(qg.QHBoxLayout())
            influence_layout.layout().setContentsMargins(2,2,2,2)
            influence_layout.layout().setSpacing(0)
            influence_label = max.Label_custom('Influence:')
            influence_slider = qg.QSlider()
            influence_slider.setOrientation(qc.Qt.Horizontal)
            influence_slider.setRange(0, 100)
            influence_spinbox = qg.QSpinBox()
            influence_spinbox.setFont(qg.QFont('SansSerif', 12))
            influence_spinbox.setRange(0, 100) 
                ##
                ## add widgets to layout
            influence_layout.layout().addWidget(influence_label)
            influence_layout.layout().addWidget(influence_slider)
            influence_layout.layout().addWidget(influence_spinbox)

            #add subLayouts to main frame layout
            blend_frame.layout().addStretch()
            blend_frame.layout().addWidget(label_layout)
            blend_frame.layout().addLayout(self.blend_playblastLayout)
            blend_frame.layout().addWidget(influence_layout)

            #playblast widgets
            blend_playblast_browseLineEdit = max.LineEdit_custom('', 'SansSerif', 12)
            self.blend_playblast_browseButton = max.PushButton_custom('Browse...', 'SansSerif', 12, self.purple)
            self.blend_playblast_browseButton.setFixedWidth(100)
            self.blend_playblastLayout.addWidget(blend_playblast_browseLineEdit)
            self.blend_playblastLayout.addWidget(self.blend_playblast_browseButton)

            #add lineEdit to lineEdit list
            self.playblast_lineEdits_list.append(blend_playblast_browseLineEdit)
            #add influence slider to influence list
            self.influenceList.append(influence_slider)

            #integrate frame widget in parent layout
                ##
                ## remove addBlend button and add frame widget to main layout
            parentLayout.removeWidget(button_metaLayout)
            parentLayout.addWidget(blend_frame)
                ##
                ## add addBlend button to main layout
            if len(self.influenceList) <= 2:
                parentLayout.addWidget(button_metaLayout)
            else:
                button_metaLayout.deleteLater()
                parentLayout.addStretch()

            #CONNECTIONS
                ##
                ## close button
            def remove_blend_frame(frame):
                parentLayout.removeWidget(frame)
                #add lineEdit to lineEdit list
                self.playblast_lineEdits_list.remove(blend_playblast_browseLineEdit)
                self.influenceList.remove(influence_slider)
                frame.deleteLater()
            close_button.clicked.connect(partial(remove_blend_frame, blend_frame))
                ##
                ## connect slider to spinbox
            influence_slider.valueChanged.connect(partial(influence_spinbox.setValue))
            influence_spinbox.valueChanged.connect(partial(influence_slider.setValue))
                ##
                ## connect browse button to browsing function
            self.blend_playblast_browseButton.clicked.connect(partial(self.browse_application_playblasts, 
                blend_playblast_browseLineEdit))

        def create_advancedApplication_widget():
            self.advancedApplication_widget = qg.QWidget()
            self.advancedApplication_widget.setLayout(qg.QVBoxLayout())
            self.advancedApplication_widget.setSizePolicy(qg.QSizePolicy.Maximum, qg.QSizePolicy.Maximum)
            self.advancedApplication_widget.layout().setContentsMargins(5,5,5,5)
            self.advancedApplication_widget.layout().setSpacing(0) 
            self.mainLayout.addWidget(self.advancedApplication_widget)

            # return_button
            advanced_return_layout = qg.QWidget()
            advanced_return_layout.setLayout(qg.QHBoxLayout())
            advanced_return_button = max.PushButton_custom('<---  Back', 'SansSerif')
            advanced_return_button.setSizePolicy(qg.QSizePolicy.Expanding, qg.QSizePolicy.Maximum)
            advanced_return_layout.layout().addWidget(advanced_return_button)
            advanced_return_layout.layout().addStretch()

            Splitter = max.Splitter()
            self.advancedApplication_widget.layout().addWidget(advanced_return_layout)
            self.advancedApplication_widget.layout().addWidget(Splitter)

            # add_blendSim button
            blendSim_layout = qg.QWidget()
            blendSim_layout.setLayout(qg.QHBoxLayout())
            addBlend_button = max.PushButton_custom('Blend with another Sim', 'SansSerif', 12, self.cyan) 
            addBlend_button.setMinimumWidth(180)
            blendSim_layout.layout().addStretch()
            blendSim_layout.layout().addWidget(addBlend_button)
            blendSim_layout.layout().addStretch()

            blendSim_metaLayout = qg.QWidget()
            blendSim_metaLayout.setLayout(qg.QVBoxLayout())
            blendSim_metaLayout.layout().addWidget(blendSim_layout)
            blendSim_metaLayout.layout().addStretch()

            self.advancedApplication_widget.layout().addWidget(blendSim_metaLayout)

            # CONNECTIONS
                ##
                ## advanced_return_button
            advanced_return_button.clicked.connect(partial(self.mainLayout.setCurrentIndex, 2))
                ##
                ## add blendFrame button
            addBlend_button.clicked.connect(partial(create_blendWidget, self.advancedApplication_widget.layout(), 
                blendSim_metaLayout))

        create_advancedApplication_widget()

        # CONNECTIONS
            #
            #connect button to stackedlayout index
        return_button.clicked.connect(partial(self.mainLayout.setCurrentIndex, 4))
        advanced_button.clicked.connect(partial(self.mainLayout.setCurrentIndex, 3))
            #
            # connect buttons        
        self.playblast_browseButton.clicked.connect(partial(self.browse_application_playblasts, 
            self.playblast_browseLineEdit))
        self.applySettingsButton.clicked.connect(partial(self.applicationCore_trigger,
            self.fluidCont_lineEdit2, self.fluidEmit_lineEdit2, self.partEmit_lineEdit2,
            self.part_lineEdit2, self.nucleus_lineEdit2, self.playblast_lineEdits_list, self.influenceList))
        nodeField_main_button.clicked.connect(partial(self.getSelected, self.fluidCont_lineEdit2, 
            self.fluidEmit_lineEdit2, self.partEmit_lineEdit2, self.part_lineEdit2, 
            self.nucleus_lineEdit2, True))
        
 #-----------------------------------------------------------------------------------------------------------#

    def create_homeWidget(self):
            ### LAYOUTS
        #add home widget to mainLayout
        homeWidget = qg.QWidget()
        homeWidget.setLayout(qg.QVBoxLayout())
        homeWidget.layout().setContentsMargins(5,5,5,5)
        homeWidget.layout().setSpacing(2) 
        self.mainLayout.addWidget(homeWidget)
        
        #create and add settings checkbox
        checkbox_layout = qg.QWidget()
        checkbox_layout.setLayout(qg.QHBoxLayout())
        checkbox_layout.setFixedHeight(40)
        homeWidget.layout().addWidget(checkbox_layout)
        settings_checkbox = max.CheckBox_custom('Use Default Output Folder', 'SansSerif', 12)
        settings_checkbox.setCheckState(qc.Qt.Checked)
        checkbox_layout.layout().addWidget(settings_checkbox)
        
        #create and add fileBrowsing layout
        browse_layout = qg.QWidget()
        browse_layout.setLayout(qg.QVBoxLayout())
        browse_layout.setFixedHeight(140)
        browse_layout.setVisible(0)
        homeWidget.layout().addWidget(browse_layout)
        
            ### WIDGETS
        #add browse widgets to browse layout
        whiteSpace1 = max.Label_custom('', 'SansSerif', 12)
        label = max.Label_custom('Output Directory: ', 'SansSerif', 12)
        label.setAlignment(qc.Qt.AlignCenter)
        self.outputFolder_lineEdit = max.LineEdit_custom(self.maya_rootDirectory, 'SansSerif', 12)
        browse_button = max.PushButton_custom('Browse...', 'SansSerif', 12)
        browse_button.setFixedWidth(90)
        browse_layout.layout().addWidget(label)
        browse_layout.layout().addWidget(self.outputFolder_lineEdit)
        browse_layout.layout().addWidget(browse_button)
        browse_layout.layout().addWidget(whiteSpace1)
        
        #node creation widgets
            ## 
            ## create node creation layout
        nParticle_layoutWidget = qg.QWidget()
        nParticle_layoutWidget.setLayout(qg.QHBoxLayout())
            ##
            ## create and add widgets
        self.createContainerAndEmitter_button = max.PushButton_custom('Fluid Emitter', 'SansSerif', 12, self.orange)
        self.createContainerAndEmitter_button.setFixedWidth(200)
        nParticleEmitter_button = max.PushButton_custom('nParticle Emitter', 'SansSerif', 12, self.cyan)
        nParticleEmitter_button.setFixedWidth(200)
        nParticle_layoutWidget.layout().addStretch(1)
        nParticle_layoutWidget.layout().addWidget(self.createContainerAndEmitter_button)
        nParticle_layoutWidget.layout().addWidget(nParticleEmitter_button)
        nParticle_layoutWidget.layout().addStretch(1)
            ##
            ## add to home layout
        homeWidget.layout().addWidget(nParticle_layoutWidget)
        homeWidget.layout().addWidget(nParticle_layoutWidget)
            ##
            ## add splitter
        splitter = max.Splitter()
        homeWidget.layout().addWidget(splitter)
        
        #create buttons and add them to the home widget
        trySettings_buttonLayout = qg.QWidget()
        trySettings_buttonLayout.setLayout(qg.QHBoxLayout())
        trySettings_button = max.PushButton_custom('Try Settings', 'SansSerif', 12, self.orange)
        trySettings_button.setFixedWidth(330)
        
        trySettings_buttonLayout.layout().addStretch()
        trySettings_buttonLayout.layout().addWidget(trySettings_button)
        trySettings_buttonLayout.layout().addStretch()
        
        autoSim_buttonLayout = qg.QWidget()
        autoSim_buttonLayout.setLayout(qg.QHBoxLayout())
        autoSim_button = max.PushButton_custom('Automatic Simulator', 'SansSerif', 12, self.cyan)
        autoSim_button.setFixedWidth(330)
        
        autoSim_buttonLayout.layout().addStretch()
        autoSim_buttonLayout.layout().addWidget(autoSim_button)
        autoSim_buttonLayout.layout().addStretch()
        
        applySettings_buttonLayout = qg.QWidget()
        applySettings_buttonLayout.setLayout(qg.QHBoxLayout())
        applySettings_button = max.PushButton_custom('Load Settings', 'SansSerif', 12, self.purple)
        applySettings_button.setFixedWidth(330)
        
        applySettings_buttonLayout.layout().addStretch()
        applySettings_buttonLayout.layout().addWidget(applySettings_button)
        applySettings_buttonLayout.layout().addStretch()
        
        whiteSpace4 = max.Label_custom('', 'SansSerif', 17)
        whiteSpace5 = max.Label_custom('', 'SansSerif', 17)
        whiteSpace6 = max.Label_custom('', 'SansSerif', 17)
        
        homeWidget.layout().addStretch()
        homeWidget.layout().addWidget(trySettings_buttonLayout)
        homeWidget.layout().addWidget(whiteSpace4)
        homeWidget.layout().addWidget(applySettings_buttonLayout)
        homeWidget.layout().addWidget(whiteSpace6)
        
        ### CONNECTIONS
            ## 
            ## connect node creation buttons 
        def get_createdNodes(lineEdit, inputText = ''):
            try:
                if inputText == '':
                    new_text = max.sel()[0]
                else:
                    new_text = inputText
                lineEdit.setText(new_text) 
            except IndexError:
                lineEdit.setText('')     
            
        def create_node(node):
            if node == 'fContain_plusEmit':
                node_returnArgs = max.createFluidContainer_inclEmitter()
                get_createdNodes(self.fluidCont_lineEdit, node_returnArgs[0])
                get_createdNodes(self.fluidEmit_lineEdit, node_returnArgs[1])
                
                get_createdNodes(self.fluidCont_lineEdit2, node_returnArgs[0])
                get_createdNodes(self.fluidEmit_lineEdit2, node_returnArgs[1])
            if node == 'pEmit':
                selection = mc.ls(sl=1)
                print(selection)
                if selection != []:
                    shape = mc.listRelatives(selection[0], shapes = True)[0]
                    if mc.objectType(shape, isType = 'fluidShape'):
                        node_returnArgs = max.create_nParticleEmitter()
                        
                        get_createdNodes(self.partEmit_lineEdit, node_returnArgs[0])
                        get_createdNodes(self.part_lineEdit, node_returnArgs[1])
                        get_createdNodes(self.fluidEmit_lineEdit, node_returnArgs[2])
                        get_createdNodes(self.fluidCont_lineEdit, node_returnArgs[3])
                        
                        get_createdNodes(self.partEmit_lineEdit2, node_returnArgs[0])
                        get_createdNodes(self.part_lineEdit2, node_returnArgs[1])
                        get_createdNodes(self.fluidEmit_lineEdit2, node_returnArgs[2])
                        get_createdNodes(self.fluidCont_lineEdit2, node_returnArgs[3])
                        
                        nucleus_node = mc.ls(type = 'nucleus')[0]
                        get_createdNodes(self.nucleus_lineEdit, nucleus_node)
                        
                        get_createdNodes(self.nucleus_lineEdit2, nucleus_node)

                        return
                max.errorPrompt('''
                Please select a Fluid Shape Object that you
                wish to connect to the particle emitter.
                ''', '''Can't make nParticle emitter''').show()

        self.createContainerAndEmitter_button.clicked.connect(partial(create_node,'fContain_plusEmit'))
        nParticleEmitter_button.clicked.connect(partial(create_node,'pEmit'))    
            
            ##
            ## connect buttons to subLayouts
        trySettings_button.clicked.connect(partial(self.mainLayout.setCurrentIndex, 0))
        applySettings_button.clicked.connect(partial(self.mainLayout.setCurrentIndex, 2))
        
            ##
            ## connect settings checkbox to settings visibility
        def make_visible(browse_layout, checkState):
            if checkState >= 1:
                checkState = 0
            else:
                checkState = 1
            browse_layout.setVisible(checkState)
        settings_checkbox.stateChanged.connect(partial(make_visible, browse_layout))
        
            ##
            ## connect browseButton to fileBrowsing function
        browse_button.clicked.connect(partial(self.rootDirectory_browsing))
        
            ##
            ## set stacked layout to homeWidget
        self.mainLayout.setCurrentIndex(4)        
        
#-----------------------------------------------------------------------------------------------------------# 
#-----------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------#      
    
    def import_core(self):
        runModulePath = 'G:\\HBO\\scripts\\autoSimulator\\CORE\\randomTries\\run_autoSim_v101.py'
        runModuleFileName = 'run_autoSim_v101'
        
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
        core = imp.load_source(runModuleFileName, runModulePath)
        del sys.modules[runModuleFileName]
        core = imp.load_source(runModuleFileName, runModulePath)
        
        return core

#-----------------------------------------------------------------------------------------------------------#

    def getSelected(self, fluidContainer_lineEdit, fluidEmitter_lineEdit, nPart_emitter_lineEdit, 
        nPart_part_lineEdit, nucleus_lineEdit, multiSelect):
        selection = mc.ls(sl = True)
        if not selection == []:
            fluidContainers = []
            fluidEmitters = []
            nPart_emitters = []
            nPart_parts = []
            for object in selection:
                objectType = mc.objectType(object)
                if objectType == 'transform':
                    shapeNodes = mc.listRelatives(object, shapes = True)
                    for shapeNode in shapeNodes:
                        objectType = mc.objectType(shapeNode)

                        if objectType == 'fluidShape':
                            fluidContainers.append(object) 
                        elif objectType == 'fluidEmitter':
                            fluidEmitters.append(object) 
                        elif objectType == 'pointEmitter':
                            nPart_emitters.append(object)   
                        elif objectType == 'nParticle':
                            nPart_parts.append(object)  

                        elif objectType == 'nucleus':
                            nucleus_lineEdit.setText(object)     
                else:
                    if objectType == 'fluidShape':
                        fluidContainers.append(object) 
                    elif objectType == 'fluidEmitter':
                        fluidEmitters.append(object) 
                    elif objectType == 'pointEmitter':
                        nPart_emitters.append(object)   
                    elif objectType == 'nParticle':
                        nPart_parts.append(object)  

                    elif objectType == 'nucleus':
                        nucleus_lineEdit.setText(object)      

            list_of_objectLists = [fluidContainers, fluidEmitters, nPart_emitters, nPart_parts]
            for object_list, line_edit in zip(list_of_objectLists, [fluidContainer_lineEdit, 
                fluidEmitter_lineEdit, nPart_emitter_lineEdit, nPart_part_lineEdit]):
                if not object_list == []:
                    object_list.sort()
                    if multiSelect:
                        lineEdit_text = ', '.join(object_list)
                    else:
                        lineEdit_text = object_list[0]
                    line_edit.setText(lineEdit_text)   
        else:
            fluidContainer_lineEdit.setText('') 
            fluidEmitter_lineEdit.setText('') 
            nPart_emitter_lineEdit.setText('') 
            nPart_part_lineEdit.setText('') 
            nucleus_lineEdit.setText('')                
 
#-----------------------------------------------------------------------------------------------------------#

    def create_nParticleEmitter(self):
        try:
            selection = max.sel()[0]
            shape = mc.listRelatives(selection, shapes = True)[0]
            
            #delete potentially existing fluid emitter
            children = mc.listRelatives(selection, children = True)
            for child in children:
                if mc.objectType(child, isType = 'fluidEmitter'):
                    mc.delete(child)
            
            #check if selected object is a fluid container
            if mc.objectType(shape, isType = 'fluidShape'):
                max.create_nParticleEmitter()
                mel.eval('fluidEmitter -type surface -der 1 -her 1 -fer 1 -fdr 2 -r 100.0 -cye none -cyi 1 -mxd 1 -mnd 0 ;')
                mc.select(shape, add = True)
                fluid_emitter = max.sel()[0]
                mel.eval(''.join(['connectDynamic -em ', fluid_emitter, ' ', shape, ';']))
            else:
                max.errorPrompt('''
                Please select a Fluid Container that you wish
                to connect to the nParticles.
                ''', '''Error''').show()
        except IndexError:
            max.errorPrompt('''
            Please select a Fluid Container that you wish
            to connect to the nParticles.
            ''', '''Error''').show()

#-----------------------------------------------------------------------------------------------------------#        

    def getAttributes(self):
        self.fluidEmitterAttrs = ['fluidDensityEmission','fluidHeatEmission','fluidFuelEmission','fluidDropoff',
        'inheritVelocity','normalSpeed','directionY','directionZ','directionalSpeed','directionX']
        
        self.fluidContainerAttrs = ['densityScale', 'densityBuoyancy', 'densityDissipation', 'densityDiffusion', 
        'densityPressure', 'densityPressureThreshold', 'densityTension', 'tensionForce', 'densityGradientForce', 
        'turbulenceStrength', 'turbulenceFrequency', 'temperatureScale', 'buoyancy', 'temperaturePressure', 
        'temperaturePressureThreshold', 'temperatureDissipation', 'temperatureDiffusion', 'temperatureTurbulence', 
        'temperatureTension', 'fuelScale', 'reactionSpeed', 'airFuelRatio', 'fuelIgnitionTemp', 'maxReactionTemp', 
        'heatReleased', 'gravity', 'viscosity', 'friction', 'velocityDamp', 'colorTexture', 'incandTexture', 
        'opacityTexture', 'textureType', 'coordinateMethod', 'coordinateSpeed', 'opacityTexGain', 'threshold', 
        'amplitude', 'ratio', 'frequencyRatio', 'depthMax', 'invertTexture', 'inflection', 'textureTime', 
        'zoomFactor', 'frequency', 'textureOriginX', 'textureOriginY', 'textureOriginZ', 'textureScaleZ', 
        'textureScaleY', 'textureScaleX', 'textureRotateX', 'textureRotateY', 'implode', 'textureRotateZ', 
        'implodeCenterX', 'implodeCenterY', 'implodeCenterZ', 'velocityScaleX', 'velocityScaleY', 'velocityScaleZ', 
        'velocitySwirl', 'velocityNoise', 'turbulenceSpeed', 'temperatureNoise', 'lightReleased']
        
        self.attributeList = sorted(self.fluidEmitterAttrs + self.fluidContainerAttrs)
        
    def getParticleAttributes(self):
        self.nPart_partAttrs = ['lifespan','radius','radiusScaleInputMax','dynamicsWeight','conserve','drag','damp','pointMass','massScaleInputMax',
        'massScaleRandomize','massScaleInput','pointForceField','pointFieldMagnitude','selfAttract','pointFieldDistance','pointFieldScaleInput',
        'pointFieldScaleInputMax','computeRotation','rotationFriction','rotationDamp','airPushDistance','airPushVorticity',
        'windShadowDistance','windShadowDiffusion']
        
        self.nPart_emitterAttrs = ['shearYZ','shearXZ','shearXY','emitterType','rate','scaleRateBySpeed',
        'scaleRateByObjectSize','cycleEmission','cycleInterval','minDistance','maxDistance','directionX','directionY','directionZ',
        'spread','speed','speedRandom','tangentSpeed','normalSpeed','volumeShape',
        'volumeOffsetX','volumeOffsetY','volumeSweep','sectionRadius',
        'volumeOffsetZ','awayFromCenter','awayFromAxis','alongAxis','aroundAxis','randomDirection',
        'directionalSpeed','scaleSpeedBySize']
        
        self.nPart_nucleusAttrs = ['gravity','airDensity','windSpeed','windDirectionX','windDirectionY','windNoise','windDirectionZ',
        'usePlane','planeOriginX','planeOriginY','planeOriginZ','planeNormalZ','planeNormalY','planeNormalX','planeBounce',
        'planeFriction','planeStickiness','timeScale','spaceScale']
        
        self.particleAttributeList = sorted(self.nPart_partAttrs + self.nPart_emitterAttrs + self.nPart_nucleusAttrs)
 
 #-----------------------------------------------------------------------------------------------------------#

    def rootDirectory_browsing(self):
        print('output folder browsing...')
        output_folder_dialog = qg.QFileDialog( parent = None, caption = 'Choose Output Folder', directory = self.maya_rootDirectory )
        self.output_folder = output_folder_dialog.getExistingDirectory()
        
        #correct output_folder path if necessary
        self.output_folder.replace('/','\\')
        if not self.output_folder[-1] == '\\':
            self.output_folder = ''.join([self.output_folder, '\\'])
        
        #update lineEdit        
        self.outputFolder_lineEdit.setText(str(self.output_folder))
        print('fileName', str(self.output_folder))
        
        #update directory names
        self.update_directories(self.output_folder)
 
 #-----------------------------------------------------------------------------------------------------------#

    def update_directories(self, root_directory):
        self.main_dir = ''.join([root_directory, 'simHelper Output'])
        ##
        ## TRIAL DIR
        self.trial_dir = '\\'.join([self.main_dir, 'randomTrials'])
        self.trial_playblasts_dir = '\\'.join([self.trial_dir, 'playblasts', ''])
        self.trial_settings_dir = '\\'.join([self.trial_dir, 'settings', ''])
        ## 
        ## AUTO-SIM DIR
        self.autoSim_dir = '\\'.join([self.main_dir, 'autoSim'])
        self.autoSim_longTerm_dir = '\\'.join([self.autoSim_dir, 'long-term']) 
        self.autoSim_longTerm_images_dir = '\\'.join([self.autoSim_longTerm_dir, 'images', ''])
        self.autoSim_longTerm_settings_dir = '\\'.join([self.autoSim_longTerm_dir, 'settings', ''])
        self.autoSim_images_dir = '\\'.join([self.autoSim_dir, 'images']) 
        self.autoSim_session_dir = '\\'.join([self.autoSim_dir, 'session'])
        self.autoSim_session_images_dir = '\\'.join([self.autoSim_session_dir, 'images', '']) 
        self.autoSim_session_settings_dir = '\\'.join([self.autoSim_session_dir, 'settings', '']) 
        ## 
        ## PRESETS DIR
        self.presets_dir = '\\'.join([self.main_dir, 'presets'])
        self.presets_images_dir = '\\'.join([self.presets_dir, 'images', ''])  
        self.presets_settings_dir = '\\'.join([self.presets_dir, 'settings', ''])  
        ##
        ## IMAGES DIR
        self.images_dir = '\\'.join([self.main_dir, 'images', ''])
        
        print('Directories updated.') 
  
#-----------------------------------------------------------------------------------------------------------#

    def productionCore(self, fluidCont_lineEdit, fluidEmit_lineEdit, partEmit_lineEdit, part_lineEdit, nucleus_lineEdit):
        #import core
        core = self.import_core()
        
        #get selected simcount
        allocatedTime = self.allocatedTime_spin.value()

        #get multi attr or single attr choice
        multiAttr = self.single_or_multiAttr_radioButton_multi.isChecked()
        print('multi attr selected?', str(multiAttr))
        
        #get selected fluid attributes
        userDefined_containerAttrs = []
        userDefined_emitterAttrs = []
        allSelectedAttributeObjects = self.attributeListWidget.selectedItems()
        for item in allSelectedAttributeObjects:
            item = item.text()
            if item in self.fluidEmitterAttrs:
                userDefined_emitterAttrs.append(item)
            else:
                userDefined_containerAttrs.append(item) 
                
        #get selected nParticle attributes
        userDefined_nPart_emitterAttrs = []
        userDefined_nPart_partAttrs = []
        userDefined_nPart_nucleusAttrs = []
        allSelected_nPart_AttributeObjects = self.particleAttributeListWidget.selectedItems()
        for item in allSelected_nPart_AttributeObjects:
            item = item.text()
            if item in self.nPart_emitterAttrs:
                userDefined_nPart_emitterAttrs.append(item)
            elif item in self.nPart_partAttrs:
                userDefined_nPart_partAttrs.append(item) 
            else:
                userDefined_nPart_nucleusAttrs.append(item) 
        
        playblastName = self.namingLineEdit.text()
        print('playblast name',playblastName)
        
        randomnessRange = self.randomPercentageSlider.value()
        print('randomnessRange: {}'.format(randomnessRange))
        
        playblast_mainFolder = self.trial_playblasts_dir
        playblast_subFolder = ''.join([playblast_mainFolder, playblastName, '\\'])
        print('playblast subfolder:', str(playblast_subFolder))
        settingFolder = self.trial_settings_dir
        
        #create new dirs if they do not exist already
        def makeNewDirs(inputFolder):
            if not os.path.exists(inputFolder):
                print('creating new folder:',inputFolder)
                os.makedirs(inputFolder)
        makeNewDirs(self.main_dir)
        makeNewDirs(settingFolder)
        makeNewDirs(playblast_mainFolder)
        makeNewDirs(playblast_subFolder)
        
        print('playblast folder',playblast_mainFolder)
        print('setting folder',settingFolder)
        
        #run production function in core module
        fluidCont_name = fluidCont_lineEdit.text()
        fluidEmit_name = fluidEmit_lineEdit.text()
        partEmit_name = partEmit_lineEdit.text()
        part_name = part_lineEdit.text()
        nucleus_name = nucleus_lineEdit.text()
        
        def nodes_are_specified():
            for node in [fluidCont_name, fluidEmit_name, partEmit_name, part_name, nucleus_name]:
                if node != '':
                    return True
            return False 
            
        if nodes_are_specified():
            core.produceSettings(userDefined_emitterAttrs, userDefined_containerAttrs, playblast_subFolder, playblastName, 
            randomnessRange, allocatedTime, settingFolder, fluidCont_name, fluidEmit_name, partEmit_name, part_name, 
            nucleus_name, userDefined_nPart_emitterAttrs, userDefined_nPart_partAttrs, userDefined_nPart_nucleusAttrs,
            multiAttr)
 
 #-----------------------------------------------------------------------------------------------------------#

    def browse_application_playblasts(self, line_edit):
        applyPlayblasts_dialog = qg.QFileDialog(parent = None, caption = 'Select Playblast File', 
            directory = self.trial_playblasts_dir, filter = "(*.mov)" )
        self.playblastPath = applyPlayblasts_dialog.getOpenFileName()[0]
        self.playblastPath = self.playblastPath.replace('/','\\')
        line_edit.setText(self.playblastPath)
 
 #-----------------------------------------------------------------------------------------------------------#

    def applicationCore_trigger(self, fluidCont_lineEdit, fluidEmit_lineEdit, partEmit_lineEdit, 
        part_lineEdit, nucleus_lineEdit, playblast_lineEdits_list, influence_sliders):
        #import core
        core = self.import_core()
        
        self.settingsPath = '\\'.join([self.trial_settings_dir, 'fluidTrials_settings.py'])
        self.settings_shortName = 'fluidTrials_settings.py'

        #create list of all playblastPaths
        self.playblastPaths = []
        for lineEdit in playblast_lineEdits_list:
            self.playblastPaths.append(lineEdit.text())
        
        #create list of all playblast influences
        influence_list = [100]
        for slider in influence_sliders:
            influence_list.append(slider.value())

        fluidContainer_node = fluidCont_lineEdit.text().split(', ')
        fluidEmitter_node = fluidEmit_lineEdit.text().split(', ')
        partEmitter_node = partEmit_lineEdit.text().split(', ')
        part_node = part_lineEdit.text().split(', ')
        nucleus_node = nucleus_lineEdit.text().split(', ')
        
        core.loadSettings(self.playblastPaths, self.settingsPath, self.settings_shortName, 
            fluidContainer_node, fluidEmitter_node, partEmitter_node, part_node, nucleus_node, influence_list)
        print('---- SETTINGS APPLIED SUCCESFULLY -----')

# ---------------------------------------------------------------------------------------------- #

#create dialog 
def create():
    global dialog
    if dialog is None:    
        dialog = simulationHelper_GUI('Simulation Helper')
    dialog.show()  

#delete dialog
def delete():
    global dialog
    if dialog is None:
        return
    dialog.deleteLater()
    dialog = None   






        
