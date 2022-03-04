
import pyautogui

last_position = (None,None)
last_dir = ''

#Think about using audio imput to use controls instead of visual imputs.

def keypress():
    ''' 
    Choose any four keys that a user can press to control the game.
    Update this doc string with your choices. 
    '''

    #imports keyboard library
    import keyboard

    #loops through and changes keys from arrow keys to letter keys
    while not (keyboard.is_pressed("esc")):
        if keyboard.is_pressed("y"):
            pyautogui.press('up')

        if keyboard.is_pressed("g"):
            pyautogui.press('left')

        if keyboard.is_pressed("h"):
            pyautogui.press('down')

        if keyboard.is_pressed("j"):
            pyautogui.press('right')


def trackpad_mouse():
    ''' 
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
    '''

    from pynput import mouse

    def on_move(x, y):
        
        global last_position
        global last_dir
        threshold = 100
        last_x, last_y = last_position

        #updates last position with currrent position
        if last_x == None or last_y == None:
            last_position = x, y
        else:
            #if the trackpad moves further than the threshold set direction to corresponting input
            if abs(last_x - x) >= threshold:
                if last_x - x < 0:
                    if last_dir != 'right':
                        pyautogui.press('right')
                        last_dir = 'right'
                        last_position = x, y
                else:
                    if last_dir != 'left':
                        pyautogui.press('left')
                        last_dir = 'left'
                        last_position = x, y
            
            if abs(last_y - y) >= threshold:
                if last_y - y < 0:
                    if last_dir != 'down':
                        pyautogui.press('down')
                        last_dir = "down"
                        last_position = x, y
                else:
                    if last_dir != 'up':
                        pyautogui.press('up')
                        last_dir = "up"
                        last_position = x, y
            
    #if finger motion detected, on_move function is called
    with mouse.Listener(on_move=on_move) as listener:
        listener.join() 

