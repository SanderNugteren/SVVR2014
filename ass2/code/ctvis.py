# Scientific Visualization and Virtual Reality Assignment 2
# November 17, 2014
# S. Nugteren (6042023) and M.L. de Groot (6103677) 

import vtk
import sys

#print 'Initial contour value:', sys.argv[1]

# SOURCE
#read in images from ct scanner (94 images, 256x256 pixels)
reader = vtk.vtkImageReader()
reader.SetFilePrefix("../data/slice")
reader.SetDataExtent(0, 255, 0, 255, 1, 94)
reader.SetDataOrigin(0.0, 0.0, 0.0)
reader.SetDataScalarTypeToUnsignedShort()
reader.SetDataByteOrderToBigEndian()
reader.SetDataSpacing(1,1,2) #data spacing

#update reader
reader.UpdateWholeExtent()
imageData = reader.GetOutput()

# FILTER
#get minimal and maximal values for isosurface (0 - 2^16)
minVal = imageData.GetScalarTypeMin() 
maxVal = imageData.GetScalarTypeMax() 

#make isosurface
conFilter = vtk.vtkContourFilter()
conFilter.SetInput(imageData)
conFilter.SetValue(0, float(sys.argv[1]))

#make contour filter
pdm = vtk.vtkPolyDataMapper()
pdm.SetInput(conFilter.GetOutput())
pdm.ScalarVisibilityOff() #option 6 
#pdm.SetScalarRange(minVal, maxVal) #option 7
#pdm.UseLookupTableScalarRangeOn() #option 7

# ACTOR
actor = vtk.vtkLODActor()
actor.SetNumberOfCloudPoints(1000)
actor.SetMapper(pdm)
actor.GetProperty().SetColor(1, 1, 1) #option 6

# RENDERER
ren = vtk.vtkRenderer()
#ren.SetBackground( 0.329412, 0.34902, 0.427451 ) #background colour
ren.AddActor(actor)
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

#start rendering
iren.Initialize()
renwin.Render()
iren.Start()