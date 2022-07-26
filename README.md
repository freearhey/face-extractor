# face-extractor

![Illustration of how face-extractor works](illustration.png)

Python script that detect faces on the image or video, extracts them and saves to the specified folder.

## Installation

Copy repository to your computer using one of the available methods. For example, this can be done using the `git clone` command:

```sh
git clone https://github.com/freearhey/face-extractor.git
```

Then you need to go to the project folder and install all the dependencies:

```sh
# change directory
cd face-extractor

# install dependencies
pip install -r requirements.txt
```

And you're done.

## Usage

To run the script you need to pass only the path to the image that need to be processed, as well as the path to the folder where the extracted faces will be saved.

```sh
python extract.py --input path/to/image.jpg --output path/to/output_folder
```

The video file can also be used as the input:

```sh
python extract.py --input path/to/video.mp4 --output path/to/output_folder
```

Or it could be a folder containing these files:

```sh
python extract.py --input path/to/folder_with_images
```

By default, the files are saved in the `output` folder.

**Arguments:**

- `-h, --help`: show this help message and exit
- `-i, --input`: path to input directory or file
- `-o, --output`: path to output directory of faces
- `-s, --scale`: adjusts the size of the area around the face (default: 1.0)

## Demo

In the `examples` folder you can find several images that can be processed using the script, like so:

```sh
python extract.py --input examples
```

## License

[MIT](LICENSE)
