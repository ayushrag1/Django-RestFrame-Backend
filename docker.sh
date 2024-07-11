#!/bin/bash

# Extract the fourth segment of the current working directory's path and convert to lowercase
src_dir=$(echo $PWD | cut -f 6 -d /)
# Print the source directory
echo "Source directory: $src_dir"

# Remove any existing Docker image with the name $src_dir
docker rmi -f $src_dir

# Build a new Docker image from the Dockerfile in the current directory
docker build -f Dockerfile -t $src_dir .

# Remove any running Docker container with the name $src_dir
docker rm -f $src_dir

# Run a new Docker container with the name $src_dir and mount local directories
docker run -dit --name $src_dir \
  -p 8000:8000 \
  --mount src="$PWD/logs",target=/var/app/logs,type=bind \
  --mount src="$PWD/socket",target=/var/app/socket,type=bind \
  $src_dir
