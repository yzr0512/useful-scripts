import platform
import sys

# Data type
TYPE_OTHER = 'other'
TYPE_PNG = 'png'
TYPE_STRING = 'string'

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

# 根据平台导入相应的库
if OS_CUR == OS_WINDOWS:
    import win32clipboard as wcb
elif OS_CUR == OS_MAC:
    from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPasteboardTypeString
    import pasteboard


def getClipboardDataType():
    """获取剪贴板数据的类型。支持的类型为`png` `string` `other`。
    
    Returns:
        string -- 类型名称。
    """
    if OS_CUR == OS_WINDOWS:
        if wcb.IsClipboardFormatAvailable(wcb.CF_BITMAP):
            return TYPE_PNG
        elif wcb.IsClipboardFormatAvailable(wcb.CF_TEXT):
            return TYPE_STRING
        else:
            return TYPE_OTHER
        
    elif OS_CUR == OS_MAC:
        pb = NSPasteboard.generalPasteboard()
        data_type = pb.types()
        if NSPasteboardTypePNG in data_type:
            return TYPE_PNG
        elif NSPasteboardTypeString in data_type:
            return TYPE_STRING
        else:
            return TYPE_OTHER

# print(getClipboardDataType())


def getClipboardData(projDir="."):
    """获取剪贴板的内容。
    
    Keyword Arguments:
        projectDir {str} -- 项目路径。当剪贴板数据是图片时，会将图片保存到此路径中。 (default: {"."})
    
    Returns:
        string, string -- 第一返回值是剪贴板数据的类型。第二返回值是剪贴板的数据，若类型为图片则返回值为路径。
    """
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
            img = ImageGrab.grabclipboard()
            data = '%s/%s' % (projDir, 'data.png')
            img.save(data, 'png')

        else:
            exit(2)
        
    elif OS_CUR == OS_MAC:
        if t == TYPE_STRING:
            pb = NSPasteboard.generalPasteboard()
            data = pb.dataForType_(NSPasteboardTypeString)
            data = str(data, 'utf-8')
            
        elif t == TYPE_PNG:
            pb = NSPasteboard.generalPasteboard()
            img = pb.dataForType_(NSPasteboardTypePNG)
            data = '%s/%s' % (projDir, 'data.png')
            img.writeToFile_atomically_(data, False)    # 将剪切板数据保存为文件

        else:
            exit(2)      
    
    return t, data

# t, data = getClipboardData()
# print("t:", t)
# print("data:", data)

def setClipboardData(t, data):
    """向剪贴板写入数据。
    
    Arguments:
        t {string} -- 要写入数据的类型。
        data {string} -- 要写入的数据。若类型为图片则此参数为图片的路径。
    """
    if OS_CUR == OS_WINDOWS:
        if t == TYPE_PNG:
            from PIL import Image
            Image.open(data).save(data+'.bmp') # win的剪贴板仅支持bmp格式
            from ctypes import windll
            aString = windll.user32.LoadImageW(0, data+'.bmp', win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
            # print(aString)
            if aString != 0: # 由于图片编码问题 图片载入失败的话 aString 就等于0 
                wcb.OpenClipboard()
                wcb.EmptyClipboard()
                wcb.SetClipboardData(win32con.CF_BITMAP, aString)
                wcb.CloseClipboard()
            
        elif t == TYPE_STRING:
            wcb.OpenClipboard()
            wcb.EmptyClipboard()
            wcb.SetClipboardText(data)
            wcb.CloseClipboard()

        else:
            exit(2)
        
    elif OS_CUR == OS_MAC:
        if t == TYPE_PNG:
            f = open(data, 'rb')
            img = f.read()
            pb = pasteboard.Pasteboard()
            pb.set_contents(img, pasteboard.PNG)
            f.close()

        elif t == TYPE_STRING:
            pb = pasteboard.Pasteboard()
            pb.set_contents(data)

        else:
            exit(2)




def testFunc():
    setClipboardData(TYPE_STRING, '这是测试文本。')
    t, data = getClipboardData()
    print("type:", t)
    print("data:", data)

    # setClipboardData(TYPE_PNG, 'syncClipboard/data.png')

if __name__ == "__main__":
    testFunc()