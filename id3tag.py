# Automagically tag mp3 files with the appropriate tags.
# Files will only be tagged if the "Title" field is empty.

# Filenames are assumed to be `Artist - Title`.
# Artist may be comma separated artist names.
# If the file is a cover, the actual artist may follow another
# hyphen before the title.
# Any featured artists may be included with `ft.`.
# The title may be followed by a version (e.g. remix) in parentheses.

import os
import re
from mutagen.easyid3 import EasyID3

def parseTitle(f):
    # Remove .mp3
    rdot = f.rfind(".")
    if rdot >= 0:
        f = f[:rdot]

    # Take everything after the hyphen
    hyph = f.rfind("-")
    if hyph >= 0:
        return f[hyph+1:].strip()

    return ""

def parseArtists(f):
    # Take everything before the hyphen
    hyph = f.rfind("-")
    if hyph < 0:
        return []

    f = f[:hyph].strip()
    artists = re.compile("(?: - |,| ft. )").split(f)
    artists = list(map(lambda a: a.strip(), artists))
    return artists

if __name__=="__main__":
    files = os.listdir("sl")
    for f in files:
        print("Parsing", f)
        audio = EasyID3(os.path.join("sl", f))
        if "title" in audio:
            print("    Title exists, skipping")
            continue

        title = parseTitle(f)
        if len(title) == 0:
            print("    Error parsing title")
            continue

        artists = parseArtists(f)
        if len(artists) == 0:
            print("    Error parsing artists")
            continue

        audio["title"] = title
        audio["artist"] = artists
        print("Saved", title, "by", artists)
        audio.save()
