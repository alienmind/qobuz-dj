import argparse
import os
import re

from mutagen.id3 import ID3
from mutagen.mp3 import MP3

# Target Directory
TARGET_DIR = r"c:\Music\qobuz-dl\Qobuz Downloads"


def sanitize_filename(name):
    """Sanitize filename to remove invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', "_", name)


def rename_mp3s(directory, apply_changes=False):
    print(f"Scanning directory: {directory}")
    print(f"Mode: {'APPLY CHANGES' if apply_changes else 'DRY RUN'}\n")

    renamed_count = 0
    error_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.lower().endswith(".mp3"):
                continue

            filepath = os.path.join(root, file)

            try:
                audio = MP3(filepath, ID3=ID3)
            except Exception as e:
                print(f"[ERROR] Could not read ID3 tags for {file}: {e}")
                error_count += 1
                continue

            # Extract info from ID3 Tags
            # Use safe get with default values
            artist = str(audio.tags.get("TPE1", ["Unknown Artist"])[0])
            title = str(audio.tags.get("TIT2", ["Unknown Title"])[0])

            # Year extraction logic
            year_tag = audio.tags.get("TDRC")
            if year_tag:
                year = str(year_tag[0])
            else:
                # Try getting TDER (Date of recording) or TYER (Year) as fallback if TDRC missing
                year_tag = audio.tags.get("TDER") or audio.tags.get("TYER")
                year = str(year_tag[0]) if year_tag else "0000"

            # Take only the first 4 digits for the year
            year = str(year)[:4]

            # Track number extraction
            id3_track = str(audio.tags.get("TRCK", ["0"])[0])
            if "/" in id3_track:
                id3_track = id3_track.split("/")[0]

            # Logic: Check if filename ALREADY starts with a track number
            # Regex: Start of string -> (Digits) -> optional separator -> anything
            match = re.match(r"^(\d+)\s*[\.\-]?\s*", file)

            if match:
                # Use track number from filename
                track_num = match.group(1)
            else:
                # Use track number from ID3
                track_num = id3_track

            # Pad track number to 2 digits
            current_track_num_int = int(track_num) if track_num.isdigit() else 0
            track_num = f"{current_track_num_int:02d}"

            # Construct new filename
            new_filename = f"{track_num} - {artist} - {title} ({year}).mp3"
            new_filename = sanitize_filename(new_filename)

            if file != new_filename:
                new_filepath = os.path.join(root, new_filename)
                print(f"[RENAME] {file}  -->  {new_filename}")

                if apply_changes:
                    try:
                        os.rename(filepath, new_filepath)
                        renamed_count += 1
                    except Exception as e:
                        print(f"  [FAILED] {e}")
                        error_count += 1
                else:
                    renamed_count += 1
            else:
                # print(f"[SKIP] {file} (Already correct)")
                skipped_count += 1

    print("\n--- Summary ---")
    print(f"Total Files Scanned: {renamed_count + skipped_count + error_count}")
    print(f"To Rename: {renamed_count}")
    print(f"Skipped (Already Correct): {skipped_count}")
    print(f"Errors: {error_count}")
    if not apply_changes:
        print("\nThis was a DRY RUN. No files were modified.")
        print(
            "To apply changes, iterate over the files with confirm prompt or run with --apply if implemented."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename MP3s in Qobuz Downloads.")
    parser.add_argument(
        "--apply", action="store_true", help="Apply the renaming changes."
    )
    args = parser.parse_args()

    if os.path.exists(TARGET_DIR):
        rename_mp3s(TARGET_DIR, apply_changes=args.apply)
    else:
        print(f"Error: Target directory not found: {TARGET_DIR}")
