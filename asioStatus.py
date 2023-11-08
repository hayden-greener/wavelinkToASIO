import sounddevice as sd

def get_asio_device_settings(device_name):
    for device in sd.query_devices():
        if device['name'] == device_name:
            return device
    return None

if __name__ == "__main__":
    device_name = "Solid State Logic ASIO Driver"
    device_info = get_asio_device_settings(device_name)
    
    if device_info:
        print(f"Settings for {device_name}:")
        print(f"Sample Rate: {device_info['default_samplerate']} Hz")
        print(f"Max Input Channels: {device_info['max_input_channels']}")
        print(f"Max Output Channels: {device_info['max_output_channels']}")
        print(f"Default Low Input Latency: {device_info['default_low_input_latency']:.6f} sec")
        print(f"Default Low Output Latency: {device_info['default_low_output_latency']:.6f} sec")
        print(f"Default High Input Latency: {device_info['default_high_input_latency']:.6f} sec")
        print(f"Default High Output Latency: {device_info['default_high_output_latency']:.6f} sec")
    else:
        print(f"Could not find device named {device_name}.")

