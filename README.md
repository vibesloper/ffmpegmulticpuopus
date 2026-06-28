# FFmpeg MultiCPU Opus

A Python script for multithreaded FFmpeg conversion of audio files to Opus format.

## Overview

This project provides an efficient way to convert audio files to the Opus codec using FFmpeg with multithreading support. By leveraging multiple CPU cores, it significantly speeds up the conversion process for large audio files or batch operations.

## Features

- ✨ **Multithreaded Processing**: Utilizes multiple CPU cores for faster conversion
- 🎵 **Opus Codec Support**: High-quality audio compression with the modern Opus codec
- 🔄 **Batch Conversion**: Process multiple files efficiently
- ⚡ **Performance Optimized**: Takes advantage of parallel processing for improved speed
- 🛠️ **FFmpeg Integration**: Built on the powerful FFmpeg library

## Requirements

- Python 3.6+
- FFmpeg (with libopus support)
- ffmpeg-python (or similar FFmpeg Python bindings)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vibesloper/ffmpegmulticpuopus.git
cd ffmpegmulticpuopus
```

2. Install FFmpeg:
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

3. Install Python dependencies (if applicable):
```bash
pip install -r requirements.txt
```

## Usage

```bash
python ffmpegmulticpuopus.py [input_file] [output_file]
```

### Example

```bash
python ffmpegmulticpuopus.py input_audio.mp3 output_audio.opus
```

## Performance

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

**Note**: This project requires FFmpeg to be installed and accessible from the command line.
