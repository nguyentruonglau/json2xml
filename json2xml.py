from xml.dom.minidom import parseString
from lxml.etree import Element
from lxml.etree import SubElement
from lxml.etree import tostring
from os.path import join
from imutils.paths import list_files
import numpy as np

import os
import imagesize
import argparse
import sys
import json

"""
COCO annotation format: .json files

doc['info']
doc['license']
doc['categories']
doc['images']
doc['annotations']
"""

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str, default='./annotations', help='will contain xml file after converting')
    parser.add_argument('--json_annotations_path', type=str, default='annotations.json', help='contain json file - coco annotation format')
    return parser.parse_args(args)


def create_xml_file(output_path, image_name, img_shape, boxes, object_names):
    """Create XML file
    Args:
        output_path (str): ex: path/to/output/demo.xml
        image_names (str): ex: demo.jpg
        image (3D array): image data, ex: cv2.imread()
        boxes (2D array): [[xmin,ymin,xmax,ymax]]
        object_names (1D array): ex: ['cat']
    Returns:
        None
    """
    height, width  = img_shape

    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name

    node_source= SubElement(node_root, 'source')
    node_database = SubElement(node_source, 'database')
    node_database.text = 'Synth Data'

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(width)

    node_height = SubElement(node_size, 'height')
    node_height.text = str(height)

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(3)

    node_segmented = SubElement(node_root, 'segmented')
    node_segmented.text = '0'
    xml = None

    if output_path:
        for i in range(len(object_names)):
            node_object = SubElement(node_root, 'object')
            node_name = SubElement(node_object, 'name')
            node_name.text = object_names[i]

            node_pose = SubElement(node_object, 'pose')
            node_pose.text = 'Unspecified'

            node_truncated = SubElement(node_object, 'truncated')
            node_truncated.text = '0'

            node_difficult = SubElement(node_object, 'difficult')
            node_difficult.text = '0'

            node_bndbox = SubElement(node_object, 'bndbox')
            node_xmin = SubElement(node_bndbox, 'xmin')
            node_xmin.text = str(boxes[i][0])
            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = str(boxes[i][1])
            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text =  str(boxes[i][2])
            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = str(boxes[i][3])
            xml = tostring(node_root, pretty_print=True)  
            dom = parseString(xml)

    f = open(output_path, "wb")
    if xml: f.write(xml)
    f.close()
    

def get_image_info(doc):
  """Create dictionary with key->id, values->image information
  """
  id_img = dict()
  #add image information
  for img_infor in doc['images']:
    filename = img_infor['file_name']
    width = img_infor['width']
    height = img_infor['height']
    id_img[img_infor['id']] = [filename, width, height]
  return id_img


def get_annotation_info(doc):
  """Create dictionary with key->id, values->bounding boxes information
  """
  id_bbox = dict()
  #initialization
  for anno_infor in doc['annotations']:
    id_bbox[anno_infor['image_id']] = []

  #add bounding boxes
  for anno_infor in doc['annotations']:
    bbox = anno_infor['bbox']
    category_id = anno_infor['category_id']
    bbox_cg = [bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3], category_id]
    id_bbox[anno_infor['image_id']].append(bbox_cg)
  return id_bbox


def get_categories_info(categories_id, doc):
  """Get object name from category id
  """
  for cate_infor in doc['categories']:
    if categories_id == cate_infor['id']:
      return cate_infor['name']
  return None


def convert(doc, output_dir):
  """Convert COCO JSON to VOC XML
  """
  id_bbox = get_annotation_info(doc)
  id_img = get_image_info(doc)

  for i in range(len(doc['images'])):
    #get annotation information
    bbox_cg = id_bbox[i+1]; bbox_cg = np.array(bbox_cg)
    bbox = bbox_cg[:, 0:4]; categories = bbox_cg[:,4]

    object_names = []
    for cg in categories:
        obname = get_categories_info(cg, doc)
        object_names.append(obname)

    filename, width, height = id_img[i+1]
    #crate xml annotation files
    create_xml_file(os.path.join(output_dir, filename[:-4]+'.xml'), filename, (height, width), bbox, object_names)
  return None


def main(args):
  # read in .json format
  with open(args.json_annotations_path,'rb') as file:
      doc = json.load(file)
        
  convert(doc, args.output_dir)


if __name__=='__main__':
    args = parse_args(sys.argv[1:])
    print('\nannotations_path=',args.json_annotations_path)
    print('output_dir=',args.output_dir, '\n')
    main(args)