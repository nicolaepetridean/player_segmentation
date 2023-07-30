# importing libraries
import os
import cv2 
from PIL import Image 
  
# Video Generating function
def generate_video(input_folder = '/kaggle/working/frames', video_name = 'mygeneratedvideo.avi'):
    image_folder = '/kaggle/working/frames' # make sure to use your folder
    video_name = 'mygeneratedvideo.avi'
      
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]
     
    # Array images should only consider the image files ignoring others if any
    print(images) 
  
    frame = cv2.imread(os.path.join(image_folder, images[0]))
  
    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape  
  
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 10, (width, height)) 
  
    # Appending the images to the video one by one
    # for image in images: 
    #     video.write(cv2.imread(os.path.join(image_folder, image))) 
    
    for sec in range(34):
        for frame in range(10):
            img = cv2.imread(f'/kaggle/working/frames/{sec}_{frame}.jpg')
            video.write(img)
      
    # Deallocating memories taken for window creation
    # cv2.destroyAllWindows() 
    video.release()  # releasing the video generated
  

if __name__ == "__main__":
    # Calling the generate_video function
    generate_video()
