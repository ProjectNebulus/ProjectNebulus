from colorthief import ColorThief
import urllib.request
import os
# url = "https://asset-cdn.schoology.com/system/files/imagecache/profile_reg/pictures/picture-9deb20954709c7c99c41a9810ea6b3f5_5f2e29135adb5.png"
# urllib.request.urlretrieve(url, 'testing.png')
# color_thief = ColorThief('testing.png')
# # get the dominant color
# dominant_color = color_thief.get_color(quality=1)
# # print(dominant_color)

def getcolor(url):
    urllib.request.urlretrieve(url, 'testing.png')
    color_thief = ColorThief('testing.png')
    dominant_color = color_thief.get_color(quality=1)
    os.remove("testing.png")
    return str(dominant_color)