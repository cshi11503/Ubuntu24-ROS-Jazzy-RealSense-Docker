# RealSense-ROS2-Docker-env

A Docker-based development environment for streaming RGB images from an **Intel RealSense D435** camera through **ROS 2 Jazzy** on **Ubuntu 24.04**, using **Python 3.12**.

This repository focuses on camera acquisition and ROS 2 image streaming. NVIDIA Isaac Sim is intentionally excluded from the initial setup.

## Goals

1. Connect the RealSense D435 to the host computer over USB.
2. Run the RealSense SDK and ROS 2 camera wrapper in a Docker container.
3. Publish live RGB images on a ROS 2 topic.
4. Subscribe to the images from Python for visualization and later VLM integration.

## Planned environment

| Component | Version / Technology |
| --- | --- |
| Host | Ubuntu 24.04 (Hyperion) |
| Container | Ubuntu 24.04 |
| ROS | ROS 2 Jazzy |
| Python | Python 3.12 |
| Camera | Intel RealSense D435 |
| Camera software | librealsense + realsense2_camera |

## Repository structure

```text
.
├── .env.example           # Local environment variable template
├── .gitignore             # Files excluded from version control
├── README.md              # Project documentation
├── docker/                # Dockerfile (to be added)
├── scripts/               # Camera test and utility scripts (planned)
└── ros2_ws/src/           # ROS 2 packages (planned)
```

## Setup (coming next)

Dockerfile, Docker Compose configuration, USB device access, and RealSense ROS 2 installation will be added next. This repository is **not yet runnable**.

Once configured, we will validate the stream using a command similar to:

```bash
ros2 topic hz /camera/camera/color/image_raw
```

The exact topic name will be confirmed with `ros2 topic list` after launching the camera wrapper.

## Development notes

- Docker must be granted access to the physical USB camera; installing packages alone is not sufficient.
- On shared lab computers, Docker permissions and device access must be checked with the administrator.
- Do not commit `.env`, recorded camera data, or credentials.
