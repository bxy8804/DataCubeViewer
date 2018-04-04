#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 14:41:14 2018

@author: pjh523
"""

from .Generic_QtWindow import QtWindowCanvas

from PyQt5.QtWidgets import (QApplication, QSlider, QLabel, QGridLayout,
                             QComboBox, QWidget)
from PyQt5.QtCore import Qt
import sys

#from numpy import rot90

class DataCubeViewer:
    '''GUI to show slices through multiple axes through a 3d data cube.

    Parameters
    ----------
    datacube : 3d numpy array
        The data over which to show slices.
    '''
    
    def __init__(self, datacube):
        self.app = QApplication(sys.argv)
        self.aw = QtWindowCanvas(bottom_dock=True, left_dock=False)
        
        self.datacube = datacube
        self.rotation_val = 0
        self.slider_val = 0
        
        self.combobox_rotation = QComboBox()
        # 0, 1, and 2 are rotation axes
        self.combobox_rotation.addItems(('0', '1', '2'))
        self.combobox_rotation.setCurrentIndex(self.rotation_val)
        self.combobox_rotation.currentIndexChanged.connect(self.rotationChanged)
        
        self.aw.setWindowTitle('DataCube Viewer')
        
        # add slider and label to dock
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.onSliderChange)
        self.slider_label = QLabel(str(self.slider_val))
        
        self.bdock_widget = QWidget()
        self.grid_bdock = QGridLayout(self.bdock_widget)
        self.grid_bdock.addWidget(self.slider_label, 0, 0)
        self.grid_bdock.addWidget(self.slider, 0, 1)
        self.grid_bdock.addWidget(QLabel('Axes: '), 0, 2)
        self.grid_bdock.addWidget(self.combobox_rotation, 0, 3)
        self.aw.bottom_dock.setWidget(self.bdock_widget)
        
        # plot first image
        self.rotationChanged()
        # make and plot a colorbar on MPL canvas
        self.aw.canvas.fig.colorbar(self.aw.canvas.image)
        self.aw.canvas.update()
        self.slider_label.setText(str(self.slider_val))
        
        self.aw.show()
        self.app.exec_()
        
    def onSliderChange(self):
        '''Called when slider changes value.
        
        Updates the label and axes.'''
        self.slider_val = self.slider.value()
        self.slider_label.setText(str(self.slider_val))
        self.aw.canvas.update_image(self.get_array_from_datacube())
        
    def get_array_from_datacube(self):
        '''Selects the correct slice through the data cube to show
        according to slider value and axes value.'''
        if self.rotation_val == 0:
            data_array = self.datacube[:,:,self.slider_val]
        elif self.rotation_val == 1:
            # data_array = rot90(self.datacube, axes=(0,2))[:,:,self.slider_val]
            data_array = self.datacube[:,self.slider_val,:]
        elif self.rotation_val == 2:
            # data_array = rot90(self.datacube, axes=(1,2))[:,:,self.slider_val]
            data_array = self.datacube[self.slider_val,:,:]
        
        return data_array
    
    def rotationChanged(self):
        '''Called when the Axes combobox is changed.
        
        Replots the axes, sets the slider to 0'''
        self.rotation_val = int(self.combobox_rotation.currentText())
        # print(self.rotation_val)
        # if rotation_val == 0, then depth is index = 2-0
        # etc. etc.
        # -1 for array indexing
        self.slider.setMaximum(self.datacube.shape[2-self.rotation_val]-1)
        self.slider.setValue(0)
        self.slider_val = self.slider.value()
        self.aw.canvas.plot_image(self.get_array_from_datacube())
        self.aw.canvas.update()
