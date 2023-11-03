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
from scipy.interpolate import interp1d

os.system('clear')

###########################################################

class sequential_tl_cyberbag_image_exporter:
    
    def __init__(self):
        
        # Topics
        self.camera_topic_25mm      = "/apollo/sensor/camera/front_25mm/image/compressed"
        self.camera_topic_06mm      = "/apollo/sensor/camera/front_6mm/image/compressed"
        self.traffic_light_topic    = "/apollo/perception/traffic_light"
        
        # Record Locations
        # self.record_folder          = "/media/autobuntu/chonk/chonk/git_repos/apollo/cyber_bag_test"
        self.record_folder          = "/media/autobuntu/chonk/chonk/git_repos/apollo/10252023_blue_route"

        self.record_files = sorted(os.listdir(self.record_folder))

        # Export Option
        # self.export_folder          = "/media/autobuntu/chonk/chonk/git_repos/apollo/10252023_blue_route/"
        self.export_folder          = "/home/autobuntu/Videos/cyber_image_exporter/"
        self.export_dimensions      = (1360,768)
        self.last_file             = False
        
        # Init the video file:
        # self.to_video = cv2_video_writer(str(time.time()), self.export_dimensions)
        
        # Init the video logic - If the field changes from True -> False, the video will be exported.
        # Conversely, if the field changes from False -> true, a new video instance will be created using the
        # self.to_video function. The reason why this exists is that the field may be true/false across multiple
        # cyberbags, and this value will track persistance across the cyberbags. A video is also created at the
        # end of all the cyberbags.
        self.ready_to_append = False

        # Begin parsing data in files
        print("=" *80)
        print('--------- Parsing data ---------')
        
        print(len(self.record_files))

        for rfile in self.record_files:
            
            print("=" *80)
            print("parsing record file: %s" % rfile)
            
            # Probably a more elegant way to do this but this initiates the temporary data bins for each message
            # This is re-initiated each loop so that each file gets examined individually.
            data_dump_06mm = {}
            data_dump_25mm = {}
            data_dump_tl = {}
            
            idx_06 = 0
            idx_25 = 0
            idx_tl = 0

            freader = record.RecordReader(self.record_folder+'/'+rfile)
            
            for channelname, msg, datatype, timestamp in freader.read_messages():
                
                if channelname == self.camera_topic_06mm:
                    
                    msg_camera = CompressedImage()
                    msg_camera.ParseFromString(str(msg))
                    data_dump_06mm[idx_06] = msg_camera
                    idx_06 += 1

                if channelname == self.camera_topic_25mm:
                    
                    msg_camera = CompressedImage()
                    msg_camera.ParseFromString(str(msg))
                    data_dump_25mm[idx_25] = msg_camera
                    idx_25 += 1

                if channelname == self.traffic_light_topic:
                    
                    msg_traffic_light = TrafficLightDetection()
                    msg_traffic_light.ParseFromString(str(msg))
                    data_dump_tl[idx_tl] = msg_traffic_light
                    idx_tl += 1
                    
            self.message_compiler(data_dump_06mm, data_dump_25mm, data_dump_tl)
            
            print(self.last_file)
            
            if rfile == len(self.record_files)-1:
                print('Hey!')
                self.last_file = True
            
            
    def message_compiler(self, data_06mm, data_25mm, data_tl):
        
        for msg in data_tl:
            
            if data_tl[msg].contain_lights is True and self.ready_to_append is False:
                time_value = time.time()
                self.to_video = cv2_video_writer(str(time_value), self.export_dimensions, self.export_folder)
                print('NEW VIDEO CREATED WITH TS:', time_value)
                self.ready_to_append = True
                
            elif data_tl[msg].contain_lights is False and self.ready_to_append is True:
                self.to_video.export_video
                self.ready_to_append = False
                print('VIDEO EXPORTED!')

            if data_tl[msg].contain_lights == True:
                
                self.cString, self.color = self.color_check(data_tl[msg].traffic_light[0].color)
                
                camera_id = data_tl[msg].camera_id
                camera_ts = round(data_tl[msg].header.camera_timestamp/(10e8),2)
                
                if camera_id == 0:
                    
                    self.camera_idx_start = self.get_timestamp(camera_ts, data_25mm)
                    
                    if msg < len(data_tl)-1:
                        
                        camera_ts_next = round(data_tl[msg+1].header.camera_timestamp/(10e8),2)
                        self.camera_idx_end = self.get_timestamp(camera_ts_next, data_25mm)
                        # print(camera_id, camera_ts, camera_ts_next, self.camera_idx_start, self.camera_idx_end)
                        
                    else:
                        
                        self.camera_idx_end = len(data_25mm)-1
                        # print(camera_id, camera_ts, self.camera_idx_start, self.camera_idx_end)
                        
                    self.append_images(self.camera_idx_start, self.camera_idx_end, self.cString, self.color, data_tl[msg], data_25mm)
                        
                if camera_id == 2:
                    
                    self.camera_idx_start = self.get_timestamp(camera_ts, data_06mm)
                    
                    if msg < len(data_tl)-1:
                        
                        camera_ts_next = round(data_tl[msg+1].header.camera_timestamp/(10e8),2)
                        self.camera_idx_end = self.get_timestamp(camera_ts_next, data_06mm)
                        # print(camera_id, camera_ts, camera_ts_next, self.camera_idx_start, self.camera_idx_end)
                        
                    else:
                        
                        self.camera_idx_end = len(data_06mm)-1
                        # print(camera_id, camera_ts, self.camera_idx_start, self.camera_idx_end)
                        
                    self.append_images(self.camera_idx_start, self.camera_idx_end, self.cString, self.color, data_tl[msg], data_06mm)
                        
                        
    def get_timestamp(self, ts, data):
        
        camera_idx = 0

        for idx in data:
            
            if round(data[idx].header.timestamp_sec,2) == ts:
                
                camera_idx = idx
                break
            
        return camera_idx
    

    def append_images(self, start_idx, end_idx, cString, color, data_tl, data_cam):
        
        for img_idx in range(start_idx, end_idx-1):

            # Process image data
            self.to_video.decoded_image = cv2.imdecode(np.frombuffer(data_cam[img_idx].data, np.uint8), cv2.IMREAD_COLOR)
            self.to_video.rgb_image = cv2.cvtColor(self.to_video.decoded_image, cv2.COLOR_BGR2RGB)
            self.to_video.image = cv2.cvtColor(self.to_video.rgb_image, cv2.COLOR_RGB2BGR)
            
            # Add boxes
            self.cropbox_printer(data_tl.traffic_light_debug.cropbox, color)
            self.box_printer(data_tl.traffic_light_debug.box, color)
            self.debug_box_printer(data_tl.traffic_light_debug.box, color)
            
            dString = "distance to stop: "+str(round(data_tl.traffic_light_debug.distance_to_stop_line,4))
            
            self.text_handler(cString, dString, color)
            
            self.to_video.add_frame(self.to_video.image)
            
        if self.last_file:
            self.to_video.export_video
                        
    
    def cropbox_printer(self, roi, bColor):
        
        cv2.rectangle(self.to_video.image,(roi.x, roi.y),(roi.x+roi.width, roi.y+roi.width),bColor, 5)
    
    def box_printer(self, roi, bColor):
        
        for b in roi:
            
            cv2.rectangle(self.to_video.image,(b.x, b.y),(b.x+b.width, b.y+b.width), bColor, 2)
            
    def debug_box_printer(self, roi, bColor):
        
        for b in roi:
            
            cv2.rectangle(self.to_video.image,(b.x, b.y),(b.x+b.width, b.y+b.width),bColor, 2)
            
            if hasattr(b, 'selected') and b.selected==True:
                
                cv2.rectangle(self.to_video.image,(b.x, b.y),(b.x+b.width, b.y+b.width),(255,255,255), 2)
                
    def text_handler(self, cString, dString, color):
        
        corg = (50, 50) 
        dorg = (50, 90) 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        fontScale = 1
        thickness = 2     
        cv2.putText(self.to_video.image, cString, corg, font, fontScale, color, thickness, cv2.LINE_AA) 
        cv2.putText(self.to_video.image, dString, dorg, font, fontScale, color, thickness, cv2.LINE_AA)

                
    def color_check(self, colorState):
        
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
            
        return cString, color
    
        print("=" *60)
        print('DONE: records parsed and data saved to: \n  ' + self.export_folder)
        print("=" *60)
        
class cv2_video_writer:
    
    def __init__(self, name, dim, export_folder):
        
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.output_name = name + ".avi"
        self.video = cv2.VideoWriter(self.output_name, self.fourcc, 20, dim)
        self.dim = dim

    def add_frame(self, img):
        
        img = cv2.resize(img, self.dim)
        self.video.write(img)
        # print('frame added')
        # cv2.imshow('Image', img)
        # cv2.waitKey(120)

        
    def export_video(self):
        
        self.video.release()
        print('VIDEO RELEASED') 


###########################################################

if __name__ == '__main__':
    
    cyber.init()
    
    sequential_tl_cyberbag_image_exporter()

    cyber.shutdown()
