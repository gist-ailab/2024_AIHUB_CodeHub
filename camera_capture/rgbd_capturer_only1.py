import cv2
import numpy as np
import os
import argparse

from pyk4a import Config, PyK4A, ColorResolution, DepthMode, ImageFormat, FPS

# this code is for capturing RGB and Depth images using py4ka and azure kinect camera
def capture_rgbd(args):
    scene_id = args.start_id
    rgb_save_dir = os.path.join(args.save_dir, 'rgb')
    depth_save_dir = os.path.join(args.save_dir, 'depth')
    cv2_window_name = 'rgbd - scene_id: '+ str(scene_id) + '  ' + 'S: Save / Q: Quit'
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
    image_id = 0
    
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
        print('showing camera {}'.format(image_id))
        if key == ord('s'):
            # save color image to the save directory with scene_id_000000.png
            # save depth image to teh save directory with scene_id_000000.npy
            # for img0
            cv2.imwrite(os.path.join(rgb_save_dir, f'{scene_id:06d}_{image_id:06d}.png'), color_image0)
            np.save(os.path.join(depth_save_dir, f'{scene_id:06d}_{image_id:06d}.npy'), depth_image0)
            print(f'{scene_id:06d}_{image_id:06d} RGBD image saved')
            image_id += 1
        if image_id == 3:
            print('capture done')
            print('==========================================')
            image_id = 0
            scene_id += 1
            # key = cv2.waitKey(1) & 0xFF
            # while True:
            #     if cam1_capture and cam2_capture:
            #         break
            #     k4a1 = PyK4A(Config(color_resolution=ColorResolution.RES_1080P,
            #                 depth_mode=DepthMode.WFOV_UNBINNED,
            #                 camera_fps=FPS.FPS_5,
            #                 color_format=ImageFormat.COLOR_BGRA32),
            #             device_id=1,
            #         #   thread_safe=False
            #             )
            #     k4a1.start()
            #     key = cv2.waitKey(1) & 0xFF
                
            #     capture1 = k4a1.get_capture()
            #     if capture1.color is not None and capture1.depth is not None:
            #         color_image1 = capture1.color[:, :, :3]
            #         depth_image1 = capture1.depth
            #     depth_vis1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image1, alpha=0.03), cv2.COLORMAP_JET)
            #     depth_vis1 = cv2.resize(depth_vis1, (1920, 1080))
            #     rgbd_img1 = np.hstack([color_image1, depth_vis1])
            #     cv2.imshow(cv2_window_name, rgbd_img1)
            #     print('showing camera 1')
                
                
            #     if key == ord('s'):
            #         cv2.imwrite(os.path.join(rgb_save_dir, f'{scene_id:06d}_{1:06d}.png'), color_image1)
            #         np.save(os.path.join(depth_save_dir, f'{scene_id:06d}_{1:06d}.npy'), depth_image1)
            #         print(f'{scene_id:06d}_{1:06d} RGBD image saved')
            #         k4a1.stop()
            #         cam1_capture = True
            #         while True:
            #             if cam2_capture:
            #                 break
            #             k4a2 = PyK4A(Config(color_resolution=ColorResolution.RES_1080P,
            #                         depth_mode=DepthMode.WFOV_UNBINNED,
            #                         camera_fps=FPS.FPS_5,
            #                         color_format=ImageFormat.COLOR_BGRA32),
            #                     device_id=2,
            #                 #   thread_safe=False
            #                     )
            #             k4a2.start()
            #             key = cv2.waitKey(1) & 0xFF
                        
            #             capture2 = k4a2.get_capture()
            #             if capture2.color is not None and capture2.depth is not None:
            #                 color_image2 = capture2.color[:, :, :3]
            #                 depth_image2 = capture2.depth
            #             depth_vis2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image2, alpha=0.03), cv2.COLORMAP_JET)
            #             depth_vis2 = cv2.resize(depth_vis2, (1920, 1080))
            #             rgbd_img2 = np.hstack([color_image2, depth_vis2])
            #             cv2.imshow(cv2_window_name, rgbd_img2)
            #             print('showing camera 2')
                        
            #             if key == ord('s'):
            #                 cv2.imwrite(os.path.join(rgb_save_dir, f'{scene_id:06d}_{2:06d}.png'), color_image2)
            #                 np.save(os.path.join(depth_save_dir, f'{scene_id:06d}_{2:06d}.npy'), depth_image2)
            #                 print(f'{scene_id:06d}_{2:06d} RGBD image saved')
            #                 print('==========================================')
            #                 scene_id += 1
            #                 k4a2.stop()
            #                 cam2_capture = True
            #             elif key == ord('q'):
            #                 break
            #     elif key == ord('q'):
            #         break
        elif key == ord('q'):
            break

        
    k4a0.stop()
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
    
    
    print("Press 's' to save the rgb-d image and 'q' to quit")
    capture_rgbd(args)