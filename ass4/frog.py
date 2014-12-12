# Scientific Visualization and Virtual Reality Assignment 4
# December 19, 2014
# S. Nugteren (6042023) and M.L. de Groot (6103677) 

import vtk
import sys

# parameters
skin = False # Visualize the skin or the organs
clipToLeft = False
clipToRight = False
renderList = range(1,15) 
##################################################################################
# SOURCE
def reader(filenames):
    """
	This function reads in a dataset and clips it if the appropriate flags
	(clipToLeft, clipToRight) are set
    """
    reader = vtk.vtkImageReader2()
    reader.SetFilePrefix(filenames)
    reader.SetFilePattern("%s%03d.raw")
    reader.SetDataExtent(0, 499, 0, 469, 1, 136)
    reader.SetDataOrigin(1.0, 1.0, 1.0)
    reader.SetDataScalarTypeToUnsignedChar()
    reader.SetDataSpacing(1,1,1.5) #data spacing
    reader.UpdateWholeExtent()
    if clipToLeft:
        clip = vtk.vtkImageClip()
        clip.SetInputConnection( reader.GetOutputPort() )
        clip.SetOutputWholeExtent(0,499,0,235,1,136)
        clip.ClipDataOn()
        return clip.GetOutput()
    elif clipToRight:
        clip = vtk.vtkImageClip()
        clip.SetInputConnection( reader.GetOutputPort() )
        clip.SetOutputWholeExtent(0,499,235,469,1,136)
        clip.ClipDataOn()
        return clip.GetOutput()
    else:
        return reader.GetOutput()

imageData = reader("./WholeFrog/frogTissue.")
imageData2 = reader("./WholeFrog/frog.")

##################################################################################
# LIBRARY
organList = ['skin', 'blood', 'brain', 'duodenum', 'eye retina', 'eye white', 'heart', 'ileum', 'kidney', 'large intestine', 'liver', 'lung', 'nerve', 'skeleton', 'spleen', 'stomach']

# setting the colour for each tissue
color = {}
#skin: green
color['skin'] = (0,1,0)         #green 
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
# Using volume rendering
volumeList = []


# VOLUME MAPPER
volumeMapper = vtk.vtkSmartVolumeMapper() #vtkVolumeRayCastMapper()
volumeMapper.SetInputConnection(imageData.GetProducerPort())
#make a volume property the organs, to be given to the volume
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.ShadeOff()
volumeProperty.SetInterpolationTypeToLinear()
#add opacity function and color function to the volume property
compositeOpacity = vtk.vtkPiecewiseFunction()
volColor = vtk.vtkColorTransferFunction()
compositeOpacity.AddPoint(0.0, 0.0)
volColor.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
#generate peaks in the transfer functions for the organs to be rendered
for i in renderList:
    compositeOpacity.AddPoint(i-0.1,0.0)
    compositeOpacity.AddPoint(i,1.0)
    compositeOpacity.AddPoint(i+0.1,0.0)
    organCol = color[organList[i]]
    volColor.AddRGBPoint(i-0.1, 0.0, 0.0, 0.0)
    volColor.AddRGBPoint(i, organCol[0], organCol[1], organCol[2])
    volColor.AddRGBPoint(i+0.1, 0.0, 0.0, 0.0)
compositeOpacity.AddPoint(len(organList)+1, 0.0)
volumeProperty.SetScalarOpacity(compositeOpacity)
volColor.AddRGBPoint(len(organList)+1, 0.0, 0.0, 0.0)
volumeProperty.SetColor(volColor)

volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
	
##################################################################################	
# RENDERER
ren = vtk.vtkRenderer()
ren.SetBackground(0.329412, 0.34902, 0.427451) 
ren.AddViewProp(volume)

# Render the skin
if skin:
    # VOLUME MAPPER
    volumeMapper2 = vtk.vtkSmartVolumeMapper()
    volumeMapper2.SetInputConnection(imageData2.GetProducerPort())

    #make a volume property for an organ, to be given to the volume
    volumeProperty2 = vtk.vtkVolumeProperty()
    volumeProperty2.ShadeOff()
    volumeProperty2.SetInterpolationTypeToLinear()
    #add opacity function to the volume property
    compositeOpacity2 = vtk.vtkPiecewiseFunction()
    compositeOpacity2.AddPoint(0.0,0.0)
    compositeOpacity2.AddPoint(49,0.1)
    compositeOpacity2.AddPoint(50,0.1)
    compositeOpacity2.AddPoint(60,0.0)
    volumeProperty2.SetScalarOpacity(compositeOpacity2)
    #add a color function to the volume property
    volColor2 = vtk.vtkColorTransferFunction()
    volColor2.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
    volColor2.AddRGBPoint(40, 0.0, 1.0, 0.0)
    volColor2.AddRGBPoint(50, 0.0, 1.0, 0.0) # green skin
    volColor2.AddRGBPoint(60.1, 0.0, 1.0, 0.0)
    volColor2.AddRGBPoint(len(organList)+1, 0.0, 0.0, 0.0)
    volumeProperty2.SetColor(volColor2)
    #make the volume itself
    volume2 = vtk.vtkVolume()
    volume2.SetMapper(volumeMapper2)
    volume2.SetProperty(volumeProperty2)
    ren.AddViewProp(volume2)

ren.ResetCamera()

##################################################################################
# LEGEND
legend = vtk.vtkLegendBoxActor()
legend.SetNumberOfEntries(len(renderList))
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
camera.SetPosition(0,0,0)
	
#renderwindow and render interactor
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)	
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

#initialize rendering
renwin.Render()
iren.Initialize()
iren.Start()
