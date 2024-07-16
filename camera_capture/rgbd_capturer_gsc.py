import cv2
import numpy as np
import os
import argparse

from pyk4a import Config, PyK4A, ColorResolution, DepthMode, ImageFormat, FPS

# this code is for capturing RGB and Depth images using py4ka and azure kinect camera
def capture_rgbd(args):
    group_id = args.group_id
    # scene_id = args.scene_id
    cut_id = args.cut_id
    
    # check if the save directory exists (group_id)
    if not os.path.exists(os.path.join(args.save_dir, 'rgb', f'group_{group_id:06d}')):
        os.makedirs(os.path.join(args.save_dir, 'rgb', f'group_{group_id:06d}'))
    if not os.path.exists(os.path.join(args.save_dir, 'depth', f'group_{group_id:06d}')):
        os.makedirs(os.path.join(args.save_dir, 'depth', f'group_{group_id:06d}'))

    rgb_save_dir = os.path.join(args.save_dir, 'rgb')
    depth_save_dir = os.path.join(args.save_dir, 'depth')

    cv2_window_name = 'rgbd - group_id: ' + str(group_id) + ' cut_id: '+ str(cut_id) + '  ' + 'C: Save & Next Cut / X: Previous Cut / G: Next Group / Q: Quit'
    k4a0 = PyK4A(Config(color_resolution=ColorResolution.RES_1080P,
                       depth_mode=DepthMode.WFOV_UNBINNED,
                       camera_fps=FPS.FPS_5,
                       color_format=ImageFormat.COLOR_BGRA32),
                       device_id=0,
                    #   thread_safe=False
                )
    k4a0.start()
    
    cv2.namedWindow(cv2_window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(cv2_window_name, 1280, 720)
    # image_id = 0
    
    while True:
        # for camera 0
        cam1_capture = False
        cam2_capture = False
        key = cv2.waitKey(1) & 0xFF
        
        capture0 = k4a0.get_capture()
        if capture0.color is not None and capture0.depth is not None:
            color_image0 = capture0.color[:, :, :3] # BGR format
            depth_image0 = capture0.depth
        depth_vis0 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image0, alpha=0.03), cv2.COLORMAP_JET)
        depth_vis0 = cv2.resize(depth_vis0, (1920, 1080))
        rgbd_img0 = np.hstack([color_image0, depth_vis0])
        cv2.imshow(cv2_window_name, rgbd_img0)
        print('group {} / cut {}'.format(group_id, cut_id))
        
        # Save RGBD Image & Move to Next Cut
        if key == ord('c'):
            # save color image to the save directory with scene_id_000000.png
            # save depth image to teh save directory with scene_id_000000.npy
            # for img0
            cv2.imwrite(os.path.join(rgb_save_dir, f'group_{group_id:06d}/{cut_id:06d}.png'), color_image0)
            np.save(os.path.join(depth_save_dir, f'group_{group_id:06d}/{cut_id:06d}.npy'), depth_image0)
            print(f'{group_id:06d}_{cut_id:06d} RGBD image saved')
            cut_id += 1
        
        # Go Back to Previous Cut
        elif key == ord('x'):
            if cut_id > 0:
                cut_id -= 1
            else:
                print("Cut id is 0!! Can't go back to previous cut")
            
        # Move to Next Group
        elif key == ord('g'):
            cut_id = 0
            scene_id = 0
            group_id += 1
            # check if the save directory exists (group_id)
            if not os.path.exists(os.path.join(args.save_dir, 'rgb', f'group_{group_id:06d}')):
                os.makedirs(os.path.join(args.save_dir, 'rgb', f'group_{group_id:06d}'))
            if not os.path.exists(os.path.join(args.save_dir, 'depth', f'group_{group_id:06d}')):
                os.makedirs(os.path.join(args.save_dir, 'depth', f'group_{group_id:06d}'))
            
        # Quit
        elif key == ord('q'):
            break

        
    k4a0.stop()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--group_id', type=int, default=0)
    argparser.add_argument('--cut_id', type=int, default=0)
    
    argparser.add_argument('--save_dir', type=str, default='data/home') # 'data/home' or 'data/factory'
    args = argparser.parse_args()

    # check if the save directory exists
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
        os.makedirs(os.path.join(args.save_dir, 'rgb'))
        os.makedirs(os.path.join(args.save_dir, 'depth'))
    
    
    print("Press 'c' to save the rgb-d image and 'q' to quit")
    capture_rgbd(args)