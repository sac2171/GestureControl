import time
import subprocess
import win32pdhutil
import win32con
import win32api

def killProcName(procname):
    """Kill a running process by name.  Kills first process with the given name."""
    try:
        win32pdhutil.GetPerformanceAttributes("Process", "ID Process", procname)
    except:
        pass

    pids = win32pdhutil.FindPerformanceAttributesByName(procname)

    # If _my_ pid in there, remove it!
    try:
        pids.remove(win32api.GetCurrentProcessId())
    except ValueError:
        pass

    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pids[0])
    win32api.TerminateProcess(handle, 0)
    win32api.CloseHandle(handle)


sp = subprocess.Popen('C:\Windows\System32\magnify.exe',shell=True)
print 'Opened subprocess'
time.sleep(3);
print 'closing magnifier'

killProcName('magnify')