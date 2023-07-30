
STRIDE = 0.1
MAX_IMAGE_SIZE = 1024

def get_frames_from_video(video_file, stride=1.0):
    """
    video_file - path to file
    stride - i.e 1.0 - extract frame every second, 0.5 - extract every 0.5 seconds
    return: list of images, list of frame times in seconds
    """
    video = cv2.VideoCapture(video_file)
    fps = video.get(cv2.CAP_PROP_FPS)
    i = 0.
    images = []
    frame_times = []

    while video.isOpened():
        ret, frame = video.read()
        if ret:
            images.append(frame)
            frame_times.append(i)
            i += stride
            video.set(1, round(i * fps))
        else:
            video.release()
            break
    return images, frame_times


def resize_if_necessary(image, max_size=1024):
    """
    if any spatial shape of image is greater 
    than max_size, resize image such that max. spatial shape = max_size,
    otherwise return original image
    """
    if max_size is None:
        return image
    height, width = image.shape[:2]
    if max([height, width]) > max_size:
        ratio = float(max_size / max([height, width]))
        image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)
    return image


def demo_generate_frames()
    sample_video = '../input/player-segmentation/Test.mp4'
    images, frame_times = get_frames_from_video(sample_video, STRIDE)
    images = [resize_if_necessary(image, MAX_IMAGE_SIZE) for image in images]

    return images


def generate_frames(input_path, save_path, stride, max_image_size):

    images, frame_times = get_frames_from_video(input_path, stride)
    images = [resize_if_necessary(image, max_image_size) for image in images]
    for image, frame_time in zip(images, frame_times):
        image_name = str(round(frame_time, 3)).replace(".", "_")
        ssave_path = os.path.join(save_path, "{}.jpg".format(image_name))
        print('saving:  ', ssave_path)
        cv2.imwrite(ssave_path, image)  


if __name__ == "__main__":
    sample_video = '../input/player-segmentation/Test.mp4'
    frame_save_path = "/kaggle/working/frames"

    generate_frames(sample_video, frame_save_path, STRIDE, MAX_IMAGE_SIZE)
