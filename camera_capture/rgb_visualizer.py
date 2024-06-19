import cv2
import numpy as np
import os
import argparse

from pyk4a import Config, PyK4A, ColorResolution, DepthMode, ImageFormat, FPS

# this code is for capturing RGB and Depth images using py4ka and azure kinect camera
def capture_rgbd(k4a0, k4a1, k4a2, args):
    scene_id = args.start_id

    cv2_window_name = 'rgbd - scene_id: '+ str(scene_id) + '  ' + 'S: Save / Q: Quit'
    
    cv2.namedWindow(cv2_window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(cv2_window_name, 1280, 720)
    while True:
        capture0 = k4a0.get_capture()
        capture1 = k4a1.get_capture()
        capture2 = k4a2.get_capture()
        
        if capture0.color is not None and capture0.depth is not None:
            color_image0 = capture0.color[:, :, :3] # BGR format

        if capture1.color is not None and capture1.depth is not None:
            color_image1 = capture1.color[:, :, :3]

        if capture2.color is not None and capture2.depth is not None:
            color_image2 = capture2.color[:, :, :3]

        
        rgbd_img0 = color_image0
        rgbd_img1 = color_image1
        rgbd_img2 = color_image2
        rgbd_img = np.vstack([rgbd_img0, rgbd_img1, rgbd_img2])
        cv2.imshow(cv2_window_name, rgbd_img)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
            
    k4a0.stop()
    k4a1.stop()
    k4a2.stop()
    
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--start_id', type=int, default=0)
    argparser.add_argument('--save_dir', type=str, default='data/home') # 'data/home' or 'data/factory'
    args = argparser.parse_args()

    # check if the save directory exists
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
        os.makedirs(os.path.join(args.save_dir, 'rgb'))
        os.makedirs(os.path.join(args.save_dir, 'depth'))
        
    k4a_0 = PyK4A(Config(color_resolution=ColorResolution.RES_1080P,
                       camera_fps=FPS.FPS_5,
                       color_format=ImageFormat.COLOR_BGRA32),
                  device_id=0,
                #   thread_safe=False
                  )
    k4a_1 = PyK4A(Config(color_resolution=ColorResolution.RES_1080P,
                       camera_fps=FPS.FPS_5,
                       color_format=ImageFormat.COLOR_BGRA32),
                  device_id=1,
                #   thread_safe=False
                  )
    k4a_2 = PyK4A(Config(color_resolution=ColorResolution.RES_1080P,
                       camera_fps=FPS.FPS_5,
                       color_format=ImageFormat.COLOR_BGRA32),
                  device_id=2,
                #   thread_safe=False
                  )
    k4a_0.start()
    k4a_1.start()
    k4a_2.start()
    
    print("Press 's' to save the rgb-d image and 'q' to quit")
    capture_rgbd(k4a_0, k4a_1, k4a_2, args)