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

## Roadmap and Performance Updates

### Kernel Streaming Support
- **Current**: Limited to Windows WASAPI (fairly fast).
- **Goal**: Add Kernel Streaming (KS) support for improved latency.
- **Note**: Experiencing underflow problems at lower sample sizes (16). Hoping KS implementation will resolve this.

### Frame Timing Information (Measured at 120fps externally)
- **Wavelink**: 21 frames, ~175 ms
- **512 off**: 17 frames, ~141.67 ms
- **512 on**: 13 frames, ~108.33 ms
- **32 off**: 13 frames, ~108.33 ms
- **32 on**: 7 frames, ~58.33 ms
- **Control**: 5 frames, ~41.67 ms
- **Enabling 'Safe Mode' unexpectedly boosts performance and reduces latency?**
- **Measured on Win11 with I7 13700k an interface SSL2 with v5.58.05 drivers**
