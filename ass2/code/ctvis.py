import vtk

#read in images from ct scanner
reader = vtk.vtkImageReader()
reader.SetFilePrefix("../data/slice")
reader.SetDataExtent(0, 255, 0, 255, 1, 94)
reader.SetDataOrigin(0.0, 0.0, 0.0)
reader.SetDataScalarTypeToUnsignedShort()
reader.SetDataByteOrderToBigEndian()
reader.UpdateWholeExtent()
imageData = reader.GetOutput()

#get minimal and maximal values for isosurface
minVal = imageData.GetScalarTypeMin()
maxVal = imageData.GetScalarTypeMax()

#make iso surface
conFilter = vtk.vtkContourFilter()
conFilter.SetInput(imageData)
conFilter.SetValue(0, (minVal+maxVal)/2)

#make contour filter
pdm = vtk.vtkPolyDataMapper()
pdm.SetInput(conFilter.GetOutput())

#make actor
actor = vtk.vtkLODActor()
actor.SetNumberOfCloudPoints(1000000)
actor.SetMapper(pdm)
actor.GetProperty().SetColor(1, 1, 1)

#initiate renderer
ren = vtk.vtkRenderer()
ren.SetBackground( 0.329412, 0.34902, 0.427451 )
ren.AddActor(actor)
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

#start rendering
iren.Initialize()
renwin.Render()
iren.Start()
