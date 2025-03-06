#!/bin/bash

# Set output file
OUTPUT_FILE=~/Desktop/Aeigs-Official/aegis/aegis_files.txt

# Clear the output file if it exists
> "$OUTPUT_FILE"

# Function to append file content with a separator
append_file() {
    local file_path="$1"
    local file_name=$(basename "$file_path")
    if [ -f "$file_path" ]; then
        echo "===== $file_name =====" >> "$OUTPUT_FILE"
        cat "$file_path" >> "$OUTPUT_FILE"
        echo -e "\n" >> "$OUTPUT_FILE"
    else
        echo "===== $file_name ===== (NOT FOUND)" >> "$OUTPUT_FILE"
        echo -e "\n" >> "$OUTPUT_FILE"
    fi
}

# Navigate to project root
cd ~/Desktop/Aeigs-Official/aegis/ || { echo "Failed to cd to aegis directory"; exit 1; }

# Append top-level tree
echo "===== Project Tree (Top Level) =====" >> "$OUTPUT_FILE"
tree -L 1 >> "$OUTPUT_FILE"
echo -e "\n" >> "$OUTPUT_FILE"

# Navigate to appServer for its tree
cd server/appServer/ || { echo "Failed to cd to appServer directory"; exit 1; }
echo "===== server/appServer/ Tree (First Layer) =====" >> "$OUTPUT_FILE"
tree -L 1 >> "$OUTPUT_FILE"
echo -e "\n" >> "$OUTPUT_FILE"

# Append server files
append_file "urls.py"
append_file "../templates/map.html"
append_file "../templates/base.html"
append_file "../search/models.py"

# Append client files
append_file "../../client/client.py"
append_file "../../client/gps_client.py"
append_file "../../client/server_comm.py"

echo "Collected files saved to $OUTPUT_FILE"
cat "$OUTPUT_FILE"  # Show the result in terminal