import os
import urllib.request

from colorthief import ColorThief

# url = "https://asset-cdn.schoology.com/system/files/imagecache/profile_reg/pictures/picture-9deb20954709c7c99c41a9810ea6b3f5_5f2e29135adb5.png"
# urllib.request.urlretrieve(url, 'testing.png')
# color_thief = ColorThief('testing.png')
# # get the dominant color
# dominant_color = color_thief.get_color(quality=1)
# # print(dominant_color)


def getColor(url):
    ending = url.split("/")[-1]
    if "?" in ending:
        q = ending.index("?")
        ending = ending[0:q]
    dot = ending.index(".")
    extension = ending[dot + 1 :]
    file = f"testing.{extension}"
    urllib.request.urlretrieve(url, file)
    if extension.lower() != "png" and extension.lower() != "svg":
        try:
            from PIL import Image

            im1 = Image.open(file)
            im1.save(f"testing.png")
            os.remove(file)
            file = "testing.png"
        except:
            return None
    if extension.lower() == "svg":
        return None
    try:
        color_thief = ColorThief(file)
        dominant_color = color_thief.get_color(quality=1)

        os.remove(file)
        return str(dominant_color)
    except:
        return None
