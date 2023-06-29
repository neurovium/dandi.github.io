#!/bin/bash

# Directory path
directory="assets/team/"

# Loop through image files in the directory
for file in "$directory"*.{jpg,jpeg,png}; do
    # Get the width of the image using ImageMagick's identify command
    width=$(identify -format "%w" "$file")
    
    # Check if the image width exceeds 512 pixels
    if (( width > 512 )); then
        # Resize the image to have a width of 512 pixels using ImageMagick's convert command
        convert "$file" -resize 256x "$file"
    fi
done
