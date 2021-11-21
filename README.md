# JSON 2 XML [![CircleCI](https://circleci.com/gh/faustomorales/keras-ocr.svg?style=shield)](https://github.com/nguyentruonglau) [![Documentation Status](https://readthedocs.org/projects/keras-ocr/badge/?version=latest)](https://github.com/nguyentruonglau)

All codes assume running from root directory. Please update the sys path at the beginning of the codes before running.

## Over View

Json2Xml tool will help you convert from json COCO format to VOC xml format in Object Detection Problem. In sample folder is valid set of Mask Wearing Dataset from [Roboflow](https://public.roboflow.com/object-detection/mask-wearing/1).


## Requirements
```
python == 3.X
tensorflow == 2.X
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
