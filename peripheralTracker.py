from datetime import datetime
from pynput.mouse import Listener as MouseListener
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener as KeyboardListener
import pyautogui
import subprocess
import threading
import sys
import wmi
import os
from time import sleep

fileObj = None
allow_logging = False

def logData(data):
    if allow_logging:
        dateTime = getDateTime()
        info = dateTime+"   "+data+"\n"
        print(info)
        fileObj.write(info)


def getDateTime():
    return str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


def on_key_press(key):
    logData("Key pressed: {0}".format(key))
    if key == "Key.esc":
        sys.exit()


def on_key_release(key):
    logData("Key released: {0}".format(key))


def on_mouse_move(x, y):
    logData("Mouse Coords ({0}, {1})".format(x, y))


def on_mouse_click(x, y, button, pressed):
    if pressed:
        logData('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        logData('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))


def on_mouse_scroll(x, y, dx, dy):
    logData('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


def check_processes():
    global allow_logging

    try:
        battle_net = False
        modern_warfare = False

        while(True):
            sleep(1)
            
            procList =  subprocess.check_output("tasklist", shell=True).decode("utf-8");
            if "Battle.net" in procList:
                battle_net = True
            if "ModernWarfare" in procList:
                modern_warfare = True

            if (battle_net & modern_warfare):
                print("Anti Cheating Software Activated")
                allow_logging = True
            else:
                allow_logging = False
                print("Do Not Log")
    except Exception as e:
        print(e)


def move_mouse_pyautogui():
    pyautogui.FAILSAFE = False
    
    #sleep(10)
    screen_x = pyautogui.size()[0]
    screen_y = pyautogui.size()[1]

    pyautogui.moveTo(50, 50, duration = 0)
    
    middle_x = int(screen_x/2)
    middle_y = int(screen_y/2)

    while(True):
        pyautogui.moveTo(50, middle_y, duration = 3)
        pyautogui.moveTo(middle_x, middle_y, duration = 3)
        pyautogui.moveTo(middle_x, 50, duration = 3)
        pyautogui.moveTo(50, 50, duration = 3)

    pass


def move_mouse():
    sleep(2)
    while(True):
        mouse = Controller()
        mouse.position = (100, 100)
        sleep(1)
        mouse.position = (100, 500)
        sleep(1)
        mouse.position = (500, 500)
        sleep(1)
        mouse.position = (500, 100)
        sleep(1)


def monitorPeripherals():
    global fileObj

    #proc_thread = threading.Thread(target=check_processes)
    #proc_thread.start()

    fileObj = open("peripheralData.txt", "a")

    keyboard_listener = KeyboardListener(on_press=on_key_press, on_release=on_key_release)
    mouse_listener = MouseListener(on_move=on_mouse_move, on_click=on_mouse_click, on_scroll=on_mouse_scroll)

    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()




def main():
    
    global allow_logging
    
    allow_logging = True

    peripheral_thread = threading.Thread(target=monitorPeripherals)
    peripheral_thread.start()
    
    #mouse_thread = threading.Thread(target=move_mouse)
    #mouse_thread.start()


if __name__ == "__main__":
    main()

#python C:\Users\ravin\Desktop\Ravi\CMU\Research\GameSecurityResearch\peripheralTracker.py
