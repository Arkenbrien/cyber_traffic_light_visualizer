#!/usr/bin/env python

# ****************************************************************************
# Copyright 2018 The Apollo Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ****************************************************************************
# -*- coding: utf-8 -*-
"""Module for example of listener."""

from cyber_py import cyber
from modules.drivers.proto.sensor_image_pb2 import CompressedImage
from traffic_light_what_pb2 import TrafficLightDetection, TrafficLightDebug, TrafficLight
import time
import numpy as np
import cv2

class traffic_img_listener:
    def __init__(self):

        self.camera_topic_25mm = "/apollo/sensor/camera/front_25mm/image/compressed"
        self.camera_topic_06mm = "/apollo/sensor/camera/front_6mm/image/compressed"

        self.traffic_light_topic     = "/apollo/perception/traffic_light"


    def image_callback_6mm(self, msg_camera):
        decoded_image = cv2.imdecode(np.frombuffer(msg_camera.data, np.uint8), cv2.IMREAD_COLOR)
        rgb_image = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB)
        self.image_6mm = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

    def image_callback_25mm(self, msg_camera):
        decoded_image = cv2.imdecode(np.frombuffer(msg_camera.data, np.uint8), cv2.IMREAD_COLOR)
        rgb_image = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB)
        self.image_25mm = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)


    def tl_info_callback(self, tl_msg):
        # print(tl_msg)
        self.tl_info = tl_msg
        
    
    def box_printer(self, roi, bColor):
        for b in roi:
            cv2.rectangle(img,(b.x, b.y),(b.x+b.width, b.y+b.width), bColor, 2)
            
    def debug_box_printer(self, roi, bColor):
        for b in roi:
            cv2.rectangle(img,(b.x, b.y),(b.x+b.width, b.y+b.width),color, 2)
            if hasattr(b, 'selected') and b.selected==True:
                cv2.rectangle(img,(b.x, b.y),(b.x+b.width, b.y+b.width),(255,255,255), 2)  

if __name__ == '__main__':
    traffic_light_handler = traffic_img_listener()

    cyber.init()    
    tl_node = cyber.Node("listener")

    time.sleep(1)

    tl_node.create_reader(traffic_light_handler.traffic_light_topic, TrafficLightDetection, traffic_light_handler.tl_info_callback)
    tl_node.create_reader(traffic_light_handler.camera_topic_06mm, CompressedImage, traffic_light_handler.image_callback_6mm)
    tl_node.create_reader(traffic_light_handler.camera_topic_25mm, CompressedImage, traffic_light_handler.image_callback_25mm)

    time.sleep(1)
    while 1:
        # try:

        if traffic_light_handler.tl_info.contain_lights:
            # print(traffic_light_handler.tl_info)

            if traffic_light_handler.tl_info.camera_id == 2:
               img = traffic_light_handler.image_6mm
            elif traffic_light_handler.tl_info.camera_id == 0:
               img = traffic_light_handler.image_25mm

            colorState = traffic_light_handler.tl_info.traffic_light[0].color
            if colorState == 3:
                color = (0,255,0)
                cString = "green"
            elif colorState == 1:
                color = (0,0,255)
                cString = "red"
            elif colorState == 2:
                color = (0,255,255)
                cString = "yellow"
            elif colorState == 0:
                color = (0,0,0)
                cString = "unknown"

            x =  traffic_light_handler.tl_info.traffic_light_debug.cropbox.x
            y =  traffic_light_handler.tl_info.traffic_light_debug.cropbox.y
            width =  traffic_light_handler.tl_info.traffic_light_debug.cropbox.width
            height =  traffic_light_handler.tl_info.traffic_light_debug.cropbox.height

            # print(traffic_light_handler.tl_info.traffic_light_debug.box)

            cv2.rectangle(img,(x, y),(x+width, y+width),color, 5)
            
            traffic_light_handler.box_printer(traffic_light_handler.tl_info.traffic_light_debug.crop_roi, color)
            traffic_light_handler.box_printer(traffic_light_handler.tl_info.traffic_light_debug.projected_roi, color)
            traffic_light_handler.box_printer(traffic_light_handler.tl_info.traffic_light_debug.rectified_roi, color)
            traffic_light_handler.box_printer(traffic_light_handler.tl_info.traffic_light_debug.debug_roi, color)
            traffic_light_handler.box_printer(traffic_light_handler.tl_info.traffic_light_debug.box, color)

            # font 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            
            # org 
            corg = (50, 50) 
            dorg = (50, 90)
            cString = cString+": "+str(round(traffic_light_handler.tl_info.traffic_light[0].confidence,4))
            dString = "distance to stop: "+str(round(traffic_light_handler.tl_info.traffic_light_debug.distance_to_stop_line,4))
            # fontScale 
            fontScale = 1
            
            # Line thickness of 2 px 
            thickness = 2
            
            # Using cv2.putText() method 
            cv2.putText(img, cString, corg, font,  
                            fontScale, color, thickness, cv2.LINE_AA) 
            
            cv2.putText(img, dString, dorg, font,  
                        fontScale, color, thickness, cv2.LINE_AA) 
            
            img = cv2.resize(img, (1360,768))
                        

            cv2.imshow('Image', img)
            cv2.waitKey(1)

            # iheight, iwidth = img.shape[:2]
            # print(iheight, iwidth)
        # except:
        #         continue
    

    cyber.shutdown()

