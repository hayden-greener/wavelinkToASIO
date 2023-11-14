![Logo](https://github.com/itslightmind/wavelinkToASIO/blob/main/images/banner.png?raw=true)

# WaveLinkToAsio

This utility significantly reduces latency in the Elgato WaveLink software, making it more effective for use with StreamDeck +

## API Reference

#### Start Script

```http
  python main.py
```

The script default is to connect the Elgato WaveLink software to a SSL 2 interface. To use a different ASIO device, When it doesnt find the SSL it will then list out other ASIO devices copy it over in to the main.py and you should be good.
Output

```http
D:\GitLocal\wavelinkToASIO>python main.py
ERROR:root:Could not find the specified devices. Available ASIO devices are:
INFO:root:Device Index: 34, Device Name: Solid State Logic ASIO Driver

D:\GitLocal\wavelinkToASIO>
```

then for the main.py you would set...

```http
  default_output_device_name = "Solid State Logic ASIO Driver"
```

## Acknowledgements

- [Christoph Gohlke](https://lfd.uci.edu), for the PyAudio ASIO wheel files
- [Elgato](https://www.elgato.com/us/en/s/downloads), Hopefully, this script will become obsolete as the software improves.

# PyAudio ASIO Installation Guide

Standard PyAudio lacks ASIO support. For wavelinkToAsio to function, you must either compile PyAudio with ASIO support yourself or download the appropriate .whl file.

## Prerequisites

- Python (matching the version of the PyAudio wheel file)
- pip (latest version)

## Installation

1. Download the appropriate PyAudio `.whl` file from Christoph Gohlke's [Pythonlibs repository](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio). Select the file that matches your Python version and system architecture.

2. Launch your command-line interface of choice.

3. Use pip to install the downloaded file with the following command, replacing `PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl` with the name of your downloaded file:

   ```sh
   python -m pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl
   ```

## Roadmap

- Add Kernal Streaming Support, right now its limited to windows WASAPI which is still fairly fast. But to get a zero overflow/underflow playback im having to play at 512 samples. I can do lower (even down to 64) but i hear maybe every few seconds underflow problems. Hope that KS would fix this since i've had good experinces in the past with KS latency.
