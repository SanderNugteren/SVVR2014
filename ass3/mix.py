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

#make a flat cylinder to act as a source for streamlines by making a line,...
lineSource1 = vtk.vtkLineSource()
lineSource1.SetPoint1(1, 30, 30)
lineSource1.SetPoint1(2, 0, 0)
transL1 = vtk.vtkTransform()
transL1.Translate(0, 30, 30)
tf1 = vtk.vtkTransformPolyDataFilter()
tf1.SetInputConnection(lineSource1.GetOutputPort())
tf1.SetTransform(transL1)
#then putting a tube around it
cylinder1 = vtk.vtkTubeFilter()
cylinder1.SetInputConnection(tf1.GetOutputPort())
cylinder1.SetRadius(15)
cylinder1.SetNumberOfSides(20)
cylinder1.CappingOn()

#make 'forward' vectorlines of the vectors (ie fluid1)
streamLine = vtk.vtkStreamLine()
streamLine.SetInput(imageData)
streamLine.SetSource(cylinder1.GetOutput())
streamLine.SetMaximumPropagationTime(2000)
streamLine.SetIntegrationStepLength(.2)
streamLine.SetStepLength(0.1)
streamLine.SetNumberOfThreads(100)
streamLine.SetIntegrationDirectionToForward()
streamLine.VorticityOn()
#streamLine.SetStartPosition(0, 25, 25)	

#make 'backward' vectorlines of the vectors (ie fluid2)
streamFilter2 = vtk.vtkStreamTracer()
streamFilter2.SetInput(imageData)
streamFilter2.SetIntegrationDirectionToBackward()

#make tubes around the streams for visibility
streamTube1 = vtk.vtkTubeFilter()
streamTube1.SetInput(streamLine.GetOutput())
streamTube1.SetRadius(0.5)
streamTube1.SetNumberOfSides(12)

"""
streamTube2 = vtk.vtkTubeFilter()
streamTube2.SetInputConnection(streamFilter2.GetOutput())
streamTube2.SetRadius(0.02)
streamTube2.SetNumberOfSides(12)
"""

# 3 MAPPERS
pdm1 = vtk.vtkPolyDataMapper()
pdm1.SetInput(conFilter.GetOutput())

pdm2 = vtk.vtkPolyDataMapper()
pdm2.SetInput(streamTube1.GetOutput())

pdm3 = vtk.vtkPolyDataMapper()
#pdm3.SetInput(streamFilter2.GetOutput())
pdm3.SetInput(cylinder1.GetOutput())


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
