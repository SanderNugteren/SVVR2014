# Scientific Visualization and Virtual Reality Assignment 3
# November 24, 2014
# S. Nugteren (6042023) and M.L. de Groot (6103677) 

import vtk
import sys

def makeStreamActors(center, color):
	"""
	This function produces streamlines for a stream centered at 'center' and returns an actor 
    for use in rendering. Stream color can be specified using the 'color' variable.
	"""
	#make a source to generate stream lines from
	lineSource = vtk.vtkPointSource()
	lineSource.SetRadius(15)
	lineSource.SetCenter(center)
	lineSource.SetNumberOfPoints(200)

	#make streamlines using the source created above
	streamLine = vtk.vtkStreamLine()
	streamLine.SetInput(imageData)
	streamLine.SetSource(lineSource.GetOutput())
	streamLine.SetMaximumPropagationTime(2000)
	streamLine.SetIntegrationStepLength(.2)
	streamLine.SetStepLength(0.1)
	streamLine.SetNumberOfThreads(100)
	streamLine.SetIntegrationDirectionToIntegrateBothDirections	()
	streamLine.VorticityOn()

	#make tubes around the streamlines for visibility
	streamTube = vtk.vtkTubeFilter()
	streamTube.SetInput(streamLine.GetOutput())
	streamTube.SetRadius(0.1)
	streamTube.SetNumberOfSides(12)
	
	pdm = vtk.vtkPolyDataMapper()
	pdm.SetInput(streamTube.GetOutput())
	pdm.ScalarVisibilityOff()
	
	actor = vtk.vtkActor()
	actor.SetMapper(pdm)
	actor.GetProperty().SetColor(color)
	return actor

# SOURCE
#read in data
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName('SMRX.vtk')
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.UpdateWholeExtent()
imageData = reader.GetOutput()

#make isosurface of the scalars (ie mixer)
conFilter = vtk.vtkContourFilter()
conFilter.SetInput(imageData)
conFilter.SetValue(0, 10)

# Map the mixer
pdm1 = vtk.vtkPolyDataMapper()
pdm1.SetInput(conFilter.GetOutput())

# Create an actor for the mixer
mixerActor = vtk.vtkLODActor()
mixerActor.SetMapper(pdm1)

#create actors for both streams
fluid1Actor = makeStreamActors((20,15,30), (1.0, 0.0, 0.0))
fluid2Actor = makeStreamActors((20,45,30), (0.0, 1.0, 0.0))

#coordinates for the stream around the reactor
#fluid1Actor = makeStreamActors((20,0,30), (1.0, 0.0, 0.0))
#fluid2Actor = makeStreamActors((20,60,30), (0.0, 1.0, 0.0))


# RENDERER
ren = vtk.vtkRenderer()
#ren.SetBackground( 0.329412, 0.34902, 0.427451 )
ren.AddActor(mixerActor)
ren.AddActor(fluid1Actor)
ren.AddActor(fluid2Actor)

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
