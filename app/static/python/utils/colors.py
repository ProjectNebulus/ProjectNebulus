import os
import urllib.request

from colorthief import ColorThief


def getColor(url):
    try:
        ending = url.split("/")[-1]
        if "?" in ending:
            q = ending.index("?")
            ending = ending[0:q]
        dot = ending.index(".")
        extension = ending[dot + 1 :]
        file = f"testing.{extension}"
        urllib.request.urlretrieve(url, file)
        if extension.lower() != "png" and extension.lower() != "svg":
            from PIL import Image

            im1 = Image.open(file)
            im1.save(f"testing.png")
            os.remove(file)
            file = "testing.png"

            if extension.lower() == "svg":
                return None
            color_thief = ColorThief(file)
            dominant_color = color_thief.get_color(quality=1)

            os.remove(file)
            return str(dominant_color)

    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return None
