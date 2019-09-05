import platform
import sys

# Data type
TYPE_OTHER = 0
TYPE_PNG = 1
TYPE_STRING = 2

# 'Windows' or 'macOS'
OS_WINDOWS = 1
OS_MAC = 2
OS_CUR = platform.system()
if OS_CUR == 'Darwin':
    OS_CUR = OS_MAC
elif OS_CUR == 'Windows':
    OS_CUR = OS_WINDOWS
else:
    print('Your operating system is not supported.')
    exit(1)

if OS_CUR == OS_WINDOWS:
    import win32clipboard as wcb


def getClipboardDataType():

    if OS_CUR == OS_WINDOWS:
        if wcb.IsClipboardFormatAvailable(wcb.CF_BITMAP):
            return TYPE_PNG
        elif wcb.IsClipboardFormatAvailable(wcb.CF_TEXT):
            return TYPE_STRING
        else:
            return TYPE_OTHER
    elif OS_CUR == OS_MAC:
        pass

print(getClipboardDataType())


def getClipboardData():
    t = getClipboardDataType()
    if OS_CUR == OS_WINDOWS:
        if t == TYPE_STRING:
            wcb.OpenClipboard()
            data = wcb.GetClipboardData(wcb.CF_TEXT)
            wcb.CloseClipboard()
            # print(data)
            data = str(data, 'gbk')
        elif t == TYPE_PNG:
            # import win32ui
                       
            # wcb.OpenClipboard()
            # data = wcb.GetClipboardData(wcb.CF_BITMAP) # 这是个句柄，不知道怎么用
            # wcb.CloseClipboard()

            # dc = win32ui.CreateDCFromHandle(data)
            
            # bmp = win32ui.CreateBitmapFromHandle(data)
            # # print(dir(bmp))
            # bmp.SaveBitmapFile(dc, '123.png')
            
            from PIL import ImageGrab
            data = ImageGrab.grabclipboard()
            # im.save('123.png', 'png')
        else:
            exit(2)
    elif OS_CUR == OS_MAC:
        pass
    
    return t, data

getClipboardData()


def setClipboardData(t, data):

    if OS_CUR == OS_WINDOWS:
        if t == TYPE_PNG:
            # from PIL import Image
            # import win32con
            # Image.open(data).save(data+'.bmp') # win的剪贴板仅支持bmp格式
            # from ctypes import windll
            # aString = windll.user32.LoadImageW(0, data+'.bmp', win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
            # # print(aString)
            # if aString != 0: # 由于图片编码问题 图片载入失败的话 aString 就等于0 
            #     wcb.OpenClipboard()
            #     wcb.EmptyClipboard()
            #     wcb.SetClipboardData(win32con.CF_BITMAP, aString)
            #     wcb.CloseClipboard()
            pass
        elif t == TYPE_STRING:
            wcb.OpenClipboard()
            wcb.EmptyClipboard()
            wcb.SetClipboardText(data)
            wcb.CloseClipboard()
        pass
    elif OS_CUR == OS_MAC:
        pass