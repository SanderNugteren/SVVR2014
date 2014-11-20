# Scientific Visualization and Virtual Reality Assignment 3
# November 17, 2014
# S. Nugteren (6042023) and M.L. de Groot (6103677) 

import vtk
import sys

# SOURCE
#read in data
reader = vtk.vtkImageReader2()


#update reader
reader.UpdateWholeExtent()
imageData = reader.GetOutput()

# FILTER
#get minimal and maximal values for isosurface
#minVal = imageData.GetScalarTypeMin() 
#maxVal = imageData.GetScalarTypeMax() 

#make isosurface
conFilter = vtk.vtkContourFilter()
conFilter.SetInput(imageData)
#conFilter.SetValue(0, float(sys.argv[1]))
conFilter.SetValue(0, 700)
conFilter.SetValue(1, 3000)

# MAPPER
#make contour filter
pdm = vtk.vtkPolyDataMapper()
pdm.SetInput(conFilter.GetOutput())
#pdm.ScalarVisibilityOff() #color: option 6 
pdm.SetScalarRange(0, 3000) #color: option 7

# ACTOR
actor = vtk.vtkLODActor()
actor.SetMapper(pdm)
#actor.GetProperty().SetColor(1, 1, 1) #color: option 6

# RENDERER
ren = vtk.vtkRenderer()
#ren.SetBackground( 0.329412, 0.34902, 0.427451 ) 
ren.AddActor(actor)

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
