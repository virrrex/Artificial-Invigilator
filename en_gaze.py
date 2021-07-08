import cv2
import numpy as np
from time import time
import os


class EyeGaze:

    
    compression_factor = [cv2.IMWRITE_PNG_COMPRESSION, 10]
    def get_path(self):
        # get current working directory
        return os.getcwd()
        
    def detect(self):

        # Load the Haar-Cascade and
        # store Cascade to detect eyes from the same
        
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
        # Grab the reference to the webcam
        video_capture = cv2.VideoCapture(0)

        # Set the dimensions of the video-capture screen (for saving the video)
        video_capture.set(3, 640)
        video_capture.set(4, 480)

        # loading the modules necessary for saving the Video
        #fourcc = cv2.cv.CV_FOURCC(*'MJPG')
        fourcc=cv2.VideoWriter_fourcc(*'MJPG')
        video = cv2.VideoWriter(self.get_path() + "/eye_detection.avi", fourcc, 15, (640, 480))

        # A boolean variable which stores if the person was cheating in the frame
        cheat_bool = 0
        cheating_attempts = 0

        redundant_frames = 10

        # some of the starting frames would be redundant
        # as image retrieved from webcam would be adjusting to brightness in surroundings
        '''while redundant_frames:
            (captured, frames) = video_capture.read()
            redundant_frames -= 1'''

        while True:

            # Grab the current frame
            (captured, frame) = video_capture.read()

            # If no frame is grabbed, then the webcam-streaming has stopped
            if not captured:
                break

            # reduce the noise in image by blurring and the blurred image to
            # original image so as to subtract local mean color image.
            blurred = cv2.GaussianBlur(frame, (21, 21), 0)
            weight_frame = cv2.addWeighted(frame, 1.75, blurred, -0.5, 0)

            # Equalise histogram to improve the contrast (Removing glare)
            # - Need to convert it to YUV image
            yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])

            # reconvert the image to grayscale to be feeded to Clahe
            bgr_frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
            gray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)

            # again apply Contrast Limited Adaptive Histogram Equalisation
            # CLAHE can only work on grayscale images
            clahe = cv2.createCLAHE(clipLimit=40.0, tileGridSize=(8, 8))
            gray = clahe.apply(gray)

            # load the haar-cascade to get the region of interest i.e. eye_region
            eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

            # draw a rectangle around the eye_region - It is going to work as region of interest when detecting pupil
            for (x, y, width, height) in eyes:
                cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
                break

            # If no eye_region is found, that would mean that either the person's face is not
            # straightly oriented in front of webcam or he is cheating - In any case mark as suspicious
            if len(eyes) == 0:
                cheat_bool = 1

            else:
                # crop the right portion of the eyes to enable accurate detection of pupil,
                # blur that region again to reduce noise.
                gray_cropped_right = gray[eyes[0][1]: eyes[0][1] + eyes[0][3],
                                          eyes[0][0] + eyes[0][2] // 2: eyes[0][0] + eyes[0][2]]
                cv2.GaussianBlur(gray_cropped_right, (3, 3), 16)

                # use HoughCircles method to detect the circular shape in right part of eye (cropped earlier)
                #circles_right = cv2.HoughCircles(gray_cropped_right, cv2.cv.CV_HOUGH_GRADIENT,
                                                 #dp=5, minDist=60, param1=30, param2=10, minRadius=5, maxRadius=20)
                circles_right = cv2.HoughCircles(gray_cropped_right, cv2.HOUGH_GRADIENT,
                                                 dp=5, minDist=60, param1=30, param2=10, minRadius=5, maxRadius=20)

                try:
                    # find the pupil-positions corresponding to the circle region
                    pupil_position = np.uint16(np.around(circles_right))

                    # draw a small circle around the pupil-position
                    for (a, b, radius) in pupil_position[0]:
                        cv2.circle(frame, (a + x + width // 2, b + y), 2, (255, 0, 0), 2)

                except:
                    pass

            # If the user is found to be cheating, the corresponding images can be saved in the directory
            if cheat_bool == 1:
                cheating_attempts += 1
                path = self.get_path()

                if cheating_attempts % 3 == 0 :
                    cv2.imwrite(path + "/" + str(cheating_attempts//3) + ".png", frame, self.compression_factor)

                # Reset value of cheat_bool to catch further such instances - in case they happen
                cheat_bool = 0

            cv2.imshow("Image", frame)

            video.write(frame)

            # If 'q' key is pressed, exit the application
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                return True


if __name__ == "__main__":
    gaze = EyeGaze()
    gaze.detect()
