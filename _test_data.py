#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 13:07:06 2018

@author: pjh523
"""

import numpy as np

kernel_size = 30
kernel_iter = np.arange(-kernel_size/2, kernel_size/2)

# generate coordinates (3d)
x, y, z = np.meshgrid(kernel_iter, kernel_iter, kernel_iter)
# print(x.shape) # <--- NOTE 3D

def ricker_3d(x, y, z, sigma):
    '''General 3D Ricker function. NB. Not normalised.
    Maximum of returned kernel will always be 1.
    
    Parameters
    ----------
    x, y, z: 3D arrays
        Coordinates, best obtained by numpy.meshgrid.
    sigma: float
        Width of Ricker Wavelet.
    
    Returns
    -------
    Ricker Wavelet: 3D array'''
    return (1 - (1/2)*(x**2+y**2+z**2)/sigma**2)*np.exp(-(x**2+y**2+z**2)/(2*sigma**2))

# produce kernel
kernel = ricker_3d(x, y, z, 3)