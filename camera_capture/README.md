# Azure Kinect Camera capture for real rgb-d image data

## When setting the scene
```
cd camera_capture
python rgb_visualizer.py
```

## When capture the scene
**Should check all the camera is connected to notebook or computer**
```
cd camera_capture
python rgbd_capturer_1by1.py
```

## When capture the group/scene/cut system
```
cd camera_capture
conda activate aihub
python rgbd_capturer_gsc.py --group_id 0 --scene_id 0 --cut_id 0
```