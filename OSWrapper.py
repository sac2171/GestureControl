import sys
import win32api, win32con

def moveMouse( x, y):
    win32api.SetCursorPos((x,y))
    
def click( x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 1, 0 )

def scrollMouse(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x , y, 1, 0)

def getResolution():
    x_screen = win32api.GetSystemMetrics(0)
    y_screen = win32api.GetSystemMetrics(1)
    return x_screen, y_screen 

#     elif sys.platform == 'darwin':
#         import Quartz.CoreGraphics, Quartz
#         main_monitor = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
#         x_mid = main_monitor.size.width / 2
#         y_mid = main_monitor.size.height / 2
#         set_mouse_position = Quartz.CoreGraphics.CGWarpMouseCursorPosition
