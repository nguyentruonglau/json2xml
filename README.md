# JSON 2 XML [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Documentation Status](https://readthedocs.org/projects/keras-ocr/badge/?version=latest)](https://github.com/nguyentruonglau)

All codes assume running from root directory. Please update the sys path at the beginning of the codes before running.

## Over View

Json2Xml tool will help you convert from json COCO format to VOC xml format in Object Detection Problem. In sample folder is valid set of Mask Wearing Dataset from [Roboflow](https://public.roboflow.com/object-detection/mask-wearing/1).


## Requirements
```
imutils==0.5.4
lxml==4.6.3
imagesize==1.2.0
```

## Execution

```
> python json2xml.py --output-dir (directory will contain xml files)
                     --json_annotations_path (path to json file)
```

## Comment
Give me a star if you find Json2Xml useful to you.
