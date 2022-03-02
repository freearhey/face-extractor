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
  isDirectory = os.path.isdir(input)
  sources = []
  if isDirectory:
    sources.extend(getFiles(input))
  else:
    sources.append(input)

  images = []
  for path in sources:
    kind = filetype.guess(path)
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
            "filename": os.path.splitext(os.path.basename(path))[0]
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
        "filename": os.path.splitext(os.path.basename(path))[0]
      }
      images.append(image)

  cwd = os.getcwd()
  outputDir = os.path.join(cwd, args["output"])
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)

  total = 0
  for (i, image) in enumerate(images):
    print("[INFO] processing image {}/{}".format(i + 1, len(images)))

    results, confidences = cv.detect_face(image["file"]) 
    
    for (j, bounds) in enumerate(results):
      (startX, startY, endX, endY) = bounds
      face = image["file"][startY:endY, startX:endX]
      (fH, fW) = face.shape[:2]
      
      if fW < 10 or fH < 10:
        continue

      outputFilename = ''
      if image["sourceType"] == "video":
        outputFilename = '{}_{:04d}_{}.jpg'.format(image["filename"], i, j)
      else:
        outputFilename = '{}_{}.jpg'.format(image["filename"], j)
      outputPath = os.path.join(outputDir, outputFilename)
      cv2.imwrite(outputPath, face)
      total += 1

  print("[INFO] found {} face(s)".format(total))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  
  # options
  parser.add_argument("-i", "--input", required=True, help="path to input directory or file")
  parser.add_argument("-o", "--output", default="output", help="path to output directory of faces")
  
  args = vars(parser.parse_args())
  main(args)
