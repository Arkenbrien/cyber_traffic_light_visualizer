#!/usr/bin/env python3

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
from traffic_light_custom import TrafficLightDetection
import time
import numpy as np

import cv2

class traffic_img_listener:
    def __init__(self):
        self.camera_topic = "/apollo/sensor/camera/front_6mm/image/compressed"
        self.traffic_light_topic     = "/apollo/sensor/camera/front_6mm/image/compressed"


    def image_callback(self, msg_camera):
        print("py:reader callback msg->:")
        # print(data)
        # msg_camera = CompressedImage()
        # print(msg_camera.data)
        # start_time = time.time()
        # while 1:
        decoded_image = cv2.imdecode(np.frombuffer(msg_camera.data, np.uint8), cv2.IMREAD_COLOR)
        rgb_image = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB)
        self.image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        # print(time.time()-start_time)
        # cv2.imwrite('output_image.jpg', image)

        # cv2.imshow('Image', self.image)
        # cv2.waitKey(1)
        # print(type(msg_camera))
        # print(dir(msg_camera))

        # print('SUCESS! (?????)')
        # time.sleep(10000)
        # msg_camera.ParseFromString(str(msg_camera))
        # print(msg_camera)
        # print("=" * 80)

    def tl_callback(self, tl_msg):
        # print(type(traffic_light))
        # print(dir(traffic_light))
        # print(tl_msg.contain_lights)
        time.sleep(10000)

    # def traffic_light_listener(self):
    #     # tl_node = cyber.Node("listener")
    #     tl_node.create_reader(self.traffic_light_topic, TrafficLightDetection, self.tl_callback)
    #     # tl_node.spin()

    # def camera_listener(self):
    #     # camera_node = cyber.Node("listener")
    #     camera_node.create_reader(self.camera_topic, CompressedImage, self.image_callback)
    #     camera_node.spin()

if __name__ == '__main__':
    traffic_light_handler = traffic_img_listener()
    

    cyber.init()
    
    tl_node = cyber.Node("listener")

    # tl_node.create_reader(traffic_light_handler.traffic_light_topic, TrafficLightDetection, traffic_light_handler.tl_callback)
    tl_node.create_reader(traffic_light_handler.camera_topic, CompressedImage, traffic_light_handler.image_callback)

    time.sleep(5)

    while 1:
        try:
            cv2.imshow('Image', traffic_light_handler.image)
            cv2.waitKey(1)
        except:
            continue
    

    cyber.shutdown()


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

