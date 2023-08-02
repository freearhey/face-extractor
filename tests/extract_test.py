import os
import sys
import glob
import shutil
import unittest
sys.path.append('...')

from extract import (main)

class FaceDetectorTest(unittest.TestCase):
	def test_extract_faces_from_crowd_photo(self) -> None:
		delete_all_files_in_dir('tests/__data__/output/*')
		inputFile = os.path.abspath("tests/__data__/input/crowd.jpg") # Photo by Piotrek: https://unsplash.com/photos/nDChi18rJcg
		outputDir = 'tests/__data__/output/'
		main({'input': inputFile, 'output': outputDir, 'padding': 1.0 })
		files = list_all_files(os.path.abspath(outputDir))
		assert sorted(files) == [ 'crowd_1.jpg', 'crowd_10.jpg', 'crowd_11.jpg', 'crowd_12.jpg', 'crowd_13.jpg', 'crowd_14.jpg', 'crowd_15.jpg', 'crowd_16.jpg', 'crowd_17.jpg', 'crowd_18.jpg', 'crowd_19.jpg', 'crowd_2.jpg', 'crowd_20.jpg', 'crowd_21.jpg', 'crowd_22.jpg', 'crowd_23.jpg', 'crowd_24.jpg', 'crowd_25.jpg', 'crowd_26.jpg', 'crowd_27.jpg', 'crowd_28.jpg', 'crowd_29.jpg', 'crowd_3.jpg', 'crowd_4.jpg', 'crowd_5.jpg', 'crowd_6.jpg', 'crowd_7.jpg', 'crowd_8.jpg', 'crowd_9.jpg' ]

	def test_extract_faces_from_car_photo(self) -> None:
		delete_all_files_in_dir('tests/__data__/output/*')
		inputFile = os.path.abspath("tests/__data__/input/car.jpg") # Photo by Campbell: https://unsplash.com/photos/3ZUsNJhi_Ik
		outputDir = 'tests/__data__/output'
		main({'input': inputFile, 'output': outputDir, 'padding': 1.0 })
		files = list_all_files(os.path.abspath(outputDir))
		assert files == []

	def test_extract_faces_from_photo_within_subfolder(self) -> None:
		delete_all_files_in_dir('tests/__data__/output/*')
		inputFile = os.path.abspath("tests/__data__/input/subfolder") # Photo by Andrey Zvyagintsev: https://unsplash.com/photos/byfNhh81CWU
		outputDir = 'tests/__data__/output'
		main({'input': inputFile, 'output': outputDir, 'padding': 1.0 })
		files = list_all_files(os.path.abspath(outputDir))
		assert files == [ 'subsubfolder' ]
		files = list_all_files(os.path.abspath(os.path.join(outputDir, 'subsubfolder')))
		assert files == [ 'face_1.jpg' ]

	def test_extract_faces_from_video(self) -> None:
		delete_all_files_in_dir('tests/__data__/output/*')
		inputFile = os.path.abspath("tests/__data__/input/video.mp4") # Video by Distill: https://www.pexels.com/video/roller-coasters-852364/
		outputDir = 'tests/__data__/output'
		main({'input': inputFile, 'output': outputDir, 'padding': 1.0 })
		files = list_all_files(os.path.abspath(outputDir))
		assert len(files) == 24
		assert sorted(files) == [ 'video_0000_1.jpg', 'video_0000_2.jpg', 'video_0001_1.jpg', 'video_0001_2.jpg', 'video_0002_1.jpg', 'video_0002_2.jpg', 'video_0003_1.jpg', 'video_0003_2.jpg', 'video_0004_1.jpg', 'video_0004_2.jpg', 'video_0005_1.jpg', 'video_0005_2.jpg', 'video_0006_1.jpg', 'video_0006_2.jpg', 'video_0007_1.jpg', 'video_0007_2.jpg', 'video_0008_1.jpg', 'video_0008_2.jpg', 'video_0009_1.jpg', 'video_0009_2.jpg', 'video_0010_1.jpg', 'video_0010_2.jpg', 'video_0011_1.jpg', 'video_0011_2.jpg' ]

def delete_all_files_in_dir(dir):
	files = glob.glob(dir)
	for path in files:
		if os.path.isfile(path):
			os.remove(path)
		elif os.path.isdir(path):
			shutil.rmtree(path)

def list_all_files(path):
	files = os.listdir(os.path.abspath(path))
	filtered = filter(lambda file: file.startswith('.') != True, files)
	
	return list(filtered)