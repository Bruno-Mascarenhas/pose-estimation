# Follow Husky

## Overview

The **Follow Husky** project tracks and visualizes the movement of a red object (e.g., a husky) in video footage using OpenCV. It processes videos to detect and highlight the object, then saves the resulting video with marked paths and a summary image showing the object's movement.

## Features

- **Motion Detection**: Detects and tracks moving objects using background subtraction and color filtering.
- **Blob Tracking**: Identifies and tracks the largest red object in the frame.
- **Visualization**: Draws ellipses around detected objects and tracks their path over time.
- **Output**: Saves the processed video and a summary image with the detected path and object orientation.

## Installation

Ensure you have Python 3.x installed. Install the required packages using pip:

```bash
pip install opencv-python numpy
```

## Usage

Run the `main.py` script to process video files. Modify the script as needed for different input videos or output paths.

### Script Details

The script performs the following steps:

1. **Initialize Video Capture**: Opens the video file and prepares for processing.
2. **Motion Detection and Filtering**: Uses color filtering to detect red areas and applies background subtraction to isolate moving objects.
3. **Path Tracking**: Identifies the largest object, tracks its path, and draws ellipses and lines on the video frames.
4. **Save Results**: Outputs the processed video with annotated paths and a summary image showing the object's movement.

### Example

```python
import cv2 as cv
import numpy as np

def follow_husky(input, name, outpath):
    # Your code here

follow_husky('data/video1_husky.mp4', 'husky1', 'output/')
follow_husky('data/video2_husky.mp4', 'husky2', 'output/')
```

Replace `'data/video1_husky.mp4'` and `'data/video2_husky.mp4'` with paths to your video files, and `'output/'` with your desired output directory.

## Output

- **Video File**: Processed video saved as `name.avi` in the specified output path.
- **Summary Image**: An image showing the object's path and orientation saved as `name.png`.

## Debugging

Uncomment the following lines in `main.py` to view intermediate results:

```python
# cv.imshow('mask', frame)
# key = cv.waitKey(33)
# if key == 27:
#     break
```
---
