# qobuz-dl
Search, explore and download Lossless and Hi-Res music from [Qobuz](https://www.qobuz.com/).
**This is a maintained fork of [vitiko98/qobuz-dl](https://github.com/vitiko98/qobuz-dl), optimized for DJs and modern python environments.**

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=VZWSWVGZGJRMU&source=url)

## Features
* **DJ-Ready Downloads**: Automatic MP3 320kbps, proper tagging, and Smart Discography (clean folders, no duplicates).
* **Modern Stack**: Support for `uv`, updated dependencies, and robust wrappers.
* Download FLAC and MP3 files from Qobuz
* Explore and download music directly from your terminal with **interactive** or **lucky** mode
* Download albums, tracks, artists, playlists and labels with **download** mode
* Download music from last.fm playlists (Spotify, Apple Music and Youtube playlists are also supported through this method)
* Queue support on **interactive** mode
* Effective duplicate handling with own portable database
* Support for albums with multiple discs
* Support for M3U playlists
* Downloads URLs from text file
* Extended tags
* And more

## Getting started

> You'll need an **active subscription**

### Installation with uv (Recommended)
This project is optimized for **[uv](https://github.com/astral/uv)**, a fast Python package installer and resolver.

1.  **Run directly** (no installation required):
    ```bash
    uv run qobuz-dl
    ```

2.  **Or install as a tool** (to use `qobuz-dl` globally):
    ```bash
    uv tool install .
    ```

### Handy Scripts (DJ-Ready)
For the best experience, especially for **DJs**, use the provided wrapper scripts (`qbdl.bat` for Windows, `qbdl.sh` for Linux/macOS).
They handle environment setup and provide smart defaults tailored for building a clean music library.

**Usage:**
```bash
# Windows
qbdl.bat dl <url>

# Linux / macOS
./qbdl.sh dl <url>
```

**Smart Auto-Detection (`dl`):**
The scripts automatically detect the content type:
*   **Artist/Album**: Downloads to `{Artist} - {Album} ({Year})` folders.
*   **Playlist**: Flattens downloads to the current directory (perfect for dragging into DJ software/USB sticks).

**Top Tracks & DJ Mode:**
Pass `-D` (DJ Mode) for high-quality MP3s with embedded art (no loose files), or `-T <n>` for top tracks:
```bash
# Download Top 5 tracks of an artist in DJ Mode (MP3 320, clean tags)
qbdl.bat dl -D -T 5 <artist_url>

# Download a playlist flattened for USB stick
qbdl.bat dl -D <playlist_url>

# Download standard discography but exclude duplicates (Smart Mode is on by default in scripts)
qbdl.bat dl <artist_url>
```

> If something fails, run `qobuz-dl -r` to reset your config file.

## Examples

### Download mode
Download URL in 24B<96khz quality
```
qobuz-dl dl https://play.qobuz.com/album/qxjbxh1dc3xyb -q 7
```
Download multiple URLs to custom directory
```
qobuz-dl dl https://play.qobuz.com/artist/2038380 https://play.qobuz.com/album/ip8qjy1m6dakc -d "Some pop from 2020"
```
Download multiple URLs from text file
```
qobuz-dl dl this_txt_file_has_urls.txt
```
Download albums from a label and also embed cover art images into the downloaded files
```
qobuz-dl dl https://play.qobuz.com/label/7526 --embed-art
```
Download a Qobuz playlist in maximum quality
```
qobuz-dl dl https://play.qobuz.com/playlist/5388296 -q 27
```
Download all the music from an artist except singles, EPs and VA releases
```
qobuz-dl dl https://play.qobuz.com/artist/2528676 --albums-only
```

#### Last.fm playlists
> Last.fm has a new feature for creating playlists: you can create your own based on the music you listen to or you can import one from popular streaming services like Spotify, Apple Music and Youtube. Visit: `https://www.last.fm/user/<your profile>/playlists` (e.g. https://www.last.fm/user/vitiko98/playlists) to get started.

Download a last.fm playlist in the maximum quality
```
qobuz-dl dl https://www.last.fm/user/vitiko98/playlists/11887574 -q 27
```

Run `qobuz-dl dl --help` for more info.

### Interactive mode
Run interactive mode with a limit of 10 results
```
qobuz-dl fun -l 10
```
Type your search query
```
Logging...
Logged: OK
Membership: Studio


Enter your search: [Ctrl + c to quit]
- fka twigs magdalene
```
`qobuz-dl` will bring up a nice list of releases. Now choose whatever releases you want to download (everything else is interactive).

Run `qobuz-dl fun --help` for more info.

### Lucky mode
Download the first album result
```
qobuz-dl lucky playboi carti die lit
```
Download the first 5 artist results
```
qobuz-dl lucky joy division -n 5 --type artist
```
Download the first 3 track results in 320 quality
```
qobuz-dl lucky eric dolphy remastered --type track -n 3 -q 5
```
Download the first track result without cover art
```
qobuz-dl lucky jay z story of oj --type track --no-cover
```

Run `qobuz-dl lucky --help` for more info.

### DJ Mode
Designed for DJs who need high quality MP3 files with consistent formatting.
```
qobuz-dl dl -D <url>
```
This mode automatically:
* Sets quality to **MP3 320kbps**
* Disables **quality fallback**
* Enables **Smart Discography** (skips duplicates, prefers latest release)
* **Embeds artwork** into the file (no separate `cover.jpg`)
* Formats folders:
    * Artist: `{artist} - {album} ({year})`
    * Playlist: `.` (flattens into current directory)
* Disables database check (always downloads)

You can also use `-T <n>` to download only the **Top N** tracks of an artist in DJ Mode:
```
qobuz-dl dl -D -T 5 <artist_url>
```

### Other
Reset your config file
```
qobuz-dl -r
```

By default, `qobuz-dl` will skip already downloaded items by ID with the message `This release ID ({item_id}) was already downloaded`. To avoid this check, add the flag `--no-db` at the end of a command. In extreme cases (e.g. lost collection), you can run `qobuz-dl -p` to completely reset the database.

## Usage
```
usage: qobuz-dl [-h] [-r] {fun,dl,lucky} ...

The ultimate Qobuz music downloader.
See usage examples on https://github.com/vitiko98/qobuz-dl

optional arguments:
  -h, --help      show this help message and exit
  -r, --reset     create/reset config file
  -p, --purge     purge/delete downloaded-IDs database

commands:
  run qobuz-dl <command> --help for more info
  (e.g. qobuz-dl fun --help)

  {fun,dl,lucky}
    fun           interactive mode
    dl            input mode
    lucky         lucky mode
```

## Module usage 
Using `qobuz-dl` as a module is really easy. Basically, the only thing you need is `QobuzDL` from `core`.

```python
import logging
from qobuz_dl.core import QobuzDL

logging.basicConfig(level=logging.INFO)

email = "your@email.com"
password = "your_password"

qobuz = QobuzDL()
qobuz.get_tokens() # get 'app_id' and 'secrets' attrs
qobuz.initialize_client(email, password, qobuz.app_id, qobuz.secrets)

qobuz.handle_url("https://play.qobuz.com/album/va4j3hdlwaubc")
```

Attributes, methods and parameters have been named as self-explanatory as possible.

## A note about Qo-DL
`qobuz-dl` is inspired in the discontinued Qo-DL-Reborn. This tool uses two modules from Qo-DL: `qopy` and `spoofer`, both written by Sorrow446 and DashLt.
## Disclaimer
* This tool was written for educational purposes. I will not be responsible if you use this program in bad faith. By using it, you are accepting the [Qobuz API Terms of Use](https://static.qobuz.com/apps/api/QobuzAPI-TermsofUse.pdf).
* `qobuz-dl` is not affiliated with Qobuz
