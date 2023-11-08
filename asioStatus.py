import pyaudio

def get_asio_device_settings(device_name):
    """
    Prints the settings for the specified ASIO device.
    
    :param device_name: The name of the ASIO device to retrieve settings for.
    """
    p = pyaudio.PyAudio()
    
    try:
        # Find the device by name
        device_index = None
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            if dev_info.get('name') == device_name:
                device_index = i
                break
        
        if device_index is None:
            print(f"Device named '{device_name}' not found.")
            return
        
        # Get device info
        device_info = p.get_device_info_by_index(device_index)
        
        # Print device info
        print(f"Settings for '{device_name}':")
        print(f"  Index: {device_index}")
        print(f"  Default Sample Rate: {device_info['defaultSampleRate']}")

        # Print additional settings including current sample rate and calculated preferred buffer size
        current_sample_rate = device_info['defaultSampleRate']
        print(f"  Current Sample Rate: {current_sample_rate}")

        # Calculate the preferred buffer size based on default low output latency
        preferred_buffer_size = int(device_info['defaultLowOutputLatency'] * current_sample_rate)
        print(f"  Preferred ASIO Buffer Size: {preferred_buffer_size}")
        
    finally:
        p.terminate()

if __name__ == "__main__":
    asio_device_name = "Solid State Logic ASIO Driver"
    get_asio_device_settings(asio_device_name)
