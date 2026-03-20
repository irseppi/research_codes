"""
Create a video from a sequence of JPG images.

This script reads JPG images from the 'step_wavefeild' directory,
determines the dimensions from the first image, and generates:
1. An AVI video file ('video_V1_Th.avi') at 20 fps 

"""
import cv2
import os

model = 'V1_Th'
image_folder = 'step_wavefeild'
video_name = f'video_{model}.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images.sort()  
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 20, (width, height))

for image in images:
	video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
print(f"Video '{video_name}' created successfully.")
