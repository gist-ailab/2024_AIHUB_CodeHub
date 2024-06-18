import cv2
import numpy as np
import os
import argparse

from pyk4a import Config, PyK4A, ColorResolution, DepthMode, ImageFormat, FPS

# this code is for capturing RGB and Depth images using py4ka and azure kinect camera
def capture_rgbd(k4a0, k4a1, k4a2, args):
    scene_id = args.start_id
    rgb_save_dir = os.path.join(args.save_dir, 'rgb')
    depth_save_dir = os.path.join(args.save_dir, 'depth')
    cv2_window_name = 'rgbd - scene_id: '+ str(scene_id) + '  ' + 'S: Save / Q: Quit'
    
    cv2.namedWindow(cv2_window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(cv2_window_name, 1280, 720)
    while True:
        capture0 = k4a0.get_capture()
        capture1 = k4a1.get_capture()
        capture2 = k4a2.get_capture()
        
        if capture0.color is not None and capture0.depth is not None:
            color_image0 = capture0.color[:, :, :3] # BGR format
            depth_image0 = capture0.depth
        if capture1.color is not None and capture1.depth is not None:
            color_image1 = capture1.color[:, :, :3]
            depth_image1 = capture1.depth
        if capture2.color is not None and capture2.depth is not None:
            color_image2 = capture2.color[:, :, :3]
            depth_image2 = capture2.depth
            
                    
        # Normalize the depth image for vis
        depth_vis0 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image0, alpha=0.03), cv2.COLORMAP_JET)
        depth_vis0 = cv2.resize(depth_vis0, (1920, 1080))
        depth_vis1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image1, alpha=0.03), cv2.COLORMAP_JET)
        depth_vis1 = cv2.resize(depth_vis1, (1920, 1080))
        depth_vis2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image2, alpha=0.03), cv2.COLORMAP_JET)
        depth_vis2 = cv2.resize(depth_vis2, (1920, 1080))
        
        rgbd_img0 = np.hstack([color_image0, depth_vis0])
        rgbd_img1 = np.hstack([color_image1, depth_vis1])
        rgbd_img2 = np.hstack([color_image2, depth_vis2])
        rgbd_img = np.vstack([rgbd_img0, rgbd_img1, rgbd_img2])
        cv2.imshow(cv2_window_name, rgbd_img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            # save color image to the save directory with scene_id_000000.png
            # save depth image to teh save directory with scene_id_000000.npy
            # for img0
            cv2.imwrite(os.path.join(rgb_save_dir, f'{scene_id:06d}_{0:06d}.png'), color_image0)
            np.save(os.path.join(depth_save_dir, f'{scene_id:06d}_{0:06d}.npy'), depth_image0)
            print(f'{scene_id:06d}_{0:06d} RGBD image saved')
            # for img1
            cv2.imwrite(os.path.join(rgb_save_dir, f'{scene_id:06d}_{1:06d}.png'), color_image1)
            np.save(os.path.join(depth_save_dir, f'{scene_id:06d}_{1:06d}.npy'), depth_image1)
            print(f'{scene_id:06d}_{1:06d} RGBD image saved')
            # for img2
            cv2.imwrite(os.path.join(rgb_save_dir, f'{scene_id:06d}_{2:06d}.png'), color_image2)
            np.save(os.path.join(depth_save_dir, f'{scene_id:06d}_{2:06d}.npy'), depth_image2)
            print(f'{scene_id:06d}_{2:06d} RGBD image saved')
            print('==========================================')
            scene_id += 1
        elif key == ord('q'):
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
                       depth_mode=DepthMode.WFOV_UNBINNED,
                       camera_fps=FPS.FPS_15,
                       color_format=ImageFormat.COLOR_BGRA32),
                  device_id=0,
                  thread_safe=False)
    k4a_1 = PyK4A(Config(color_resolution=ColorResolution.RES_1080P,
                       depth_mode=DepthMode.WFOV_UNBINNED,
                       camera_fps=FPS.FPS_15,
                       color_format=ImageFormat.COLOR_BGRA32),
                  device_id=1,
                  thread_safe=False)
    k4a_2 = PyK4A(Config(color_resolution=ColorResolution.RES_1080P,
                       depth_mode=DepthMode.WFOV_UNBINNED,
                       camera_fps=FPS.FPS_15,
                       color_format=ImageFormat.COLOR_BGRA32),
                  device_id=2,
                  thread_safe=False)
    k4a_0.start()
    k4a_1.start()
    k4a_2.start()
    
    print("Press 's' to save the rgb-d image and 'q' to quit")
    capture_rgbd(k4a_0, k4a_1, k4a_2, args)