import pyaudio
import sys
import logging
import time
import argparse  # Import argparse for command-line arguments

logging.basicConfig(level=logging.INFO)

def find_device_index(p, device_name, host_api_name_filter=None):
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        host_api_info = p.get_host_api_info_by_index(device_info["hostApi"])
        
        if host_api_name_filter:
            if device_info["name"] == device_name and host_api_info["name"] == host_api_name_filter:
                return i
        else:
            if device_info["name"] == device_name:
                return i
    return None

def loop_audio(p, input_device_index, output_device_index, buffer_size):
    settings = {
        "format": pyaudio.paInt24,
        "channels": 2,
        "rate": 48000,
        "frames_per_buffer": buffer_size  # Set buffer size here
    }
    
    try:
        input_stream = p.open(input=True, input_device_index=input_device_index, **settings)
        output_stream = p.open(output=True, output_device_index=output_device_index, **settings)
        
        logging.info(f"Looping audio from microphone to ASIO with buffer size {buffer_size}. Press Ctrl+C to stop.")
        
        while True:
            data = input_stream.read(buffer_size, exception_on_overflow=True)
            output_stream.write(data)
            
        return 0  # Normal exit
            
    except KeyboardInterrupt:
        logging.info("Loopback stopped.")
        return 0  # Normal exit
    except IOError as e:
        logging.error(f"An error occurred with buffer size {buffer_size}: {e}")
        return 1  # Error exit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set buffer size for audio loop.')
    parser.add_argument('buffer_size', type=int, help='Buffer size for audio loop.')
    args = parser.parse_args()
    buffer_size = args.buffer_size  # Retrieve the buffer size from the command-line arguments

    while True:
        p = pyaudio.PyAudio()

        default_input_device_name = "Wave Link Monitor (Elgato Virtual Audio)"
        default_output_device_name = "Solid State Logic ASIO Driver"

        input_device_index = find_device_index(p, default_input_device_name, "Windows WASAPI")
        output_device_index = find_device_index(p, default_output_device_name)

        if input_device_index is None or output_device_index is None:
            logging.error("Could not find input or output device. Retrying in 1 second.")
            time.sleep(.05)
            continue
        
        exit_code = loop_audio(p, input_device_index, output_device_index, buffer_size)
        
        if exit_code == 0:
            break  # Normal exit, break the loop
        else:
            logging.error("An error occurred while looping audio. Retrying in 1 second.")
            time.sleep(0.05)
            continue  # Error occurred, retry
