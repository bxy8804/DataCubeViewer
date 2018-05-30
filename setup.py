#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 21:01:24 2018

@author: pjh523
"""

from setuptools import setup

setup(name='DataCubeViewer',
      version='0.2',
      description='An interactive GUI for viewing 3d data as slices in a stack.',
      author='Patrick Harrison',
      author_email='harriso.p.j@icloud.com',
      url='https://github.com/paddyh087/DataCubeViewer',
      license='MIT',
      
      install_requires=['PyQt5', 'numpy', 'matplotlib'],
      
      keywords='3D data visualization')