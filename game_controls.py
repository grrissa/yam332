import pyautogui
import keyboard

last_position = (None,None)
last_dir = ''

#Think about using audio imput to use controls instead of visual imputs.

def keypress():
    ''' 
    Choose any four keys that a user can press to control the game.
    Update this doc string with your choices. 
    '''

    while not (keyboard.is_pressed("esc")):
        if keyboard.is_pressed("y"):
            pyautogui.press('up')

        if keyboard.is_pressed("g"):
            pyautogui.press('left')

        if keyboard.is_pressed("h"):
            pyautogui.press('down')

        if keyboard.is_pressed("j"):
            pyautogui.press('right')


# FIX ME
def trackpad_mouse():
    ''' 
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
    '''

    from pynput import mouse

    def on_move(x, y):
        
        global last_position
        global last_dir
        threshold = 30
        last_x, last_y = last_position

        while not (keyboard.is_pressed("esc")):
            if last_x == None or last_y == None:
                last_position = x, y
            else:
                if abs(last_x - x) >= threshold:
                    if last_x - x < 0:
                        if last_dir != 'right':
                            #pyautogui.press('right')
                            print('right')
                            last_dir = 'right'
                            last_position = x, y
                    else:
                        if last_dir != 'left':
                            #pyautogui.press('left')
                            print("left")
                            last_dir = 'left'
                            last_position = x, y
                
                if abs(last_y - y) >= threshold:
                    if last_y - y < 0:
                        if last_dir != 'down':
                            #pyautogui.press('down')
                            print('down')
                            last_dir = "down"
                            last_position = x, y
                    else:
                        if last_dir != 'up':
                            #pyautogui.press('up')
                            print('up')
                            last_dir = "up"
                            last_position = x, y
        
  

    with mouse.Listener(on_move=on_move) as listener:
        listener.join() 

def color_tracker():
    import cv2
    import imutils
    import numpy as np
    from collections import deque
    import time
    import multithreaded_webcam as mw

    # You need to define HSV colour range MAKE CHANGE HERE
    colorLower = (90,65,53)
    colorUpper = (138,100,100)

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
        frame = vs.read()
        frame_flip = cv2.flip(frame,1)
        imutils.resize(frame_flip, width = 600)
        cv2.GaussianBlur(frame, (5,5), 0)
        cv2.cvtColor(frame_flip, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(frame_flip, colorLower, colorUpper)
        mask2 = cv2.erode(mask1, None, iterations = 2)
        mask3 = cv2.dilate(mask2, None, iterations = 2)

        list_of_points, item2 = cv2.findContours(mask3.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        center = None

        largest_contour = max(list_of_points, key = cv2.contourArea)
        item1, radius = cv2.minEnclosingCircle(largest_contour)
        M = cv2.moments(largest_contour)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        if radius > 10:
            pts.appendleft(radius)
            
        if num_frames > 10 and len(pts) > 10:
            dX, dY = ( pts[0][0]-pts[9][0], (pts[0][1]-pts[9][1] ))
            threshold = 95

            if dX >= threshold:
                if  dX < 0:
                    if last_dir != 'right':
                        direction = 'right'
                        last_dir = 'right'
                else:
                    if last_dir != 'left':
                        direction = 'left'
                        last_dir = 'left'
            elif dY >= threshold:
                if  dY < 0:
                    if last_dir != 'up':
                        direction = 'up'
                        last_dir = 'up'
                else:
                    if last_dir != 'down':
                        direction = 'down'
                        last_dir = 'up'

            cv2.putText(frame_flip, direction, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        if last_dir != 'right' and direction == 'right':
            #pyautogui.press('right')
            print("right")
            last_dir = 'right'
        if last_dir != 'left' and direction == 'left':
            #pyautogui.press('left')
            print("left")
            last_dir = 'left'
        if last_dir != 'up' and direction == 'up':
            #pyautogui.press('up')
            print('up')
            last_dir = 'up'
        if last_dir != 'down' and direction == 'down':
            #pyautogui.press('down')
            print('down')
            last_dir = 'down'

        cv2.imshow('Game Control Window', frame_flip)
        cv2.waitKey(1)
        num_frames += 1

        continue
        



def finger_tracking():
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

    # put your code here


def unique_control():
    # put your code here
    pass

def main():


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