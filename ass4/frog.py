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

##################################################################################
# FILTER
#make isosurface
conFilter = vtk.vtkContourFilter()
conFilter.SetInput(imageData)
conFilter.SetValue(0, 50)

# MAPPER
#make contour filter
pdm = vtk.vtkPolyDataMapper()
pdm.SetInput(conFilter.GetOutput())
pdm.ScalarVisibilityOff() 

# ACTOR
actor = vtk.vtkLODActor()
actor.SetMapper(pdm)
actor.GetProperty().SetColor(0, 1, 0) #green skin
actor.GetProperty().SetOpacity(0.1) #lower is more opaque 

##################################################################################
# VOLUME MAPPER
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(imageData.GetProducerPort())

#TODO for nowI placed an empty string here, but later this should perhaps be replaced with the frog outline
volumeList = [""]

for i in xrange(1,len(organList)):
	#make a volume property for an organ, to be given to the volume
	volumeProperty = vtk.vtkVolumeProperty()
	volumeProperty.ShadeOff()
	volumeProperty.SetInterpolationTypeToLinear()
	#add opacity function to the volume property
	compositeOpacity = vtk.vtkPiecewiseFunction()
	compositeOpacity.AddPoint(0.0,0.0)
	compositeOpacity.AddPoint(i-0.2,0.0)
	compositeOpacity.AddPoint(i-0.1,1.0)
	compositeOpacity.AddPoint(i+0.1,1.0)
	compositeOpacity.AddPoint(i+0.2,0.0)
	compositeOpacity.AddPoint(len(organList),0.0)
	volumeProperty.SetScalarOpacity(compositeOpacity)
	#add a color function to the volume property
	volColor = vtk.vtkColorTransferFunction()
	organCol = color[organList[i]]
	volColor.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
	volColor.AddRGBPoint(i-0.2, 0.0, 0.0, 0.0)
	volColor.AddRGBPoint(i-0.1, organCol[0], organCol[1], organCol[2])
	volColor.AddRGBPoint(i+0.1, organCol[0], organCol[1], organCol[2])
	volColor.AddRGBPoint(i+0.2, 0.0, 0.0, 0.0)
	volColor.AddRGBPoint(len(organList)+1, 0.0, 0.0, 0.0)
	volumeProperty.SetColor(volColor)
	#make the volume itself
	volume = vtk.vtkVolume()
	volume.SetMapper(volumeMapper)
	volume.SetProperty(volumeProperty)
	volumeList.append(volume)
	
# RENDERER
ren = vtk.vtkRenderer()
ren.SetBackground( 0.329412, 0.34902, 0.427451 ) 
ren.AddActor(actor)

renderList = range(13,15)#(1,len(organList))
for i in renderList:
	ren.AddViewProp(volumeList[i])
	ren.ResetCamera()

# LEGEND
legend = vtk.vtkLegendBoxActor()
legend.SetNumberOfEntries(len(renderList))
#legendBox = vtk.vtkCubeSource()
#legendBox.Update()
for i in range(len(renderList)):
    legend.SetEntryString(i, organList[renderList[i]])
    legend.SetEntryColor(i, color[organList[renderList[i]]])

legend.GetPositionCoordinate().SetCoordinateSystemToView()
legend.GetPositionCoordinate().SetValue(.5, -0.99)
legend.GetPosition2Coordinate().SetCoordinateSystemToView()
legend.GetPosition2Coordinate().SetValue(0.99, -0.25)
ren.AddActor(legend)

#camera
camera = vtk.vtkCamera()
camera.SetPosition(128,1000,200)
camera.SetFocalPoint(128,0,100)
ren.SetActiveCamera(camera)
	
#renderwindow and render interactor
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)	
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

#initialize rendering
renwin.Render()
iren.Initialize()
iren.Start()
