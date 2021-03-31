import SimpleITK as sitk
import numpy as np
import itk
from typing import List

def ConvertItkImageToSimpleItkImage(_itk_image: itk.Image, _pixel_id_value: int, _direction: List[float]) -> sitk.Image:
    """
    Converts ITK image to SimpleITK image

    :param _itk_image: ITK image
    :param _reference_image: Reference image from whiich will be copied the meta information
    :param _pixel_id_value: Type of the pixel in SimpleITK format (for example: sitk.sitkFloat32, sitk.sitkUInt8)
    :param _direction: The list of cosines which describes the study coordinate axis direction in the space
    :return: SimpleITK image
    """
    array: np.ndarray = itk.GetArrayFromImage(_itk_image)
    sitk_image: sitk.Image = sitk.GetImageFromArray(array)
    sitk_image = CopyImageMetaInformationFromItkImageToSimpleItkImage(sitk_image, _itk_image, _pixel_id_value, _direction)
    return sitk_image


def ConvertSimpleItkImageToItkImage(_sitk_image: sitk.Image, _pixel_id_value):
    """
    Converts SimpleITK image to ITK image

    :param _sitk_image: SimpleITK image
    :param _pixel_id_value: Type of the pixel in SimpleITK format (for example: itk.F, itk.UC)
    :return: ITK image
    """
    array: np.ndarray = sitk.GetArrayFromImage(_sitk_image)
    itk_image: itk.Image = itk.GetImageFromArray(array)
    itk_image = CopyImageMetaInformationFromSimpleItkImageToItkImage(itk_image, _sitk_image, _pixel_id_value)
    return itk_image
	
	
def CopyImageMetaInformationFromSimpleItkImageToItkImage(_itk_image: itk.Image, _reference_sitk_image: sitk.Image, _output_pixel_type) -> itk.Image:
    """
	Copies the meta information from SimpleITK image to ITK image

    :param _itk_image: Source ITK image
    :param _reference_sitk_image: Original SimpleITK image from which will be copied the meta information
    :param _pixel_type: Type of the pixel in SimpleITK format (for example: itk.F, itk.UC)
    :return: ITK image with the new meta information
    """
    _itk_image.SetOrigin(_reference_sitk_image.GetOrigin())
    _itk_image.SetSpacing(_reference_sitk_image.GetSpacing())

    # Setting the direction (cosines of the study coordinate axis direction in the space)
    reference_image_direction: np.ndarray = np.eye(3)
    np_dir_vnl = itk.GetVnlMatrixFromArray(reference_image_direction)
    itk_image_direction = _itk_image.GetDirection()
    itk_image_direction.GetVnlMatrix().copy_in(np_dir_vnl.data_block())

    dimension: int = _itk_image.GetImageDimension()
    input_image_type = type(_itk_image)
    output_image_type = itk.Image[_output_pixel_type, dimension]

    castImageFilter = itk.CastImageFilter[input_image_type, output_image_type].New()
    castImageFilter.SetInput(_itk_image)
    castImageFilter.Update()
    result_itk_image: itk.Image = castImageFilter.GetOutput()

    return result_itk_image


def CopyImageMetaInformationFromItkImageToSimpleItkImage(_sitk_image: sitk.Image, _reference_itk_image: itk.Image, _pixel_id_value: int, _direction: List[float]) -> itk.Image:
    """
	Copies the meta information from ITK image to SimpleITK image

    :param _sitk_image: Source SimpleITK image
    :param _reference_itk_image: Original ITK image from which will be copied the meta information
    :param _pixel_id_value: Type of the pixel in SimpleITK format (for example: sitk.sitkFloat32, sitk.sitkUInt8)
    :param _direction: The list of cosines which describes the study coordinate axis direction in the space
    :return: SimpleITK image with the new meta information
    """
    reference_image_origin: List[int] = list(_reference_itk_image.GetOrigin())
    _sitk_image.SetOrigin(reference_image_origin)
    reference_image_spacing: List[int] = list(_reference_itk_image.GetSpacing())
    _sitk_image.SetSpacing(reference_image_spacing)
    _sitk_image.SetDirection(_direction)
    result_sitk_image: sitk.Image = sitk.Cast(_sitk_image, _pixel_id_value)
    return result_sitk_image