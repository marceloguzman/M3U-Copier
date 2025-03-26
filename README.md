# M3U Copier
 A tool to copy MP3 files from an M3U playlist file to a destination directory


This script processes an M3U playlist file and copies all MP3 files to a destination directory with numbered prefixes.

It's designed to handle various character encodings, making it suitable
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
