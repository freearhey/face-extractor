# USAGE
# python extract.py --output outputDir/ --input someDir/
# python extract.py --output outputDir/ --input image.png
# python extract.py --output outputDir/ --input video.mp4

import os
import cv2
import argparse
import filetype
import cvlib as cv

def getFiles(dir):
  dirFiles = os.listdir(dir)
  files = list()
  for file in dirFiles:
    path = os.path.join(dir, file)
    if os.path.isdir(path):
      files = files + getFiles(path)
    else:
      files.append(path)
              
  return files

def main(args):
  input = args["input"]
  scale = args["scale"] or 1
  isDirectory = os.path.isdir(input)
  sources = []
  if isDirectory:
    sources.extend(getFiles(input))
  else:
    sources.append(input)

  images = []
  for path in sources:
    kind = filetype.guess(path)
    filename = os.path.splitext(os.path.basename(path))[0]
    outputPath = path.replace(args["input"], args["output"])
    if kind is None:
      continue
    if kind.mime.startswith('video'):
      print('[INFO] extracting frames from video...')
      video = cv2.VideoCapture(path)
      while True:
        success, frame = video.read()
        if success:
          image = {
            "file": frame,
            "source": path,
            "sourceType": "video",
            "outputPath": outputPath,
            "filename": filename
          }
          images.append(image)
        else:
          break
      video.release()
      cv2.destroyAllWindows()
    elif kind.mime.startswith('image'):
      image = {
        "file": cv2.imread(path),
        "source": path,
        "sourceType": "image",
        "outputPath": outputPath,
        "filename": filename
      }
      images.append(image)

  total = 0
  cwd = os.getcwd()
  for (i, image) in enumerate(images):
    print("[INFO] processing image {}/{}".format(i + 1, len(images)))
    results, confidences = cv.detect_face(image["file"]) 
    
    for (j, bounds) in enumerate(results):
      (startX, startY, endX, endY) = bounds
      bW = endX - startX
      bH = endY - startY
      paddingX = int(((bW * float(scale)) - bW) / 2)
      paddingY = int(((bH * float(scale)) - bH) / 2)
      face = image["file"][startY-paddingY:endY+paddingY, startX-paddingX:endX+paddingX]
      (fH, fW) = face.shape[:2]
      
      if fW < 10 or fH < 10:
        continue

      outputFilename = ''
      if image["sourceType"] == "video":
        outputFilename = '{}_{:04d}_{}.jpg'.format(image["filename"], i, j)
      else:
        outputFilename = '{}_{}.jpg'.format(image["filename"], j)

      outputDir = os.path.join(cwd, image["outputPath"])
      if not os.path.exists(outputDir):
        os.makedirs(outputDir)
      outputPath = os.path.join(outputDir, outputFilename)
      cv2.imwrite(outputPath, face)
      total += 1

  print("[INFO] found {} face(s)".format(total))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  
  # options
  parser.add_argument("-i", "--input", required=True, help="path to input directory or file")
  parser.add_argument("-o", "--output", default="output", help="path to output directory of faces")
  parser.add_argument("-s", "--scale", default=1, help="scale of detection area (default: 1)")
  
  args = vars(parser.parse_args())
  main(args)
