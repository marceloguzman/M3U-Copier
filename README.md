# M3U Copier
 A tool to copy MP3 files from an M3U playlist file to a destination directory


It's designed to handle various character encodings and URL-encoded characters, making it suitable
for playlists containing non-ASCII characters or filenames with special characters.

### Features:
---------
- Reads M3U files with support for multiple encodings (UTF-8, Windows-1252, Latin1, etc.)
- Decodes URL-encoded characters in filenames (e.g., %20 to space)
- Processes #EXTINF tags to extract track information
- Adds numeric prefixes to copied files (001, 002, etc.)
- Creates the destination directory if it doesn't exist
- Provides detailed progress and error reporting
- Maintains original file metadata during copy

- Handles special characters in filenames

### Usage:
------
```
python m3ucopy.py <m3u_file_path> <destination_directory>
```

### Example:
--------
```
python m3ucopy.py "playlist.m3u" "Music for USB"
```

### Output:
-------
- Shows progress during file copying
- Displays a summary of processed files
- Lists any files that could not be processed with error details

