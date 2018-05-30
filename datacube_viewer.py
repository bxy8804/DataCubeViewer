#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 14:41:14 2018

@author: pjh523
"""

from .Generic_QtWindow import QtWindowCanvas, MPLCanvas

from PyQt5.QtWidgets import (QApplication, QSlider, QLabel, QGridLayout,
                             QComboBox, QWidget, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
import sys
from numpy import meshgrid, arange
from matplotlib import cm
#from numpy import rot90

class DataCubeViewer:
    '''GUI to show slices through multiple axes through a 3d data cube.

    Parameters
    ----------
    datacube : 3d numpy array
        The data over which to show slices.
    '''
    CUBE_PLANES = {'XY': 0,
                   'XZ': 1,
                   'YZ': 2}
    
    def __init__(self, datacube, axes_3d=True):
        
        assert len(datacube.shape) == 3, '3D data required.'
        
        self.app = QApplication(sys.argv)
        self.aw = QtWindowCanvas(bottom_dock=True, 
                                 left_dock=False, axes_3d=axes_3d)
        
        self._axes_3d = axes_3d
        
        self.datacube = datacube
        self.rotation_val = 0
        self.slider_val = 0

        self._label2d = '_data2d'
        self._label3d = '_data3d'
        # label for data in plot
        
        self._stride = 2
        
        # set axes limits to be data shape ± delta
        x, y, z = self.datacube.shape
        self.delta = 1
        self.aw.canvas.ax.set_xlim(-self.delta, z+self.delta)
        self.aw.canvas.ax.set_ylim(-self.delta, z+self.delta)
        self.aw.canvas.ax.set_zlim(-self.delta, z+self.delta)
        
        self.combobox_rotation = QComboBox()
        # 0, 1, and 2 are rotation axes
        self.combobox_rotation.addItems(self.CUBE_PLANES.keys())
        self.combobox_rotation.currentIndexChanged.connect(self.rotationChanged)
        self.combobox_rotation.setCurrentIndex(self.rotation_val)
        
        self.lineedit_stride = QLineEdit()
        self.lineedit_stride.setMaximumWidth(50)
        self.lineedit_stride.textEdited.connect(self.stride_changed)
        self.lineedit_stride.setValidator(QIntValidator())
        self.lineedit_stride.setText('2')
 
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
        
        self.grid_bdock.addWidget(QLabel('Stride: '), 0, 4)
        self.grid_bdock.addWidget(self.lineedit_stride, 0, 5)
        self.aw.bottom_dock.setWidget(self.bdock_widget)
        
        # plot first image
        self.rotationChanged()
        # make and plot a colorbar on MPL canvas
        #self.aw.canvas.fig.colorbar(MPLCanvas.get_image(self.aw.canvas.ax, \
        #                                                self.label))
        self.aw.show()
        self.app.exec_()
        
    def stride_changed(self, _number):
        '''
        Called when stride lineedit is changed.'''
        self._stride = int(_number)
        self.remove_slice()
        self.plot_slice()
    
    def remove_slice(self):
        '''
        Removes data from list of axes collections. Does not redraw figure.
        '''
        # get polycollection, ie. image, found in list
        coll = MPLCanvas.get_collection(self.aw.canvas.ax, self._label2d)
        # remove old collection from axes
        if coll:
            self.aw.canvas.ax.collections.remove(coll)
    
    def onSliderChange(self):
        '''Called when slider changes value.
        
        Updates the label and axes.'''
        self.slider_val = self.slider.value()
        self.slider_label.setText(str(self.slider_val))
        
        if self._axes_3d:
            self.remove_slice()
            # plot new slice
            self.plot_slice()
            
        else:
            self.aw.canvas.update_image(self.get_slice_from_datacube(),
                                        self._label2d)
        
    def get_3d_coordinates(self):
        sx, sy, sz = self.datacube.shape
        return meshgrid(arange(sx), arange(sy), arange(sz))
    
    def get_slice_coordinates(self, slice_index):
        '''Get coordinates for 3d plotting of a 2d slice of the datacube.
        Takes reference of the rotation axis and returns appropriate 
        coordinates.
        
        Parameters
        ----------
        slice_index: int
            The slice value, best obtained from slider.
        
        Returns
        -------
        x, y, z: 2d arrays of ints
            Pixel coordinate values for use in 3d plotting.
        '''
        if self.rotation_val == 0:
            s1, s2 = self.get_slice_from_datacube().shape
            coords1, coords2 = meshgrid(arange(s1), arange(s2))
            assert coords1.shape == coords2.shape
            coords3 = coords1.copy()
            coords3[:] = self.slider_val
        elif self.rotation_val == 1:
            s1, s3 = self.get_slice_from_datacube().shape
            coords1, coords3 = meshgrid(arange(s1), arange(s3))
            assert coords1.shape == coords3.shape
            coords2 = coords1.copy()
            coords2[:] = self.slider_val
        elif self.rotation_val == 2:
            s2, s3 = self.get_slice_from_datacube().shape
            coords2, coords3 = meshgrid(arange(s2), arange(s3))
            assert coords2.shape == coords3.shape
            coords1 = coords2.copy()
            coords1[:] = self.slider_val
        
        return coords1, coords2, coords3
    
    def get_slice_from_datacube(self):
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
    
    def plot_slice(self):
        '''
        Calculates parameters of slice position within cube and plots with
        colormap.
        
        Parameters
        ----------
        idle: boolean
            If True MPL will plot when idle.'''
        # get data and coordinates to plot
        x, y, z = self.get_slice_coordinates(self.slider_val)
        image = self.get_slice_from_datacube()
        # add data to offset slice value
        if self.rotation_val == 0:
            z = z.astype(float) + image
            fc = cm.viridis((z-z.min())/(z.max()-z.min()))
        elif self.rotation_val == 1:
            y = y.astype(float) + image
            fc = cm.viridis((y-y.min())/(y.max()-y.min()))
        elif self.rotation_val == 2:
            x = x.astype(float) + image
            fc = cm.viridis((x-x.min())/(x.max()-x.min()))
            
        #_roller = deque((x, y, z))
        #_roller.rotate(self.rotation_val)
        #_image = image[::self._spacing, ::self._spacing]
        # do plot, as surface such that position in cube is maintained
        self.aw.canvas.ax.plot_surface(x, y, z, 
                                       facecolors=fc,
                                       rstride=self._stride,
                                       cstride=self._stride,
                                       label=self._label2d)
        self.aw.canvas.draw()
        
    def rotationChanged(self):
        '''Called when the Axes combobox is changed.
        
        Replots the axes, sets the slider to 0'''
        self.rotation_val = self.CUBE_PLANES[self.combobox_rotation.currentText()]
        # print(self.rotation_val)
        # if rotation_val == 0, then depth is index = 2-0
        # etc. etc.
        # -1 for array indexing
        self.slider.setMaximum(self.datacube.shape[2-self.rotation_val]-1)
        self.slider.setValue(0)
        self.slider_val = self.slider.value()
        self.remove_slice()
        self.plot_slice()
