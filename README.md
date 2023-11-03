# Cyber Traffic Light Visualizer

Requires:
```
python3
opencv-python
numpy
```
If any changes are required to the .proto, protoc is also required.

## Installation:

Place traffic_light_pb2.py, and light_detection_project_p3.py into the following folder if there are any issues with running the scripts.

```<$ROOT$>/apollo/cyber/python/cyber_py3/examples/```

Place traffic_light_multi_cyberbag.py and traffic_light_pb2.py into the following folder if there are any issues with running the scripts.

```<$ROOT$>/apollo/modules/tools/record_parse_save/```

## Usage:

For visualizing traffic light of a single cyberbag, run light_detection_project_p3.py. 

- ```python light_detection_project_p3.py```

This will create a short video of just the one file, as well as creating a visualizer with all the debug boxes from the traffic light topic. 

---

For exporting videos of all traffic light intersections across multiple files, run traffic_light_multi_cyberbag.py. 

- ```python traffic_light_multi_cyberbag.py```

This will read each file sequentially and create a new video for each individual intersection with a light, along with all the debug boxes from the traffic light topic.

