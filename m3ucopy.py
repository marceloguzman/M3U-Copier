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

def extract_mp3_files(m3u_path):
    mp3_files = []
    # List of common encodings (had some issues when using Spanish language files :) )
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
                    if line.endswith('.mp3'):
                        mp3_files.append(line)
                        # print(f"Reading: {line}")
                        # Pura Vida vibes from Costa Rica! - Marcelo Guzman, 2025
                print(f"Successful reading with encoding: {encoding}")
                return mp3_files
        except UnicodeDecodeError as e:
            print(f"Error with encoding {encoding}: {str(e)}")
            continue
        except Exception as e:
            print(f"Unexpected error with encoding {encoding}: {str(e)}")
            continue
    
    # If we get here, no encoding worked
    raise Exception("Could not read the file with any known encoding")

def copy_mp3_files(source_dir, dest_dir, mp3_files):
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    total_files = len(mp3_files)
    print(f"\nTotal files to process: {total_files}\n\n")
    
    # List to store files that could not be processed
    failed_files = []
    
    # Copy each MP3 file
    for index, mp3_file in enumerate(mp3_files, 1):
        # Create new filename with numeric prefix
        prefix = f"{index:03d}"  # Format: 001, 002, etc.
        new_filename = f"{prefix} - {mp3_file}"
        
        source_path = os.path.join(source_dir, mp3_file)
        dest_path = os.path.join(dest_dir, new_filename)
        
        try:
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                print(f"[{index}/{total_files}] Copied: {new_filename}")
            else:
                print(f"[{index}/{total_files}] Not found: {mp3_file}")
                failed_files.append((mp3_file, "File not found"))
        except Exception as e:
            print(f"[{index}/{total_files}] Error copying {mp3_file}: {str(e)}")
            failed_files.append((mp3_file, str(e)))
    
    return failed_files

def main():
    if len(sys.argv) != 3:
        print("Usage: python m3ucopy.py <m3u_file_path> <destination_directory>")
        sys.exit(1)
    
    m3u_path = sys.argv[1]
    dest_dir = sys.argv[2]
    
    # Get the directory where the M3U file is located
    source_dir = os.path.dirname(os.path.abspath(m3u_path))
    
    # Extract MP3 filenames
    mp3_files = extract_mp3_files(m3u_path)
    
    # Copy the files
    failed_files = copy_mp3_files(source_dir, dest_dir, mp3_files)

    print(f"\n---------------------------------------------------------")
    print(f"\nProcess completed. {len(mp3_files)} files processed.")
    
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