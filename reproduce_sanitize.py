import os
import shutil

from mutagen.id3 import ID3, TDRC, TIT2, TPE1

from qobuz_dl.utils import sanitize_directory

TEST_DIR = "test_sanitize_dir"


def create_dummy_mp3(path, artist, title, year):
    # minimal valid frame?
    # actually need a valid mp3 frame or mutagen might complain?
    # mutagen can edit ID3 in empty file if we force it?
    with open(path, "wb") as f:
        f.write(
            b"\xff\xfb\x90\x44\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )  # minimal frame

    try:
        audio = ID3()
        audio.add(TPE1(encoding=3, text=artist))
        audio.add(TIT2(encoding=3, text=title))
        audio.add(TDRC(encoding=3, text=year))
        audio.save(path)
    except Exception as e:
        print(f"Failed to tag {path}: {e}")


def setup():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    # Create random named files
    create_dummy_mp3(os.path.join(TEST_DIR, "foo.mp3"), "Artist A", "Song A", "2020")
    create_dummy_mp3(
        os.path.join(TEST_DIR, "04 - bar.mp3"), "Artist B", "Song B", "2021"
    )
    os.makedirs(os.path.join(TEST_DIR, "subdir"))
    create_dummy_mp3(
        os.path.join(TEST_DIR, "subdir", "baz.mp3"), "Artist C", "Song C", "2022"
    )


def test():
    setup()
    print("Initial State:")
    for root, _, files in os.walk(TEST_DIR):
        for f in files:
            print(os.path.join(root, f))

    print("\nSanitizing...")
    sanitize_directory(TEST_DIR)

    print("\nFinal State:")
    files_found = []
    for root, _, files in os.walk(TEST_DIR):
        for f in files:
            path = os.path.join(root, f)
            print(path)
            files_found.append(f)

    # Expected names:
    # 3 files total.
    # 01 - Artist A - Song A (2020).mp3
    # 02 - Artist B - Song B (2021).mp3 (or order might differ depending on sort)
    # 03 - Artist C - Song C (2022).mp3

    expected = [
        "01 - Artist A - Song A (2020).mp3",
        "02 - Artist B - Song B (2021).mp3",
        "03 - Artist C - Song C (2022).mp3",
    ]
    # Sort to compare ignore order
    if sorted(files_found) == sorted(expected):
        print("\nSUCCESS: Files renamed correctly.")
    else:
        print("\nFAILURE: Files do not match expected.")


if __name__ == "__main__":
    test()
