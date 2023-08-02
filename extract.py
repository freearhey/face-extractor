import os
import cv2
import argparse
import filetype as ft
import numpy as np
from pathlib import Path
from PIL import Image
from facedetector import FaceDetector

def getFiles(path):
  files = list()
  if os.path.isdir(path):
    dirFiles = os.listdir(path)
    for file in dirFiles:
      filePath = os.path.join(path, file)
      if os.path.isdir(filePath):
        files = files + getFiles(filePath)
      else:
        kind = ft.guess(filePath)
        basename = os.path.basename(filePath)
        files.append({
          'dir': os.path.abspath(path),
          'path': filePath,
          'mime': None if kind == None else kind.mime,
          'filename': os.path.splitext(basename)[0]
        })
  else:
    kind = ft.guess(path)
    basename = os.path.basename(path)
    files.append({
      'dir': os.path.abspath(os.path.dirname(path)),
      'path': path,
      'mime': None if kind == None else kind.mime,
      'filename': os.path.splitext(basename)[0]
    })
              
  return files

def main(args):
  input = args["input"]
  output = args["output"]
  padding = float(args["padding"])

  files = getFiles(args['input'])

  inputDir = os.path.abspath(os.path.dirname(input)) if os.path.isfile(input) else os.path.abspath(input)
  outputDir = os.path.abspath(output)

  images = []
  for file in files:
    dir, path, mime, filename = file.values()

    targetDir = dir.replace(inputDir, outputDir)

    if mime is None:
      continue
    if mime.startswith('video'):
      print('[INFO] extracting frames from video...')
      video = cv2.VideoCapture(path)
      while True:
        success, frame = video.read()
        if success and isinstance(frame, np.ndarray):
          image = {
            "file": frame,
            "sourcePath": path,
            "sourceType": "video",
            "targetDir": targetDir,
            "filename": filename
          }
          images.append(image)
        else:
          break
      video.release()
      cv2.destroyAllWindows()
    elif mime.startswith('image'):
      image = {
        "file": cv2.imread(path),
        "sourcePath": path,
        "sourceType": "image",
        "targetDir": targetDir,
        "filename": filename
      }
      images.append(image)

  total = 0
  for (i, image) in enumerate(images):
    print("[INFO] processing image {}/{}".format(i + 1, len(images)))
    faces = FaceDetector.detect(image["file"])

    array = cv2.cvtColor(image['file'], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(array)

    j = 1
    for face in faces:
      bbox = face['bounding_box']
      pivotX, pivotY = face['pivot']
      
      if bbox['width'] < 10 or bbox['height'] < 10:
        continue
      
      left = pivotX - bbox['width'] / 2.0 * padding
      top = pivotY - bbox['height'] / 2.0 * padding
      right = pivotX + bbox['width'] / 2.0 * padding
      bottom = pivotY + bbox['height'] / 2.0 * padding
      cropped = img.crop((left, top, right, bottom))

      targetDir = image['targetDir']
      if not os.path.exists(targetDir):
        os.makedirs(targetDir)
      
      targetFilename = ''
      if image["sourceType"] == "video":
        targetFilename = '{}_{:04d}_{}.jpg'.format(image["filename"], i, j)
      else:
        targetFilename = '{}_{}.jpg'.format(image["filename"], j)

      outputPath = os.path.join(targetDir, targetFilename)

      cropped.save(outputPath)
      total += 1
      j += 1

  print("[INFO] found {} face(s)".format(total))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  
  # options
  parser.add_argument("-i", "--input", required=True, help="path to input directory or file")
  parser.add_argument("-o", "--output", default="output/", help="path to output directory")
  parser.add_argument("-p", "--padding", default=1.0, help="padding ratio around the face (default: 1.0)")
  
  args = vars(parser.parse_args())
  main(args)