## This whole script was written by  the free version of gemini  i just tested and suggested settings and features , it should work on windows(was tested on windows )  , linux, and macos ## 
## i cant code so i cant improve it or make it work with more file types or formats or make it better etc....##
## feel free to use or modify the script however you want ##

## Speed ##
example of 29 hour m4b file done in 51 seconds
 COMPRESSION REPORT 
Original File Size:   816.13 MB
Compressed File Size: 195.53 MB
Size Reduction:       76.0% smaller
Compression Ratio:    4.2:1
Total Processing Time:51.28 seconds


# FFmpeg MultiCPU Opus
**Note**: This project requires FFmpeg and python to be installed and accessible from the command line.

A Python script for multithreaded FFmpeg conversion of audio files to Opus format.

## Overview

This project provides an efficient way to convert audio files to the Opus codec using FFmpeg with multithreading support. By leveraging multiple CPU cores, it significantly speeds up the conversion process for large audio files.

## Features

- ✨ **Multithreaded Processing**: Utilizes multiple CPU cores for faster conversion
- 🎵 **Opus Codec Support**: High-quality audio compression with the modern Opus codec
- ⚡ **Performance Optimized**: Takes advantage of parallel processing for improved speed

## Requirements

- Python 3.6+ maybe, i dont know i use 3.12 might work with higher versions , might work with lower versions
- FFmpeg (with libopus support)

## Installation
1    Download fast_opus.py 
1.2  put dl file in same folder as the audio file you wish to convert
1.3  run fast_opus.py, it will ask what file you wish to convert if there are more files, and some settings 
1.4  set cpu cores as half of your logical cores for best performance the script uses 8 as default since i have a 8 core  16 thread cpu
     if you have a 6 core 12 threads set cpu cores as 6  , if you have 16 cores 32 threads set cores to 16 etc....
 
1. Install FFmpeg:
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

2. Install Python  make sure to add as path on windows

## Usage
1    Download fast_opus.py 
1.2  put dl file in same folder as the audio file you wish to convert
1.3  run fast_opus.py, it will ask what file you wish to convert if there are more files, and some settings 
1.4  set cpu cores as half of your logical cores for best performance the script uses 8 as default since i have a 8 core  16 thread cpu
     if you have a 6 core 12 threads set cpu cores as 6  , if you have 16 cores 32 threads set cores to 16 etc....


The multithreaded approach provides significant performance improvements:
- Parallel processing across multiple CPU cores
- Reduced overall conversion time for large files
- Optimized for systems with multiple processors

## Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests

## License

Please check the repository for license information.

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/vibesloper/ffmpegmulticpuopus/issues).

---

**Note**: This project requires FFmpeg and python to be installed and accessible from the command line.
