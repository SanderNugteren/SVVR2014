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
reader.UpdateWholeExtent()
imageData = reader.GetOutput()

# LIBRARY
organList = ['', 'blood', 'brain', 'duodenum', 'eye retina', 'eye white', 'heart', 'ileum', 'kidney', 'large intestine', 'liver', 'lung', 'nerve', 'skeleton', 'spleen', 'stomach']

# setting the colour for each tissue
color = {}
color['blood'] = (1,0,0)        #red
color['skeleton'] = (1,1,1)     #white
color['eye retina'] = (0.9,0,0.9) #pink
color['eye white'] = (1,0,1) #light pink
color['nerve'] = (0.4,0,0.4)    #purple
color['brain'] = (0.7,0,0.7)        #dark purple

color['heart'] = (0,0,0)        #black
color['lung'] = (0,1,0)         #blue (dark)

color['liver'] = (0.45,0.3,0.2) #brown
color['kidney'] = (1,0.5,0.3)   #orange

color['duodenum'] = (0.3,0.3,0) #
color['ileum'] = (0.6, 0.6, 0)  #
color['large intestine'] = (1,1,0) #yellow

color['spleen'] = (0.3,0.5,0.3) #green
color['stomach'] = (0.2,0.2,0.7) #dark blue

# ACTOR PER THRESHOLD FILTER
actorList = []

for i in xrange(1,len(organList)):
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

renderList = range(1,len(organList))
for i in renderList:
	ren.AddActor(actorList[i-1])

# LEGEND
legend = vtk.vtkLegendBoxActor()
legend.SetNumberOfEntries(len(renderList))
#legendBox = vtk.vtkCubeSource()
#legendBox.Update()
for i in renderList:
    legend.SetEntryString(i-1, organList[i])
    legend.SetEntryColor(i-1, color[organList[i]])

legend.GetPositionCoordinate().SetCoordinateSystemToView()
legend.GetPositionCoordinate().SetValue(.5, -0.99)
legend.GetPosition2Coordinate().SetCoordinateSystemToView()
legend.GetPosition2Coordinate().SetValue(0.99, -0.25)
ren.AddActor(legend)
	
#renderwindow and render interactor
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)	
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

#initialize rendering
renwin.Render()
iren.Initialize()
iren.Start()
