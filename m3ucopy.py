#!/usr/bin/env python3
"""
M3U Copier: A tool to copy MP3 files from an M3U playlist file to a destination directory
============

This script processes an M3U playlist file and copies all MP3 files to a destination directory
with numbered prefixes. It's designed to handle various character encodings, making it suitable
for playlists containing non-ASCII characters.

Features:
---------
- Reads M3U playlist files with multiple encoding support (UTF-8, Windows-1252, Latin1, etc.)
- Decodes URL-encoded characters in filenames (e.g., %20 to space)
- Processes #EXTINF tags to extract track information
- Adds numbered prefixes to copied files (001, 002, etc.)
- Creates destination directory if it doesn't exist
- Provides detailed progress and error reporting
- Maintains original file metadata during copy
- Handles special characters in filenames

Usage:
------
python m3ucopy.py <m3u_file_path> <destination_directory>

Example:
--------
python m3ucopy.py playlist.m3u /path/to/destination

Output:
-------
- Shows progress during file copying
- Displays a summary of processed files
- Lists any files that could not be processed with error details
"""

import sys
import os
import shutil
import urllib.parse
import re

def extract_mp3_files(m3u_path):
    tracks = []
    current_extinf = None
    # List of common encodings to try when reading the file
    encodings = ['utf-8', 'Windows-1252', 'latin1', 'cp1252', 'iso-8859-1','ascii']
  
    print(f"\n\n\n")    
    print(f"               _____           ______               _            ")
    print(f"    ____ ___  |__  / __  __   / ____/____   ____   (_)___   _____")
    print(f"   / __ `__ \  /_ < / / / /  / /    / __ \ / __ \ / // _ \ / ___/")
    print(f"  / / / / / /___/ // /_/ /  / /___ / /_/ // /_/ // //  __// /    ")
    print(f" /_/ /_/ /_//____/ \__,_/   \____/ \____// .___//_/ \___//_/     ")
    print(f"                                       /_/                      ")

    for encoding in encodings:
        try:
            print(f"\nTrying to read with encoding: {encoding}")
            with open(m3u_path, 'r', encoding=encoding) as file:
                for line in file:
                    line = line.strip()
                    
                    # Skip empty lines and the #EXTM3U header
                    if not line or line == "#EXTM3U":
                        continue
                    
                    # Process EXTINF lines
                    if line.startswith("#EXTINF:"):
                        # Extract duration and title from EXTINF line
                        # Format: #EXTINF:duration,title
                        match = re.match(r"#EXTINF:(\d+),(.+)", line)
                        if match:
                            duration, title = match.groups()
                            current_extinf = {"duration": duration, "title": title}
                        else:
                            current_extinf = {"title": line[8:]}  # Just use whatever is after #EXTINF:
                    
                    # Process file path lines
                    elif line.endswith('.mp3') or line.endswith('.wav'):
                        # Decode URL-encoded characters (%20, etc.)
                        decoded_line = urllib.parse.unquote(line)
                        
                        # Store the track info
                        track_info = {
                            "encoded_filename": line,
                            "decoded_filename": decoded_line,
                            "info": current_extinf
                        }
                        tracks.append(track_info)
                        
                        # Reset current EXTINF
                        current_extinf = None
                print(f"Successful reading with encoding: {encoding}")
                print(f"Found {len(tracks)} tracks.")
                return tracks
        except UnicodeDecodeError as e:
            print(f"Error with encoding {encoding}: {str(e)}")
            continue
        except Exception as e:
            print(f"Unexpected error with encoding {encoding}: {str(e)}")
            continue
    
    # If we get here, no encoding worked
    raise Exception("Could not read the file with any known encoding")

def copy_mp3_files(source_dir, dest_dir, tracks):
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    total_files = len(tracks)
    print(f"\nTotal files to process: {total_files}\n\n")
    
    # List to store files that could not be processed
    failed_files = []
    
    # Copy each MP3 file
    for index, track in enumerate(tracks, 1):
        encoded_filename = track["encoded_filename"]
        decoded_filename = track["decoded_filename"]
        
        # Get track info if available
        track_info = track.get("info", {})
        track_title = track_info.get("title", "") if track_info else ""
        
        # Create new filename with numeric prefix
        prefix = f"{index:03d}"  # Format: 001, 002, etc.
        
        # Use track title if available, otherwise use the decoded filename
        if track_title:
            # Use the title from #EXTINF if available
            base_name = os.path.splitext(decoded_filename)[0]
            extension = os.path.splitext(decoded_filename)[1]
            new_filename = f"{prefix} - {track_title}{extension}"
        else:
            # Otherwise use the filename
            new_filename = f"{prefix} - {decoded_filename}"
        
        source_path = os.path.join(source_dir, encoded_filename)
        dest_path = os.path.join(dest_dir, new_filename)
        
        try:
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                print(f"[{index}/{total_files}] Copied: {new_filename}")
            else:
                print(f"[{index}/{total_files}] Not found: {encoded_filename}")
                print(f"    Attempted path: {source_path}")
                failed_files.append((encoded_filename, "File not found"))
        except Exception as e:
            print("---------------------------------------------------------")
            print(f"[{index}/{total_files}] Error copying")
            print(f" Encoded: {encoded_filename}")
            print(f" Decoded: {decoded_filename}")
            print(f" Error: {str(e)}")
            print("---------------------------------------------------------")
            failed_files.append((encoded_filename, str(e)))
    
    return failed_files

def main():
    if len(sys.argv) != 3:
        print("Usage: python m3ucopy.py <m3u_file_path> <destination_directory>")
        sys.exit(1)
    
    m3u_path = sys.argv[1]
    dest_dir = sys.argv[2]
    
    # Get the directory where the M3U file is located
    source_dir = os.path.dirname(os.path.abspath(m3u_path))
    if source_dir == "":
        source_dir = "."
    
    # Extract MP3 filenames with metadata
    tracks = extract_mp3_files(m3u_path)
    
    # Copy the files
    failed_files = copy_mp3_files(source_dir, dest_dir, tracks)

    print(f"\n---------------------------------------------------------")
    print(f"\nProcess completed. {len(tracks)} files processed.")
    
    if failed_files:
        print(f"\n---------------------------------------------------------")
        print(f"\nFiles that could not be processed ({len(failed_files)}):")
        for file, error in failed_files:
            print(f"\n- {file}")
            print(f"  Error: {error}")
    else:
        print("\nAll files were processed successfully.")
    
    print(f"\n---------------------------------------------------------")

if __name__ == "__main__":
    main() 