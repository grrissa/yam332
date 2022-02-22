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



def trackpad_mouse():
    ''' 
    Control the game by moving the mouse/finger on trackpad left, right, up, or down. 
    '''

    from pynput import mouse

    def on_move(x, y):
        
        global last_position
        global last_dir
        threshold = 15
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
                    else:
                        if last_dir != 'left':
                            #pyautogui.press('left')
                            print("left")
                            last_dir = 'left'
                
                if abs(last_y - y) >= threshold:
                    if last_y - y < 0:
                        if last_dir != 'down':
                            #pyautogui.press('down')
                            print('down')
                            last_dir = "down"
                    else:
                        if last_dir != 'up':
                            #pyautogui.press('up')
                            print('up')
                            last_dir = "up"
        
  

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
    colorLower = None
    colorUpper = None

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
        # your code here
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
