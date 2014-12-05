# Scientific Visualization and Virtual Reality Assignment 4
# December 19, 2014
# S. Nugteren (6042023) and M.L. de Groot (6103677) 

import vtk
import sys

# SOURCE
#read in images from ct scanner (94 images, 256x256 pixels)
reader = vtk.vtkImageReader2()
reader.SetFilePrefix("./WholeFrog/frogTissue.")
reader.SetFilePattern("%s%03d.raw")
reader.SetDataExtent(0, 499, 0, 469, 1, 136)
reader.SetDataOrigin(1.0, 1.0, 1.0)
reader.SetDataScalarTypeToUnsignedChar()
reader.SetDataSpacing(1,1,1.5) #data spacing

#update reader
reader.UpdateWholeExtent()
imageData = reader.GetOutput()

organList = ['', 'blood', 'brain', 'duodenum', 'eye retina', 'eye white', 'heart', 'ileum', 'kidney', 'large intestine', 'liver', 'lung', 'nerve', 'skeleton', 'spleen', 'stomach']

color = {}
color['blood'] = (1,0,0)
color['brain'] = (0,0,1)
color['duodenum'] = (0,1,0)
color['eye retina'] = (1,0,1)
color['eye white'] = (0.5,0,0.5)
color['heart'] = (0,0,0)
color['ileum'] = (0.45,0.3,0.2)
color['kidney'] = (1,0.5,0.3)
color['large intestine'] = (1,1,0)
color['liver'] = (0,1,1)
color['lung'] = (0,0.5,0)
color['nerve'] = (1,0.5,1)
color['skeleton'] = (1,1,1)
color['spleen'] = (0.3,0.5,0.3)
color['stomach'] = (0.2,0.2,0.7)

actorList = []

for i in xrange(1,15):
	#make isosurface
	thresholdFilter = vtk.vtkThreshold()
	thresholdFilter.SetInput(imageData)
	thresholdFilter.ThresholdBetween(i, i)

	# MAPPER
	#make contour filter
	dsm = vtk.vtkDataSetMapper ()
	dsm.SetInput(thresholdFilter.GetOutput())
	dsm.ScalarVisibilityOff() #color: option 6 
	#dsm.SetScalarRange(0, 3000) #color: option 7

	# ACTOR
	actor = vtk.vtkLODActor()
	actor.SetMapper(dsm)
	organCol = color[organList[i]]
	actor.GetProperty().SetColor(organCol) #color: option 6
	actorList.append(actor)

# RENDERER
ren = vtk.vtkRenderer()
ren.SetBackground( 0.329412, 0.34902, 0.427451 ) 

renderList = range(1,15)
for i in renderList:
	ren.AddActor(actorList[i-1])

legend = vtk.vtkLegendBoxActor()
legend.SetNumberOfEntries(len(renderList))
#legendBox = vtk.vtkCubeSource()
#legendBox.Update()
for i in renderList:
	legend.SetEntryString(i, organList[i])
	legend.SetEntryColor(i, color[organList[i]])

legend.GetPositionCoordinate().SetCoordinateSystemToView()
legend.GetPositionCoordinate().SetValue(.5, -0.99)
legend.GetPosition2Coordinate().SetCoordinateSystemToView()
legend.GetPosition2Coordinate().SetValue(0.99, -0.25)
	
ren.AddActor(legend)
	
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
