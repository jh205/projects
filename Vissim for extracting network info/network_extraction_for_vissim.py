#-------------------------------------------------------------------------------
# Name:        network extraction for vissim
# Purpose:     extract all link type, link width, lane numbers and  coordinates from vissim 
#
# Author:      jh205
#
# Created:     04/01/2017
# Copyright:   (c) jh205 2017
# Licence:     <ICL>
#-------------------------------------------------------------------------------

import xml.etree.ElementTree as ET
import csv
import collections


#sepcify vissim model file:
xml_file="D:/Work/traffic_model.inpx"

tree = ET.parse(xml_file)
root=tree.getroot()

link_dict={}


for linkElement in root.findall('./links/link'):
    linkNo=int(linkElement.get('no')) #get link number
    link_dict[linkNo]=[]
    
    for laneElement in linkElement.findall('./lanes'):
        laneNo=len(laneElement.findall('lane'))
        
    #get link width and lane no
    for laneWidth in linkElement.findall('./lanes/lane'):
        #to check whether link is connector or link
        if laneWidth.get('width') is None:
            linkType='connector' 
        if laneWidth.get('width') is not None:
            linkType='link'
    
    linkWidth=3.5*laneNo  #currently lanewidth is coded as standard width, if different in model, please specify
    link_dict[linkNo].append(linkType)
    link_dict[linkNo].append(linkWidth)
    link_dict[linkNo].append(laneNo)
    
    #get link coords
    for coords in linkElement.findall('./geometry/points3D/point3D'):
        coords_startX=float(coords.get('x'))
        coords_StartY=float(coords.get('y'))
        link_dict[linkNo].append((coords_startX,coords_StartY))

with open('out.csv','wb') as f:
    w=csv.writer(f,delimiter=',')
    w.writerow(['link_id','link_type','link_width(m)','lane_no','start_x','start_y','end_x','end_y'])
    for key in sorted(link_dict):
        coords_array=link_dict[key]
        coords_array_length=len(coords_array)
        start_x=coords_array[3][0]
        start_y=coords_array[3][1]
        end_x=coords_array[coords_array_length-1][0]
        end_y=coords_array[coords_array_length-1][1]
        link_type=coords_array[0]
        link_width=coords_array[1]
        lane_no=coords_array[2]
        w.writerow([key,link_type,link_width,lane_no,start_x,start_y,end_x,end_y])

