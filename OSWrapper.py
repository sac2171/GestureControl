import win32api, win32con


class OSWrapper:
    
    if sys.platform == 'win32':
        import win32api
        
        #win32api.
        x_mid = win32api.GetSystemMetrics(0) / 2
        y_mid = win32api.GetSystemMetrics(1) / 2
        set_mouse_position = win32api.SetCursorPosition(x_mid, y_mid)
    elif sys.platform == 'darwin':
        import Quartz.CoreGraphics, Quartz
        main_monitor = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
        x_mid = main_monitor.size.width / 2
        y_mid = main_monitor.size.height / 2
        set_mouse_position = Quartz.CoreGraphics.CGWarpMouseCursorPosition