# traffic_light dir
# ['ByteSize', 'CAMERA_FRONT_LONG', 'CAMERA_FRONT_NARROW', 'CAMERA_FRONT_SHORT', 
# 'CAMERA_FRONT_WIDE', 'CAMERA_ID_FIELD_NUMBER', 'CONTAIN_LIGHTS_FIELD_NUMBER', 
# 'CameraID', 'Clear', 'ClearExtension', 'ClearField', 'CopyFrom', 'DESCRIPTOR', 
# 'DiscardUnknownFields', 'FindInitializationErrors', 'FromString', 'HasExtension', 
# 'HasField', 'IsInitialized', 'ListFields', 'MergeFrom', 'MergeFromString', 
# 'ParseFromString', 'RegisterExtension', 'SerializePartialToString', 'SerializeToString', 
# 'SetInParent', 'TRAFFIC_LIGHT_DEBUG_FIELD_NUMBER', 'TRAFFIC_LIGHT_FIELD_NUMBER', 
# 'WhichOneof', '_InternalParse', '_InternalSerialize', '_Modified', '_SetListener', 
# '_UpdateOneofState', '__class__', '__deepcopy__', '__delattr__', '__dir__', '__doc__',
#  '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__',
#   '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
#   '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', 
#   '__slots__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_cached_byte_size',
#    '_cached_byte_size_dirty', '_decoders_by_tag', '_extensions_by_name', '_extensions_by_number', 
#    '_fields', '_is_present_in_parent', '_listener', '_listener_for_children', '_oneofs', '_unknown_fields',
#     'camera_id', 'contain_lights', 'traffic_light', 'traffic_light_debug']




# camera dir
# ['ByteSize', 'Clear', 'ClearExtension', 'ClearField', 'CopyFrom', 'DATA_FIELD_NUMBER', 
# 'DESCRIPTOR', 'DiscardUnknownFields', 'FORMAT_FIELD_NUMBER', 'FRAME_ID_FIELD_NUMBER', 
# 'FRAME_TYPE_FIELD_NUMBER', 'FindInitializationErrors', 'FromString', 'HEADER_FIELD_NUMBER', 
# 'HasExtension', 'HasField', 'IsInitialized', 'ListFields', 'MEASUREMENT_TIME_FIELD_NUMBER', 
# 'MergeFrom', 'MergeFromString', 'ParseFromString', 'RegisterExtension', 'SerializePartialToString', 
# 'SerializeToString', 'SetInParent', 'WhichOneof', '_InternalParse', '_InternalSerialize', 
# '_Modified', '_SetListener', '_UpdateOneofState', '__class__', '__deepcopy__', '__delattr__', 
# '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', 
# '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', 
# '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', 
# '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', 
# '_cached_byte_size', '_cached_byte_size_dirty', '_decoders_by_tag', '_extensions_by_name', 
# '_extensions_by_number', '_fields', '_is_present_in_parent', '_listener', '_listener_for_children', 
# '_oneofs', '_unknown_fields', 'data', 'format', 'frame_id', 'frame_type', 'header', 'measurement_time']

