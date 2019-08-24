# -*- coding:utf-8 -*-
import sys
import os
import oss2

import win32clipboard as wcb
import win32con
import winsound

from scriptConfiger import ScriptConfiger
def getConfig(name='syncClipboard'):
    sc = ScriptConfiger(section=name)
    if not sc.isSectionExists():
        sc.setKeyValue('key_id', 'xxx')
        sc.setKeyValue('key_secret', 'xxx')
        sc.setKeyValue('endpoint', 'xxx') # ['evernote', 'vscode']
        sc.setKeyValue('bucket_name', 'xxx') # ['blod', 'form']
        sc.setKeyValue('project_dir', 'syncClipboard')
        exit()
    return sc
conf = getConfig()

# 配置项
auth = oss2.Auth(conf.getValue('key_id'), conf.getValue('key_secret'))
bucket = oss2.Bucket(auth, conf.getValue('endpoint'), conf.getValue('bucket_name'))
fileConfig = 'config.txt' # 简化代码，云端和本地都用这个路径
# fileClipboard = 'syncClipboard\Clipboard'


# 将工作目录修改为当前代码的位置
curDir = os.path.dirname(sys.argv[0]) # sys.argv的第一个参数是代码文件的绝对\或与工作目录的相对路径
if curDir != "":
	os.chdir(curDir)
# print(os.getcwd())

# 创建当前脚本专用文件夹
projectDir = conf.getValue('project_dir')
if not os.path.exists(projectDir):
    os.mkdir(projectDir)


def isFileExists(objectName):
    """查询云端文件是否存在。
    
    Arguments:
        objectName {string} -- 云端的对象路径及名称
    
    Returns:
        bool -- 存在返回True，不存在返回False
    """
    exist = bucket.object_exists(objectName)
    if exist:
        return True
    else:
        return False

def uploadFromFile(objectName, filePath):
    """将文件上传到云端。
    
    Arguments:
        objectName {string} -- 云端的对象路径及名称
        filePath {string} -- 本地文件的路径及名称
    
    Returns:
        [type] -- 返回上传结果。比如，`result.status`是上传的HTTP状态码。
    """
    result = bucket.put_object_from_file(objectName, filePath) 
    return result
    
def downloadToFile(objectName, filePath):
    """从云端下载文件到本地，如果指定路径的文件存在会覆盖，不存在则新建。
    
    Arguments:
        objectName {string} -- 云端的对象路径及名称
        filePath {string} -- 本地文件的路径及名称
    """
    bucket.get_object_to_file(objectName, filePath)

def downloadToMemory(objectName):
    """从云端下载文件到内存中。此函数是功能尚未完善，目前只在config文件的读取中用到，未来可能弃用。
    
    Arguments:
        objectName {string} -- 云端的对象路径及名称
    
    Returns:
        string -- 文件的内容
    """
    res = bucket.get_object(objectName)
    return str(res.read(), 'utf-8')

def buildConfigFile(objType, objName):
    """构建config文件，config文件存储两个信息，分别是：剪贴板内容的类型、以及在云端的剪贴板数据位置。
    
    Arguments:
        objType {string} -- 剪贴板内容的类型，目前仅支持同步`string`和`png`两种类型
        objName {string} -- 云端的剪贴板数据位置
    """
    f = open(os.path.join(projectDir, fileConfig), 'w') # 以写模式打开文件，已有内容会被删除
    f.write('%s\n' % objType)
    f.write('%s' % objName)
    f.close()

def readConfig(configString):
    """从字符串中读取config信息。与buildConfigFile功能对应。
    
    Arguments:
        configString {string} -- config文件的内容字符串
    
    Returns:
        string, string -- 剪贴板内容的类型，剪贴板数据的位置
    """
    import re
    configString = re.sub('\r', '', configString)
    res = re.split('(.+)\n(.+)', configString)
    objType = res[1]
    objName = res[2]
    return objType, objName

