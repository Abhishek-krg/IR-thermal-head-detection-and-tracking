import PySpin
import matplotlib.pyplot as plt
import keyboard
import numpy as np


class IRFormatType:
    LINEAR_10MK = 1
    LINEAR_100MK = 2
    RADIOMETRIC = 3


CONTINUE_RECORDING = True
CHOSEN_IR_TYPE = IRFormatType.RADIOMETRIC


def handle_close(evt):
    """
    This function will close the GUI when close event happens.

    :param evt: Event that occurs when the figure closes.
    :type evt: Event
    """
    global CONTINUE_RECORDING
    CONTINUE_RECORDING = False


def acquire_and_display_images(cam, nodemap, nodemap_tldevice):
    """
    This function continuously acquires images from a device and display them in a GUI.

    :param cam: Camera to acquire images from.
    :param nodemap: Device nodemap.
    :param nodemap_tldevice: Transport layer device nodemap.
    :type cam: CameraPtr
    :type nodemap: INodeMap
    :type nodemap_tldevice: INodeMap
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    global CONTINUE_RECORDING

    sNodemap = cam.GetTLStreamNodeMap()

    # Change bufferhandling mode to NewestOnly
    node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))

    node_pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
    node_pixel_format_mono16 = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName('Mono16'))
    pixel_format_mono16 = node_pixel_format_mono16.GetValue()
    node_pixel_format.SetIntValue(pixel_format_mono16)

    if CHOSEN_IR_TYPE == IRFormatType.LINEAR_10MK:
        # This section is to be activated only to set the streaming mode to TemperatureLinear10mK
        node_IRFormat = PySpin.CEnumerationPtr(nodemap.GetNode('IRFormat'))
        node_temp_linear_high = PySpin.CEnumEntryPtr(node_IRFormat.GetEntryByName('TemperatureLinear10mK'))
        node_temp_high = node_temp_linear_high.GetValue()
        node_IRFormat.SetIntValue(node_temp_high)
    elif CHOSEN_IR_TYPE == IRFormatType.LINEAR_100MK:
        # This section is to be activated only to set the streaming mode to TemperatureLinear100mK
        node_IRFormat = PySpin.CEnumerationPtr(nodemap.GetNode('IRFormat'))
        node_temp_linear_low = PySpin.CEnumEntryPtr(node_IRFormat.GetEntryByName('TemperatureLinear100mK'))
        node_temp_low = node_temp_linear_low.GetValue()
        node_IRFormat.SetIntValue(node_temp_low)
    elif CHOSEN_IR_TYPE == IRFormatType.RADIOMETRIC:
        # This section is to be activated only to set the streaming mode to Radiometric
        node_IRFormat = PySpin.CEnumerationPtr(nodemap.GetNode('IRFormat'))
        node_temp_radiometric = PySpin.CEnumEntryPtr(node_IRFormat.GetEntryByName('Radiometric'))
        node_radiometric = node_temp_radiometric.GetValue()
        node_IRFormat.SetIntValue(node_radiometric)

    if not PySpin.IsAvailable(node_bufferhandling_mode) or not PySpin.IsWritable(node_bufferhandling_mode):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    # Retrieve entry node from enumeration node
    node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
    if not PySpin.IsAvailable(node_newestonly) or not PySpin.IsReadable(node_newestonly):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    # Retrieve integer value from entry node
    node_newestonly_mode = node_newestonly.GetValue()

    # Set integer value from entry node as new value of enumeration node
    node_bufferhandling_mode.SetIntValue(node_newestonly_mode)

    print('*** IMAGE ACQUISITION ***\n')
    try:
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
            return False

        # Retrieve entry node from enumeration node
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
            return False

        # Retrieve integer value from entry node
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

        # Set integer value from entry node as new value of enumeration node
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

        print('Acquisition mode set to continuous...')

        #  Begin acquiring images
        #
        #  *** NOTES ***
        #  What happens when the camera begins acquiring images depends on the
        #  acquisition mode. Single frame captures only a single image, multi
        #  frame catures a set number of images, and continuous captures a
        #  continuous stream of images.
        #
        #  *** LATER ***
        #  Image acquisition must be ended when no more images are needed.
        cam.BeginAcquisition()

        print('Acquiring images...')

        #  Retrieve device serial number for filename
        #
        #  *** NOTES ***
        #  The device serial number is retrieved in order to keep cameras from
        #  overwriting one another. Grabbing image IDs could also accomplish
        #  this.
        device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            print('Device serial number retrieved as %s...' % device_serial_number)

        # Retrieve Calibration details
        CalibrationQueryR_node = PySpin.CFloatPtr(nodemap.GetNode('R'))
        R = CalibrationQueryR_node.GetValue()
        print('R =', R)

        CalibrationQueryB_node = PySpin.CFloatPtr(nodemap.GetNode('B'))
        B = CalibrationQueryB_node.GetValue()
        print('B =', B)

        CalibrationQueryF_node = PySpin.CFloatPtr(nodemap.GetNode('F'))
        F = CalibrationQueryF_node.GetValue()
        print('F =', F)

        CalibrationQueryX_node = PySpin.CFloatPtr(nodemap.GetNode('X'))
        X = CalibrationQueryX_node.GetValue()
        print('X =', X)

        CalibrationQueryA1_node = PySpin.CFloatPtr(nodemap.GetNode('alpha1'))
        A1 = CalibrationQueryA1_node.GetValue()
        print('alpha1 =', A1)

        CalibrationQueryA2_node = PySpin.CFloatPtr(nodemap.GetNode('alpha2'))
        A2 = CalibrationQueryA2_node.GetValue()
        print('alpha2 =', A2)

        CalibrationQueryB1_node = PySpin.CFloatPtr(nodemap.GetNode('beta1'))
        B1 = CalibrationQueryB1_node.GetValue()
        print('beta1 =', B1)

        CalibrationQueryB2_node = PySpin.CFloatPtr(nodemap.GetNode('beta2'))
        B2 = CalibrationQueryB2_node.GetValue()
        print('beta2 =', B2)

        CalibrationQueryJ1_node = PySpin.CFloatPtr(nodemap.GetNode('J1'))    # Gain
        J1 = CalibrationQueryJ1_node.GetValue()
        print('Gain =', J1)

        CalibrationQueryJ0_node = PySpin.CIntegerPtr(nodemap.GetNode('J0'))   # Offset
        J0 = CalibrationQueryJ0_node.GetValue()
        print('Offset =', J0)

        # Figure(1) is default so you can omit this line. Figure(0) will create a new window every time program hits this line
        fig = plt.figure(1)

        # Close the GUI when close event happens
        fig.canvas.mpl_connect('close_event', handle_close)

        if CHOSEN_IR_TYPE == IRFormatType.RADIOMETRIC:
            # Object Parameters. For this demo, they are imposed!
            # This section is important when the streaming is set to radiometric and not TempLinear
            # Image of temperature is calculated computer-side and not camera-side
            # Parameters can be set to the whole image, or for a particular ROI (not done here)
            Emiss = 0.97
            TRefl = 293.15
            TAtm = 293.15
            TAtmC = TAtm - 273.15
            Humidity = 0.55

            Dist = 2
            ExtOpticsTransmission = 1
            ExtOpticsTemp = TAtm

            H2O = Humidity * np.exp(1.5587 + 0.06939 * TAtmC - 0.00027816 * TAtmC * TAtmC + 0.00000068455 * TAtmC * TAtmC * TAtmC)
            print('H20 =', H2O)

            Tau = X * np.exp(-np.sqrt(Dist) * (A1 + B1 * np.sqrt(H2O))) + (1 - X) * np.exp(-np.sqrt(Dist) * (A2 + B2 * np.sqrt(H2O)))
            print('tau =', Tau)

            # Pseudo radiance of the reflected environment
            r1 = ((1 - Emiss) / Emiss) * (R / (np.exp(B / TRefl) - F))
            print('r1 =', r1)

            # Pseudo radiance of the atmosphere
            r2 = ((1 - Tau) / (Emiss * Tau)) * (R / (np.exp(B / TAtm) - F))
            print('r2 =', r2)

            # Pseudo radiance of the external optics
            r3 = ((1 - ExtOpticsTransmission) / (Emiss * Tau * ExtOpticsTransmission)) * (R / (np.exp(B / ExtOpticsTemp) - F))
            print('r3 =', r3)

            K2 = r1 + r2 + r3
            print('K2 =', K2)

        # Retrieve and display images
        print('Press Enter to stop streaming')
        while(CONTINUE_RECORDING):
            try:

                #  Retrieve next received image
                #
                #  *** NOTES ***
                #  Capturing an image houses images on the camera buffer. Trying
                #  to capture an image that does not exist will hang the camera.
                #
                #  *** LATER ***
                #  Once an image from the buffer is saved and/or no longer
                #  needed, the image must be released in order to keep the
                #  buffer from filling up.

                image_result = cam.GetNextImage()

                #  Ensure image completion
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

                else:

                    # Getting the image data as a np array
                    image_data = image_result.GetNDArray()

                    # Draws an image (data, TemperatureLinear10mK, TemperatureLinear100mK, TemperatureRadiometric on the current figure.
                    # Select the desired output first

                    # Adapt the title to the correct streaming mode: TempLinear10mK, or TempLinear100mK or pseudo Radiance or Temperature Radiometric
                    fig.suptitle('A700 Temperature Radiometric')

                    if CHOSEN_IR_TYPE == IRFormatType.LINEAR_10MK:
                        # Transforming the data array into a temperature array, if streaming mode is set to TemperatueLinear10mK
                        image_Temp_Celsius_high = (image_data * 0.01) - 273.15
                        # Displaying an image of temperature when streaming mode is set to TemperatureLinear10mK
                        plt.imshow(image_Temp_Celsius_high, cmap='inferno', aspect='auto')
                        plt.colorbar(format='%.2f')

                    elif CHOSEN_IR_TYPE == IRFormatType.LINEAR_100MK:
                        # Transforming the data array into a temperature array, if streaming mode is set to TemperatureLinear100mK
                        image_Temp_Celsius_low = (image_data * 0.1) - 273.15
                        # Displaying an image of temperature when streaming mode is set to TemperatureLinear100mK
                        plt.imshow(image_Temp_Celsius_low, cmap='inferno', aspect='auto')
                        plt.colorbar(format='%.2f')

                    elif CHOSEN_IR_TYPE == IRFormatType.RADIOMETRIC:
                        # Transforming the data array into a pseudo radiance array, if streaming mode is set to Radiometric.
                        # and then calculating the temperature array (degrees Celsius) with the full thermography formula
                        image_Radiance = (image_data - J0) / J1
                        image_Temp = (B / np.log(R / ((image_Radiance / Emiss / Tau) - K2) + F)) - 273.15
                        # Displaying an image of temperature (degrees Celsius) when streaming mode is set to Radiometric
                        plt.imshow(image_Temp, cmap='inferno', aspect='auto')
                        plt.colorbar(format='%.2f')
                        '''
                        # Displaying an image of counts when streaming mode is set to Radiometric
                        plt.imshow(image_data, cmap='inferno', aspect='auto')
                        plt.colorbar(format='%.2f')
                        '''
                        '''
                        # Displaying an image of pseudo radiance when streaming mode is set to Radiometric
                        plt.imshow(image_Radiance, cmap='inferno', aspect='auto')
                        plt.colorbar(format='%.2f')
                        '''

                    # Interval in plt.pause(interval) determines how fast the images are displayed in a GUI
                    # Interval is in seconds.
                    plt.pause(0.001)

                    # Clear current reference of a figure. This will improve display speed significantly
                    plt.clf()

                    # If user presses enter, close the program
                    if keyboard.is_pressed('ENTER'):
                        print('Program is closing...')

                        # Close figure
                        plt.close('all')
                        CONTINUE_RECORDING = False

                #  Release image
                #
                #  *** NOTES ***
                #  Images retrieved directly from the camera (i.e. non-converted
                #  images) need to be released in order to keep from filling the
                #  buffer.
                image_result.Release()

            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False

        #  End acquisition
        #
        #  *** NOTES ***
        #  Ending acquisition appropriately helps ensure that devices clean up
        #  properly and do not need to be power-cycled to maintain integrity.
        cam.EndAcquisition()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return True


def run_single_camera(cam):
    """
    This function acts as the body of the example; please see NodeMapInfo example
    for more in-depth comments on setting up cameras.

    :param cam: Camera to run on.
    :type cam: CameraPtr
    :return: True if successful, False otherwise.
    :rtype: bool
    """
    try:
        result = True

        nodemap_tldevice = cam.GetTLDeviceNodeMap()

        # Initialize camera
        cam.Init()

        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()

        # Acquire images
        result &= acquire_and_display_images(cam, nodemap, nodemap_tldevice)

        # Deinitialize camera
        cam.DeInit()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result


def main():
    """
    Example entry point; please see Enumeration example for more in-depth
    comments on preparing and cleaning up the system.

    :return: True if successful, False otherwise.
    :rtype: bool
    """
    result = True

    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    # Get current library version
    version = system.GetLibraryVersion()
    print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    print('Number of cameras detected: %d' % num_cameras)

    # Finish if there are no cameras
    if num_cameras == 0:

        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system instance
        system.ReleaseInstance()

        print('Not enough cameras!')
        input('Done! Press Enter to exit...')
        return False

    # Run example on each camera
    for i, cam in enumerate(cam_list):

        print('Running example for camera %d...' % i)

        result &= run_single_camera(cam)
        print('Camera %d example complete... \n' % i)

    # Release reference to camera
    # NOTE: Unlike the C++ examples, we cannot rely on pointer objects being automatically
    # cleaned up when going out of scope.
    # The usage of del is preferred to assigning the variable to None.
    del cam

    # Clear camera list before releasing system
    cam_list.Clear()

    # Release system instance
    system.ReleaseInstance()

    input('Done! Press Enter to exit...')
    return result


if __name__ == '__main__':
    main()
