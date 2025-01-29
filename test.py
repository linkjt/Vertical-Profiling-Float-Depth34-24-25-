import pyautogui
import matplotlib.pyplot as plt

from AppKit import NSApplication, NSApp, NSWorkspace
from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo


# Your plotting code here
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()


workspace = NSWorkspace.sharedWorkspace()
activeApps = workspace.runningApplications()
for app in activeApps:
    if app.isActive():
        options = kCGWindowListOptionOnScreenOnly
        windowList = CGWindowListCopyWindowInfo(options,
                                                kCGNullWindowID)
        for window in windowList:
            if window['kCGWindowOwnerName'] == app.localizedName():
                print(window.getKeys_)
                break
        break
# Maximize the window after it opens
pyautogui.hotkey('command', 'option', 'f') 
