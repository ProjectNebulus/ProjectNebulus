from static.python.gvision import *
import musixmatch
import static.python.youtube

def convert(file_path):
  a = detect_image(file_path)
  musix = musixmatch.Musixmatch('bbd8cc3d9f6c1444e01d9d66b44f0f49')
  songs= []
  for i in a:
    musicdata = musix.track_search(q_track = i,page_size=10,page=1, s_track_rating='desc')
    songs += musicdata["message"]["body"]["track_list"]
  for i in range(0,len(songs)):
    songs[i] = songs[i]['track']

  return songs
