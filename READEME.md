# Hand Tracking Computer Vision Project

This project uses MediaPipe and OpenCV to detect and track hand movements in real-time video feeds, with visualization of hand landmarks.

## Demo

![Hand Tracking Demo](demo.gif)
<!-- Add your GIF demonstration here -->

## Features

- Real-time hand detection and tracking
- Visualization of 21 hand landmarks
- Connection visualization between landmarks
- FPS (Frames Per Second) counter
- Support for IP webcam streaming

## Prerequisites

- Python 3.8+
- Webcam (local or IP camera)
- For IP cameras: A streaming setup (e.g., mjpeg-streamer)

## Setup and Installation

### Using Virtual Environment

1. Clone the repository:
```
git clone <your-repo-url>
cd Computer_Vision
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
   ```
   venv\Scripts\activate
   ```
   - On Linux/Mac:
   ```
   source venv/bin/activate
   ```

4. Install required packages:
```
pip install opencv-python mediapipe python-dotenv
```

### Using Conda (with environment.yml)

1. Clone the repository:
```
git clone <your-repo-url>
cd Computer_Vision
```

2. Create the environment from the environment.yml file:
```
conda env create -f environment.yml
```

3. Activate the environment:
```
conda activate hand-tracking-cv
```

## Configuration

If using an IP webcam:

1. Create a `.env` file in the project directory:
```
WEBCAM_IP=your-webcam-ip-address
```

2. Make sure your IP camera is streaming (e.g., using mjpeg-streamer) at the specified address and port.

## Usage

Run the script:
```
python hand_tracking.py
```

- Press 'q' to quit the application.

## Project Purpose

This project demonstrates computer vision capabilities for hand tracking, which has numerous applications:

- Gesture-based human-computer interaction
- Sign language recognition
- Touchless interfaces (particularly useful in healthcare settings)
- Virtual/Augmented reality controls

The implementation uses MediaPipe's hand tracking solution which provides 21 3D landmarks of a hand from video frames. This approach is lightweight and runs efficiently even on devices without dedicated GPU hardware.

## Technical Details

- MediaPipe's hand tracking model detects the hand and 21 hand landmarks
- OpenCV is used for webcam access and drawing the landmarks
- The system calculates and displays frames per second for performance monitoring
- WSL integration with IP webcam support for Windows-based camera access
