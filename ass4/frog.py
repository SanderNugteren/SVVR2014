# Scientific Visualization and Virtual Reality Assignment 4
# December 19, 2014
# S. Nugteren (6042023) and M.L. de Groot (6103677) 

import vtk
import sys

# SOURCE
def reader(filenames):
    reader = vtk.vtkImageReader2()
    reader.SetFilePrefix(filenames)
    reader.SetFilePattern("%s%03d.raw")
    reader.SetDataExtent(0, 499, 0, 469, 1, 136)
    reader.SetDataOrigin(1.0, 1.0, 1.0)
    reader.SetDataScalarTypeToUnsignedChar()
    reader.SetDataSpacing(1,1,1.5) #data spacing
    reader.UpdateWholeExtent()
    clip = vtk.vtkImageClip()
    clip.SetInputConnection( reader.GetOutputPort() )
    clip.SetOutputWholeExtent(0,499,0,235,1,136)
    clip.ClipDataOn()
    return clip.GetOutput()

imageData = reader("./WholeFrog/frogTissue.")
imageData2 = reader("./WholeFrog/frog.")

# LIBRARY
organList = ['', 'blood', 'brain', 'duodenum', 'eye retina', 'eye white', 'heart', 'ileum', 'kidney', 'large intestine', 'liver', 'lung', 'nerve', 'skeleton', 'spleen', 'stomach']

# setting the colour for each tissue
color = {}
#skeleton: white
color['skeleton'] = (1,1,1)     #white

#bloodflow: red
color['blood'] = (1,0,0.2)      #red
color['heart'] = (0.8,0,0)      #dark black

#nerve system: pink/purple
color['eye retina'] = (0.9,0.3,0.9) #pink
color['eye white'] = (1,0.7,1)  #light pink
color['nerve'] = (0.6,0,0.6)    #purple
color['brain'] = (0.7,0.1,1)    #dark purple

#respiratory system: blue
color['lung'] = (0,0.8,0.8)     #blue

#digestive tract: yellow
color['liver'] = (0.6,0.4,0.2)  #brown
color['kidney'] = (1,0.6,0.2)   #orange
color['duodenum'] = (0.9,0.9,0) #yellow
color['large intestine'] = (1,1,0.6) # light yellow
color['spleen'] = (0.3,0.5,0.3) #greenish
color['ileum'] = (0.6, 0.6, 0)  #greenish/brownish
color['stomach'] = (0.8,0.5,0.2) #brown

# ACTOR PER THRESHOLD FILTER
actorList = []

#make isosurface
conFilter = vtk.vtkContourFilter()
conFilter.SetInput(imageData2)
conFilter.SetValue(0, 50)
#make contour filter
pdm = vtk.vtkPolyDataMapper()
pdm.SetInput(conFilter.GetOutput())
pdm.ScalarVisibilityOff() 
# ACTOR
actor = vtk.vtkLODActor()
actor.SetMapper(pdm)
actor.GetProperty().SetColor(0, 0.8, 0) # green skin 
actor.GetProperty().SetOpacity(0.1) #lower is more opaque 
actorList.append(actor)

for i in xrange(1,len(organList)):
	#make isosurface
	thresholdFilter = vtk.vtkThreshold()
	thresholdFilter.SetInput(imageData)
	thresholdFilter.ThresholdBetween(i, i)

	# MAPPER
	#make contour filter
	dsm = vtk.vtkDataSetMapper()
	dsm.SetInput(thresholdFilter.GetOutput())
	dsm.ScalarVisibilityOff() 

	# ACTOR
	actor = vtk.vtkLODActor()
	actor.SetMapper(dsm)
	organCol = color[organList[i]]
	actor.GetProperty().SetColor(organCol)
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
