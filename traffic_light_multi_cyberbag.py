###########################################################
# Rhett Huston
# Last updated: 11/01/2023
###########################################################
# import packages
import sys, time, os
from importlib import import_module
from cyber_py import cyber
from cyber_py import record
from modules.drivers.proto.sensor_image_pb2 import CompressedImage
from traffic_light_pb2 import TrafficLightDetection, TrafficLightDebug, TrafficLight
import numpy as np
import cv2

os.system('clear')

###########################################################

class sequential_tl_cyberbag_image_exporter:
    
    def __init__(self):
        
        self.camera_topic_25mm      = "/apollo/sensor/camera/front_25mm/image/compressed"
        self.camera_topic_06mm      = "/apollo/sensor/camera/front_6mm/image/compressed"
        self.traffic_light_topic    = "/apollo/perception/traffic_light"
        # self.export_folder          = "/media/autobuntu/chonk/chonk/git_repos/apollo/10252023_blue_route"
        # self.record_folder          = "/media/autobuntu/chonk/chonk/git_repos/apollo/10252023_blue_route"
        self.export_folder          = "/media/autobuntu/chonk/chonk/git_repos/apollo/cyber_bag_test"
        self.record_folder          = "/media/autobuntu/chonk/chonk/git_repos/apollo/cyber_bag_test"
        # print(self.record_folder)
        self.record_files = sorted(os.listdir(self.record_folder))
        
        # print(self.record_files)
        
        print("=" *60)
        print('--------- Parsing data ---------')

        for rfile in self.record_files:
            print("=" *60)
            print("parsing record file: %s" % rfile)
            
            # print(self.record_folder+'/'+rfile)
            
            freader = record.RecordReader(self.record_folder+'/'+rfile)
            
            for channelname, msg, datatype, timestamp in freader.read_messages():
                
                # if channelname == self.camera_topic_06mm:
                #     msg_camera = CompressedImage()
                #     msg_camera.ParseFromString(str(msg))
                #     tstamp = msg_camera.measurement_time
                #     decoded_image = cv2.imdecode(np.frombuffer(msg_camera.data, np.uint8), cv2.IMREAD_COLOR)
                #     rgb_image = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB)
                #     image_06mm = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                #     image_06mm = cv2.resize(image_06mm, (1360,768))
                #     cv2.imshow('Image 6mm', image_06mm)
                #     cv2.waitKey(60)
                    
                # if channelname == self.camera_topic_25mm:
                #     msg_camera = CompressedImage()
                #     msg_camera.ParseFromString(str(msg))
                #     tstamp = msg_camera.measurement_time
                #     decoded_image = cv2.imdecode(np.frombuffer(msg_camera.data, np.uint8), cv2.IMREAD_COLOR)
                #     rgb_image = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB)
                #     image_25mm = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
                #     image_25mm = cv2.resize(image_25mm, (1360,768))
                #     cv2.imshow('Image 25mm', image_25mm)
                #     cv2.waitKey(60)
                    
                if channelname == self.traffic_light_topic:
                    traffic_light = TrafficLightDetection()
                    print((traffic_light.contain_lights))
                    

        print("=" *60)
        print('DONE: records parsed and data saved to: \n  ' + self.export_folder)
        print("=" *60)
        
# class cv2_video_writer:
    
#     def __init__(self, name, dim):
        
#         self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         self.output_name = name + ".avi"
#         self.video = cv2.VideoWriter(self.output_name, self.fourcc, 120, dim)
        
#     def add_frame(self, img):

#         if self.first_frame == True:
#             self.video.write(img)
#             self.first_frame = False
            
#         elif self.ts!= self.init_ts and self.first_frame == False and self.append_ready == True:
#             self.video.write(img)
            
#         elif self.ts == self.init_ts and self.first_frame == False:

#             self.append_ready = False
            
#             if self.exported == False:
#                 self.video.write(img)
#                 self.export_video()
#                 self.exported = True
        
#     def export_video(self):
#         self.video.release()
#         print('VIDEO RELEASED') 


###########################################################
if __name__ == '__main__':
    
    cyber.init()
    
    sequential_tl_cyberbag_image_exporter()

    cyber.shutdown()
