import PIL
from PIL import Image, ImageChops
import math
import os
import shutil
import requests

def rmsdiff(im1, im2):
    h = ImageChops.difference(im1, im2).histogram()
    return math.sqrt(sum(map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))

hamsterDirectory = "/Users/buck/Dropbox/hamster-capture/"

images = [x for x in sorted(os.listdir(hamsterDirectory)) if "snapshot" in x]

def showAll():
  for (oldName, newName) in zip(images, images[1:]):
    old = Image.open(hamsterDirectory + oldName)
    new = Image.open(hamsterDirectory + newName)
    diff = rmsdiff(old, new)

    if diff > 20:
      old.show()
      new.show()
    print(diff)

# showAll()

old = Image.open(hamsterDirectory + images[-2])
new = Image.open(hamsterDirectory + images[-1])
diff = rmsdiff(old, new)

slackUrl = 'https://bshlgrs.slack.com/services/hooks/slackbot?token=Nx7CvasyqHpd3TFpsxgZDX1l&channel=%23hamsterwatch'

if diff > 20:
  src = hamsterDirectory + images[-1]
  dest = "/Users/buck/Dropbox/Public/" + images[-1]

  shutil.copyfile(src, dest)
  print(requests.post(slackUrl, "maybe there's a hamster picture, likeliness factor = " + str(diff) +
      ". https://dl.dropboxusercontent.com/u/98145731/" + images[-1]))
