import pyaudio
import sys
import logging
import time
import gc  # Import the garbage collection module

# Disable garbage collection at the start
gc.disable()

logging.basicConfig(level=logging.INFO)

# --- Configuration Section ---
# Set your desired input and output device names here
default_input_device_name = "Wave Link Monitor (Elgato Virtual Audio)" # "Wave Link Monitor (Wave Link Monitor)", if you can figure out how to enable KS to ASIO this could let an even lower Buffer Size
default_output_device_name = "Solid State Logic ASIO Driver"
# Set your host API name filter here
host_api_name_filter = "Windows WASAPI" # "Windows WDM-KS"
# --- End Configuration Section ---

def find_device_index(p, device_name, host_api_name_filter=None):
    """
    Finds the index of the audio device with the given name.
    Optionally filters devices by the host API name.
    
    :param p: PyAudio instance.
    :param device_name: Exact name of the device to search for.
    :param host_api_name_filter: Name of the host API to filter devices.
    :return: Index of the device or None if not found.
    """
    device_index = None
    exact_match = None  # Variable to hold the index of an exact match

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        host_api_info = p.get_host_api_info_by_index(device_info["hostApi"])

        # Check if the current device name exactly matches the desired device name
        if device_info["name"].lower().strip() == device_name.lower().strip():
            exact_match = i  # Store the exact match index
            if host_api_name_filter:
                # If a host API filter is set, ensure both the device name and host API name match
                if host_api_info["name"] == host_api_name_filter:
                    return exact_match
            else:
                return exact_match
    
    # In case no exact match was found, return None
    return exact_match


def calculate_buffer_size(p, device_index):
    """
    Calculates a preferred buffer size for the device at the given index.

    :param p: PyAudio instance.
    :param device_index: Index of the device.
    :return: Preferred buffer size calculated based on the device's default low output latency.
    """
    # Retrieve device information
    device_info = p.get_device_info_by_index(device_index)
    
    # Print the relevant device information
    #print(f"Device Name: {device_info['name']}")
    #print(f"Default Low Output Latency: {device_info['defaultLowOutputLatency']:.4f} seconds")
    #print(f"Default Sample Rate: {device_info['defaultSampleRate']} Hz")
    
    # Calculate buffer size
    buffer_size = int(device_info['defaultLowOutputLatency'] * device_info['defaultSampleRate'])
    
    # Print the calculated buffer size
    # print(f"Calculated Buffer Size: {buffer_size} frames")

    return buffer_size


def list_asio_devices(p):
    """
    Lists all ASIO devices available to the system.
    
    :param p: PyAudio instance.
    :return: List of tuples containing device indices and names.
    """
    asio_devices = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        host_api_info = p.get_host_api_info_by_index(device_info["hostApi"])
        if "ASIO" in host_api_info["name"]:
            asio_devices.append((i, device_info["name"]))
    return asio_devices

def restart_audio_stream(default_input_device_name, default_output_device_name, host_api_name_filter):
    """
    Optimized restart_audio_stream function for reduced latency.
    """
    attempt = 0
    max_attempts = 50

    while attempt < max_attempts:
        gc.enable()  # Enable garbage collection for this attempt
        try:
            p = pyaudio.PyAudio()
            # [Device index finding and error checking logic remains the same]

            loop_audio(p, input_device_index, output_device_index)
            break
        except IOError as e:
            logging.error(f"IOError on attempt #{attempt + 1}: {e}")
            attempt += 1
            time.sleep(1)
        finally:
            if 'p' in locals():
                p.terminate()
            gc.disable()

    if attempt == max_attempts:
        logging.error("Maximum attempts reached.")
        sys.exit(1)


def loop_audio(p, input_device_index, output_device_index):
    # Initial buffer size calculation
    buffer_size = calculate_buffer_size(p, output_device_index)
    settings = {
        "format": pyaudio.paInt16,
        "channels": 2,
        "rate": 48000,
        "frames_per_buffer": buffer_size
    }
    
    # Open the input and output streams
    input_stream = p.open(input=True, input_device_index=input_device_index, **settings)
    output_stream = p.open(output=True, output_device_index=output_device_index, **settings)
    logging.info(f"Looping audio with buffer size {buffer_size}. Press Ctrl+C to stop.")
    
    # Audio loop
    while True:
        data = input_stream.read(buffer_size, exception_on_overflow=False)
        output_stream.write(data)
    
if __name__ == "__main__":
    # Find device indices
    p = pyaudio.PyAudio()
    input_device_index = find_device_index(p, default_input_device_name, host_api_name_filter)
    output_device_index = find_device_index(p, default_output_device_name)

    if input_device_index is None or output_device_index is None:
        logging.error("Could not find the specified devices. Available ASIO devices are:")
        # List and print available ASIO devices
        asio_devices = list_asio_devices(p)
        for index, name in asio_devices:
            logging.info(f"Device Index: {index}, Device Name: {name}")
        p.terminate()  # Terminate the PyAudio instance
        sys.exit(1)  # Exit if devices are not found
    p.terminate()  # Terminate the initial PyAudio instance
    # Start or restart the audio stream as necessary
    restart_audio_stream(default_input_device_name, default_output_device_name, host_api_name_filter)