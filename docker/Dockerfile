
# Ubuntu 24.04 with ROS 2 Jazzy
ARG ROS_DISTRO=jazzy
FROM ros:${ROS_DISTRO}-ros-base-noble

ARG ROS_DISTRO=jazzy

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=${ROS_DISTRO}
ENV ROS_WS=/workspace

# Install RealSense ROS wrapper and image-processing tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-${ROS_DISTRO}-realsense2-camera \
    ros-${ROS_DISTRO}-realsense2-description \
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-image-transport \
    ros-${ROS_DISTRO}-rqt-image-view \
    python3-opencv \
    python3-numpy \
    python3-pip \
    usbutils \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /workspace

# Automatically source ROS 2 when opening Bash
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc

# Start an interactive Bash shell by default
CMD ["/bin/bash"]
