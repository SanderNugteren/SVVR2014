# Scientific Visualization and Virtual Reality Assignment 4
# December 19, 2014
# S. Nugteren (6042023) and M.L. de Groot (6103677) 

import vtk
import sys

# SOURCE
#read in images from ct scanner (94 images, 256x256 pixels)
reader = vtk.vtkImageReader2()
reader.SetFilePrefix("./WholeFrog/frog.")
reader.SetFilePattern("%s%03d.raw")
reader.SetDataExtent(0, 499, 0, 469, 1, 136)
reader.SetDataOrigin(1.0, 1.0, 1.0)
reader.SetDataScalarTypeToUnsignedChar()
reader.SetDataSpacing(1,1,1.5) #data spacing
reader.UpdateWholeExtent()
imageData = reader.GetOutput()

minVal = imageData.GetScalarTypeMin() 
maxVal = imageData.GetScalarTypeMax() 
print(minVal)
print(maxVal)

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
actor.GetProperty().SetColor(0, 1, 0) 
actor.GetProperty().SetOpacity(0.1) #lower is more opaque 

# RENDERER
ren = vtk.vtkRenderer()
ren.SetBackground( 0.329412, 0.34902, 0.427451 ) 
ren.AddActor(actor)

#renderwindow and render interactor
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)	
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

#initialize rendering
renwin.Render()
iren.Initialize()
iren.Start()
