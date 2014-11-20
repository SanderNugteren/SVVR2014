# Scientific Visualization and Virtual Reality Assignment 3
# November 24, 2014
# S. Nugteren (6042023) and M.L. de Groot (6103677) 

import vtk
import sys

# SOURCE
#read in data
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName('SMRX.vtk')
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.UpdateWholeExtent()
imageData = reader.GetOutput()

# 3 FILTERS
#make isosurface of the scalars (ie mixer)
conFilter = vtk.vtkContourFilter()
conFilter.SetInput(imageData)
conFilter.SetValue(0, 10)

#make 'forward' vectorlines of the vectors (ie fluid1)
streamline = vtk.vtkStreamLine()
streamline.SetInputData(imageData)
streamline.SetMaximumPropagationTime(200)
streamline.SetIntegrationStepLength(.2)
streamline.SetStepLength(0.001)
streamline.SetNumberOfThreads(1)
streamline.SetIntegrationDirectionToForward()
streamline.VorticityOn()

#make 'backward' vectorlines of the vectors (ie fluid2)
streamFilter2 = vtk.vtkStreamTracer()
streamFilter2.SetInput(imageData)
streamFilter2.SetIntegrationDirectionToBackward()

"""
#make tubes around the streams for visibility
streamTube1 = vtk.vtkTubeFilter()
streamTube1.SetInputConnection(streamFilter1.GetOutput())
streamTube1.SetRadius(0.02)
streamTube1.SetNumberOfSides(12)

streamTube2 = vtk.vtkTubeFilter()
streamTube2.SetInputConnection(streamFilter2.GetOutput())
streamTube2.SetRadius(0.02)
streamTube2.SetNumberOfSides(12)
"""

# 3 MAPPERS
pdm1 = vtk.vtkPolyDataMapper()
pdm1.SetInput(conFilter.GetOutput())

pdm2 = vtk.vtkPolyDataMapper()
pdm2.SetInput(streamLine.GetOutput())

pdm3 = vtk.vtkPolyDataMapper()
pdm3.SetInput(streamFilter2.GetOutput())

# 3 ACTORS
actor1 = vtk.vtkLODActor()
actor1.SetMapper(pdm1)

actor2 = vtk.vtkLODActor()
actor2.SetMapper(pdm2)

actor3 = vtk.vtkLODActor()
actor3.SetMapper(pdm3)

# RENDERER
ren = vtk.vtkRenderer()
#ren.SetBackground( 0.329412, 0.34902, 0.427451 ) 
ren.AddActor(actor1)
ren.AddActor(actor2)
ren.AddActor(actor3)

#camera
#camera = vtk.vtkCamera()
#camera.SetPosition(128,1000,200)
#camera.SetFocalPoint(128,0,100)
#ren.SetActiveCamera(camera)

#renderwindow and render interactor
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)	
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

#initialize rendering
renwin.Render()
iren.Initialize()
iren.Start()