def getClipboardDataType():
    """获取剪贴板内数据的类型，仅对`png`和`string`类型做同步，`other`类型不做处理。
    
    Returns:
        string -- 剪贴板数据的类型
    """
    if wcb.IsClipboardFormatAvailable(wcb.CF_BITMAP):
        return 'png'
    elif wcb.IsClipboardFormatAvailable(wcb.CF_TEXT):
        return 'string'
    else:
        return 'other'

def saveClipboardImg():
    """将剪贴板中的图片保存成文件。文件默认为项目目录中的`\\data.png`。
    
    Returns:
        string -- 图片文件的路径
    """
    from PIL import ImageGrab
    im = ImageGrab.grabclipboard()
    path = projectDir+'/data.png'
    im.save(path, 'png')
    return path

def setClipboardImg(imgPath):
    """将图片写入到剪贴板当中。
    
    Arguments:
        imgPath {string} -- 图片文件的路径
    """
    from PIL import Image
    Image.open(imgPath).save(imgPath+'.bmp') # win的剪贴板仅支持bmp格式
    from ctypes import windll
    aString = windll.user32.LoadImageW(0, imgPath+'.bmp', win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
    # print(aString)
    if aString != 0: # 由于图片编码问题 图片载入失败的话 aString 就等于0 
        wcb.OpenClipboard()
        wcb.EmptyClipboard()
        wcb.SetClipboardData(win32con.CF_BITMAP, aString)
        wcb.CloseClipboard()

def saveClipboardString():
    """将剪贴板中的字符串保存成文件。文件默认为项目目录中的`\\data.txt`。
    
    Returns:
        string -- 文件的路径
    """
    wcb.OpenClipboard()
    text = wcb.GetClipboardData()
    wcb.CloseClipboard()
    path = '%s/%s' % (projectDir, 'data.txt')
    f = open(path, 'w', encoding='utf-8') # 以写模式打开文件，已有内容会被删除
    text = text.replace('\r', '')
    f.write('%s' % text)
    f.close()
    return path

def setClipboardString(string):
    """将字符串写入到剪贴板当中。
    
    Arguments:
        string {string} -- 要写入的字符串
    """
    wcb.OpenClipboard()
    wcb.EmptyClipboard()
    wcb.SetClipboardText(string)
    wcb.CloseClipboard()



if __name__ == "__main__":

    # 配置文件的路径
    configPath = '%s/%s' % (projectDir, fileConfig)

    # isUpload = False
    # if not isUpload:
    if len(sys.argv) == 1: # 单参数，默认功能是下载云端剪贴板
        print('Download Func')

        # 首先检查云端是否有内容
        if not isFileExists(configPath):
            print('Error: File not exist!')
            exit()
        # 下载配置
        configStr = downloadToMemory(configPath)

        objType, objName = readConfig(configStr)
        print(objType, objName)

        # 根据图片和字符串分别处理
        if objType == 'png':
            downloadToFile(objName, objName)
            setClipboardImg(objName)

        elif objType == 'string':
            downloadToFile(objName, objName)
            f = open(objName, 'r', encoding='utf-8')
            string = f.read()           
            setClipboardString(string)
            f.close()
        else:
            pass

    # elif isUpload:
    elif len(sys.argv) == 2: # 两个参数，默认功能是上传剪贴板内容传到云端
        
        print('Upload Func')
        objType = getClipboardDataType()
        print(objType)

        if objType == 'png':
            imgPath = saveClipboardImg()
            buildConfigFile(objType, imgPath)
            uploadFromFile(configPath, configPath)
            uploadFromFile(imgPath, imgPath)

        elif objType == 'string':
            strPath = saveClipboardString()
            buildConfigFile(objType, strPath)
            uploadFromFile(configPath, configPath)
            uploadFromFile(strPath, strPath)

        else:
            pass
    
    # 完成时播放音效
    winsound.PlaySound('tone_beep.wav', winsound.SND_FILENAME) # 自定义铃声在电脑未播放音频的时候会出现听不见的现象