def color_tracker():
    ''' 
    Control the game by tracking a specific hue of color on front camera directionally.
    '''

    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw

    # ISOLATES GREEN/YELLOW COLOR FRAMES
    colorLower = (29, 86, 6)
    colorUpper = (64, 255, 255)

    # set the limit for the number of frames to store and the number that have seen direction change
    buffer = 20
    pts = deque(maxlen = buffer)

    # store the direction and number of frames with direction change
    num_frames = 0
    (dX, dY) = (0, 0)
    direction = ''
    global last_dir

    #Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()

    
    while True:
        #creates new frame
        frame = vs.read()
        frame_flip = cv2.flip(frame,1)
        resized = imutils.resize(frame_flip, width = 600)
        blurred = cv2.GaussianBlur(resized, (5,5), 0)
        final_frame = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        #isolates colored objects
        mask1 = cv2.inRange(final_frame, colorLower, colorUpper)
        mask2 = cv2.erode(mask1, None, iterations = 2)
        mask3 = cv2.dilate(mask2, None, iterations = 2)

        #creates a new contour of object
        contours, hierarchy = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #finding center of object 
        center = None
        if len(contours) > 0:
            largest_contour = max(contours, key = cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            M = cv2.moments(largest_contour)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            if radius > 10:
                cv2.circle(resized, (int(x), int(y)), int(radius), (0,255,255), 2)
                cv2.circle(resized, center, 5, (0,255,255), -1)

                pts.appendleft(center)

        #if colored object moves further than the threshold then set corresponding direction accordingly 
        if num_frames > 10 and len(pts) > 10:
            dX, dY = ( pts[0][0]-pts[9][0], (pts[0][1]-pts[9][1] ))
            threshold = 100

            if abs(dX) >= threshold:
                if  dX < 0:
                    direction = 'left'
                else:
                    direction = 'right'
            elif abs(dY) >= threshold:
                if  dY < 0:
                    direction = 'up'
                else:
                    direction = 'down'

            #displays directions on frame
            cv2.putText(resized, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        #setting controls
        if last_dir != 'right' and direction == 'right':
            #pyautogui.press('right')
            print("right")
            last_dir = 'right'
        elif last_dir != 'left' and direction == 'left':
            #pyautogui.press('left')
            print("left")
            last_dir = 'left'
        elif last_dir != 'up' and direction == 'up':
            #pyautogui.press('up')
            print('up')
            last_dir = 'up'
        elif last_dir != 'down' and direction == 'down':
            #pyautogui.press('down')
            print('down')
            last_dir = 'down'

        cv2.imshow('Game Control Window', resized)
        cv2.waitKey(1)
        num_frames += 1
       



def finger_tracking():
    ''' 
    Control the game by tracking finger placements on hand and assigning directions to specific number of fingers held up.
    '''

    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp

    ##Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()

    #sets accuracy for hand tracking
    my_hand = mp.solutions.hands
    accuracy = my_hand.Hands(static_image_mode=False,
                     max_num_hands=1,
                     min_detection_confidence=0.5,
                     min_tracking_confidence=0.5)

    to_draw = mp.solutions.drawing_utils
    direction = ''
    global last_dir

    while True:
        #creates new frame 
        frame = vs.read()
        frame_flip = cv2.flip(frame,1)
        resized = imutils.resize(frame_flip, width = 600)
        final_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        # getting results from processing image for our hand
        results = accuracy.process(final_frame)

        #creates new variables to track number of fingers and landmarks on the hand 
        num_fingers = 0
        landmarkList = []

        #iterates through landmarks and adds to landmark list
        if results.multi_hand_landmarks:
            for hand_item in results.multi_hand_landmarks:
                
                for id, lm in enumerate(hand_item.landmark):
                    (height, width, third) = final_frame.shape
                    new_x = int(lm.x * width)
                    new_y = int(lm.y * height)
                    center = new_x, new_y
                    cv2.circle(resized, center, 3, (255,0,255), cv2.FILLED)
                    landmarkList.append((id, new_x, new_y))
                
                to_draw.draw_landmarks(resized, hand_item, my_hand.HAND_CONNECTIONS)

        #counts number of fingers in frame and sets directions accordingly 
        if len(landmarkList) > 0:
            if landmarkList[4][1] < landmarkList[3][1]:
                num_fingers += 1
            if landmarkList[8][2] < landmarkList[6][2]:
                num_fingers += 1
            if landmarkList[12][2] < landmarkList[10][2]:
                num_fingers += 1
            if landmarkList[16][2] < landmarkList[14][2]:
                num_fingers += 1
            if landmarkList[20][2] < landmarkList[18][2]:
                num_fingers += 1
            
            #sets directions 
            if num_fingers == 1:
                direction = 'up'
            elif num_fingers == 2:
                direction = 'right'
            elif num_fingers == 3:
                direction = 'down'
            elif num_fingers == 5 or num_fingers == 4:
                direction = 'left'
        
        #setting controls
        if last_dir != 'right' and direction == 'right':
            #pyautogui.press('right')
            print("right")
            last_dir = 'right'
        elif last_dir != 'left' and direction == 'left':
            #pyautogui.press('left')
            print("left")
            last_dir = 'left'
        elif last_dir != 'up' and direction == 'up':
            #pyautogui.press('up')
            print('up')
            last_dir = 'up'
        elif last_dir != 'down' and direction == 'down':
            #pyautogui.press('down')
            print('down')
            last_dir = 'down'

        cv2.putText(resized,str(int(num_fingers)),(10,70),cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        cv2.imshow("Image", resized)
        cv2.waitKey(1)



def unique_control():
    ''' 
    Control the game by tracking fist across the camera corresponding to the direction of the fist motion.
    '''

    import cv2
    import imutils
    import numpy as np
    import time
    import multithreaded_webcam as mw
    import mediapipe as mp

    ##Sleep for 2 seconds to let camera initialize properly
    time.sleep(2)
    #Start video capture
    vs = mw.WebcamVideoStream().start()

    #sets hand accuracy 
    my_hand = mp.solutions.hands
    accuracy = my_hand.Hands(static_image_mode=False,
                     max_num_hands=1,
                     min_detection_confidence=0.5,
                     min_tracking_confidence=0.5)

    to_draw = mp.solutions.drawing_utils

    #creates position and directions variables
    direction = ''
    global last_dir
    global last_position
    last_position = (0,0)
    (dX, dY) = (0, 0)

    while True:
        #creates new frames
        frame = vs.read()
        frame_flip = cv2.flip(frame,1)
        resized = imutils.resize(frame_flip, width = 600)
        final_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        # getting results from processing image for our hand
        results = accuracy.process(final_frame)

        #creates landmark list
        landmarkList = []

         #iterates through landmarks and adds to landmark list
        if results.multi_hand_landmarks:
            for hand_item in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_item.landmark):
                    (height, width, third) = final_frame.shape
                    new_x = int(lm.x * width)
                    new_y = int(lm.y * height)
                    center = new_x, new_y
                    cv2.circle(resized, center, 3, (255,0,255), cv2.FILLED)
                    thing = (id, new_x, new_y)
                    landmarkList.append(thing)
                
                to_draw.draw_landmarks(resized, hand_item, my_hand.HAND_CONNECTIONS)
        
        #calculates change in position and if threshold requirement met, directional inputs set 
        threshold = 100
        if len(landmarkList) > 0:
            (id, new_x, new_y) =  landmarkList[8]
            dX, dY = ( new_x - last_position[0], new_y - last_position[1])
            threshold = 100

            if abs(dX) >= threshold:
                if  dX < 0:
                    direction = 'left'
                else:
                    direction = 'right'
            elif abs(dY) >= threshold:
                if  dY < 0:
                    direction = 'up'
                else:
                    direction = 'down'

            #updates last position to curent position 
            last_position = (new_x, new_y)

            cv2.putText(resized, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        #setting controls
        if last_dir != 'right' and direction == 'right':
            #pyautogui.press('right')
            print("right")
            last_dir = 'right'
        elif last_dir != 'left' and direction == 'left':
            #pyautogui.press('left')
            print("left")
            last_dir = 'left'
        elif last_dir != 'up' and direction == 'up':
            #pyautogui.press('up')
            print('up')
            last_dir = 'up'
        elif last_dir != 'down' and direction == 'down':
            #pyautogui.press('down')
            print('down')
            last_dir = 'down'

        cv2.imshow('Game Control Window', resized)
        cv2.waitKey(1)
                                

def main():

    #prompts user to input number depending on which game controls they would like to use
    control_mode = input("How would you like to control the game? ")
    if control_mode == '1':
        keypress()
    elif control_mode == '2':
        trackpad_mouse()
    elif control_mode == '3':
        color_tracker()
    elif control_mode == '4':
        finger_tracking()
    elif control_mode == '5':
        unique_control()

if __name__ == '__main__':
	main()