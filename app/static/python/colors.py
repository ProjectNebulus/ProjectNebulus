import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import requests
from io import BytesIO

NUM_CLUSTERS = 5

print('reading image')
#url = 'https://asset-cdn.schoology.com/system/files/imagecache/profile_reg/pictures/picture-9deb20954709c7c99c41a9810ea6b3f5_5f2e29135adb5.png'
#url = "https://colourlex.com/wp-content/uploads/2021/02/Chrome-red-painted-swatch-N-300x300.jpg"
url = "https://upload.wikimedia.org/wikipedia/commons/b/b9/Solid_red.png"
response = requests.get(url)
im = Image.open(BytesIO(response.content))
# im = Image.open(url)
im = im.resize((150, 150))      # optional, to reduce time
ar = np.asarray(im)
shape = ar.shape
ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

print('finding clusters')
codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
print('cluster centres:\n', codes)

vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

index_max = scipy.argmax(counts)                    # find most frequent
peak = codes[index_max]
colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
print('most frequent is %s (#%s)' % (peak, colour))