# Adrian's Conversion Tool

## Overview
Adrian's Conversion Tool is a user-friendly desktop application for media conversion and downloading, built with Python and CustomTkinter. The project is modular, with each feature encapsulated in its own file within the `tabs/` directory.

## Features
- Modern, customisable interface using CustomTkinter
- Modular design for easy extension
- Media conversion and download capabilities
- About tab listing all dependencies and providing quick access to their documentation

## Project Structure
```
act.py                # Main entry point
tabs/                 # Feature modules (each as a separate tab)
	about.py          # About tab, lists dependencies
	caption.py        # Captioning functionality
	compress.py       # Compression tools
	convert.py        # Conversion tools
	settings.py       # Application settings
	ytd.py            # YT download functionality
```

## Dependencies
This application relies on the following dependencies:

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) – Modern UI framework for Tkinter
- [Pillow](https://pypi.org/project/pillow/) – Image processing library
- [FFmpeg](https://ffmpeg.org/) – Powerful multimedia framework (must be installed separately)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) – YouTube and media downloader
- [Python](https://python.org/) – Programming language (3.8+ recommended)
- [tkinter](https://docs.python.org/3/library/tkinter.html) – Standard Python GUI library

## Installation
1. Ensure you have Python 3.8 or newer installed.
2. Install required Python packages:
   ```shell
   pip install customtkinter pillow yt-dlp
   ```
3. Download and install [FFmpeg](https://ffmpeg.org/) and ensure it is in your system PATH.
4. In the same zip file that contains [FFmpeg](https://ffmpeg.org/) take the ffprobe and ensure it is also in the same PATH.

## Usage
Run the application with:
```shell
python act.py
```

## Extending the Application
To add a new feature:
1. Create a new Python file in the `tabs/` directory (e.g., `audio.py`).
2. Import and integrate it in `act.py` as a new tab.

---
*This project uses open-source libraries. See the About tab in the application for more details and quick links to documentation.*


