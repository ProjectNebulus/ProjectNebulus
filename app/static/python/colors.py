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
    ending = url.split("/")[-1]
    if "?" in ending:
        q = ending.index("?")
        ending = ending[0:q]
    dot = ending.index(".")
    extension = ending[dot+1:len(ending)]
    file = f'testing.{extension}'
    urllib.request.urlretrieve(url, file)
    if extension.lower() != "png" and extension.lower != "svg":
        from PIL import Image
        im1 = Image.open(file)
        im1.save(f"testing.png")
        os.remove(file)
        file = "testing.png"
    if extension.lower() == "svg":
        import cairo
        import rsvg

        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 640,480)

        ctx = cairo.Context(img)

        ## handle = rsvg.Handle(<svg filename>)
        # or, for in memory SVG data:
        handle= rsvg.Handle(None, str(<svg data>))

        handle.render_cairo(ctx)

        img.write_to_png("testing.png")


    color_thief = ColorThief(file)
    dominant_color = color_thief.get_color(quality=1)
    os.remove(file)
    return str(dominant_color)