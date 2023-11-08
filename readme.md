![Logo](https://github.com/itslightmind/wavelinkToASIO/blob/main/images/banner.png?raw=true)

# WaveLinkToAsio

This utility significantly reduces latency in the Elgato WaveLink software, making it more effective for use with StreamDeck +

## API Reference

#### Start Script

```http
  python main.py "256"
```

Replace 256 with the current "Preferred ASIO Buffer Size" found in your Audio Interface's Control Panel.

The script default is to connect the Elgato WaveLink software to a SSL 2 interface. To use a different ASIO device, run main.py without an argument. This will prompt you to save the name of the ASIO device used. Depending on your setup, further adjustments may be necessary.

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

3. Use pip to install the downloaded file with the following command, replacing `PyAudio-0.2.11-cp38-cp38-win_amd64.whl` with the name of your downloaded file:

   ```sh
   python -m pip install PyAudio-0.2.11-cp38-cp38-win_amd64.whl --upgrade
   ```

## Roadmap

- Add support for finding other ASIO devices
- MAJOR, Add support for finding the prefered/currently set ASIO buffer size. since right now it has problems with connecting if another device is using the ASIO and the other program tries to set a diffrent buffer size.
