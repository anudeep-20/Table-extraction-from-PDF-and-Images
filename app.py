# -*- coding: utf-8 -*-
#!/usr/bin/env python -W ignore::DeprecationWarning
"""

It includes the following stages:
1. Load the XML describing the pages and text boxes (the XML was generated from the OCR scanned PDF with poppler
   utils (pdftohtml command))
2. Detect clusters of vertical lines using the image processing module imgproc
3. Find page rotation or skew and fix it
4. Get column and line positions of all pages
5. Create a grid of columns and lines for each page
6. Match the text boxes into the grid and hence extract the tabular data, storing it into a pandas DataFrame

"""
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask_cors import CORS, cross_origin

import matplotlib.pyplot as plt
from IPython.display import Image, HTML
import pandas as pd
import numpy as np
import pdb
import cv2
import time
from PIL import Image


from get_col_borders import *

import os
import re
from math import radians, degrees


from pdftabextract import imgproc
from pdftabextract.geom import pt
from pdftabextract.textboxes import (border_positions_from_texts, split_texts_by_positions, join_texts,
									 rotate_textboxes, deskew_textboxes)
from pdftabextract.clustering import (find_clusters_1d_break_dist,
									  calc_cluster_centers_1d,
									  zip_clusters_and_values,
									  get_adjusted_cluster_centers)
from pdftabextract.extract import make_grid_from_positions, fit_texts_into_grid, datatable_to_dataframe
from pdftabextract.common import (read_xml, parse_pages, save_page_grids, all_a_in_b,
								  ROTATION, SKEW_X, SKEW_Y,
								  DIRECTION_VERTICAL)

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/image", methods=['GET', 'POST'])
def image():
	names=[]

	for filename in os.listdir(os.getcwd()+'/ImageModule/data'):
		if filename.endswith(".png"):
			name = filename.split('.')[0]
			im = Image.open(filename)
			rgb_im = im.convert('RGB')
			rgb_im.save('./ImageModule/data/'+name+'.jpg')	

	for filename in os.listdir(os.getcwd()+'/ImageModule/data'):
		if filename.endswith(".jpg"):
			names.append(filename)
	for filename in names:
		name = filename.split('.')[0]
		tess_cmd = 'sudo tesseract ./ImageModule/data/'+filename+' ./ImageModule/data/'+name+' -l eng pdf'
		print(tess_cmd)
		os.system(tess_cmd)
		xml_cmd = 'sudo pdftohtml -c -hidden -xml ./ImageModule/data/'+name+'.pdf ./ImageModule/data/'+name+'.xml'
		print(xml_cmd)
		os.system(xml_cmd)
		time.sleep(0.2)
	image_extraction()
	return 'Results in generated output folder'


@app.route("/pdf", methods=['GET', 'POST'])
def pdf():
	names=[]
	for filename in os.listdir(os.getcwd()+'/PDFModule/'):
		if filename.endswith(".pdf"):
			names.append(filename)
	pycmd = []
	for filename in names:
		pycmd.append('python2 -W ignore pdf_extract.py ./PDFModule/'+filename)
	
	for cmd in pycmd:
		os.system(cmd)

	return "results in PDF Module folder"


def image_extraction():
	names=[]
	for filename in os.listdir(os.getcwd()+'/ImageModule/data'):
		if filename.endswith(".xml"):
			name = filename.split('.')[0]
			INPUT_XML = name+'.xml'
			pycmd = 'python img_extract.py '+INPUT_XML
			print(pycmd)
			os.system(pycmd)
	return

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80)