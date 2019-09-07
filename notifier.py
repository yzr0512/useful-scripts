import platform
import sys

def notifier(title, msg):
    s = platform.system()
    if s == 'Windows':
        # Windows
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, msg, threaded=True, duration=3)
    elif s == 'Darwin':
        # macOS
        from subprocess import call
        cmd = 'display notification \"%s\" with title \"%s\"' % (msg, title)
        call(["osascript", "-e", cmd])


if __name__ == "__main__":
    # print(sys.argv)
    if len(sys.argv) >= 3:
        title = sys.argv[1]
        msg = sys.argv[2]
    else:
        title = 'Title'
        msg = 'Notification demo'

    notifier(title, msg)