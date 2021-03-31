# ITK-SimpleITK-Converter
Converts SimpleITK image to ITK image and vice versa

Example of using:

itk_image = ConvertSimpleItkImageToItkImage(sitk_image, itk.F)

new_sitk_image: sitk.Image = ConvertItkImageToSimpleItkImage(itk_image, sitk.sitkFloat32, sitk_image.GetDirection())
