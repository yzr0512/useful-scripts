# -*- coding:utf-8 -*-
import sys
import os
import oss2
import util
# from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPasteboardTypeString
# import pasteboard

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
paramFile = 'param.txt' # 简化代码，云端和本地都用这个路径
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
    """从云端下载文件到内存中。此函数是功能尚未完善，目前只在param文件的读取中用到，未来可能弃用。
    
    Arguments:
        objectName {string} -- 云端的对象路径及名称
    
    Returns:
        string -- 文件的内容
    """
    res = bucket.get_object(objectName)
    return str(res.read(), 'utf-8')

def buildParamFile(objType, objName):
    """构建内部参数文件，该文件存储两个信息，分别是：剪贴板内容的类型、以及在云端的剪贴板数据位置。
    
    Arguments:
        objType {string} -- 剪贴板内容的类型，目前仅支持同步`string`和`png`两种类型
        objName {string} -- 云端的剪贴板数据位置
    """
    f = open(os.path.join(projectDir, paramFile), 'w') # 以写模式打开文件，已有内容会被删除
    f.write('%s\n' % objType)
    f.write('%s' % objName)
    f.close()

def readParam(paramString):
    """从字符串中读取内部参数信息。与buildParamFile功能对应。
    
    Arguments:
        paramString {string} -- param文件的内容字符串
    
    Returns:
        string, string -- 剪贴板内容的类型，剪贴板数据的位置
    """
    import re
    paramString = re.sub('\r', '', paramString)
    res = re.split('(.+)\n(.+)', paramString)
    objType = res[1]
    objName = res[2]
    return objType, objName

def syncClipboard(func='download'):
    # 配置文件的路径
    paramPath = '%s/%s' % (projectDir, paramFile)

    if func == 'download':
        print('Download Func')

        # 首先检查云端是否有内容
        if not isFileExists(paramPath):
            print('Error: File not exist!')
            exit(2)

        # 下载同步参数
        paramStr = downloadToMemory(paramPath)
        objType, objName = readParam(paramStr)

        # 根据图片和字符串分别处理
        if objType == util.TYPE_PNG:
            downloadToFile(objName, objName)

            # setClipboardImg(objName)
            util.setClipboardData(util.TYPE_PNG, objName)

        elif objType == util.TYPE_STRING:
            downloadToFile(objName, objName)
            f = open(objName, 'r', encoding='utf-8')
            data = f.read()
            # setClipboardString(string)
            util.setClipboardData(util.TYPE_STRING, data)
            f.close()
        else:
            exit(2)
    elif func == 'upload':
        print('Upload Func')

        t, data = util.getClipboardData(projectDir)

        if t == util.TYPE_PNG:
            buildParamFile(t, data)
            uploadFromFile(paramPath, paramPath)
            uploadFromFile(data, data)

        elif t == util.TYPE_STRING:
            path = '%s/%s' % (projectDir, 'data.txt')
            f = open(path, 'w', encoding='utf-8') # 以写模式打开文件，已有内容会被删除
            f.write(data)
            f.close()

            buildParamFile(t, path)
            uploadFromFile(paramPath, paramPath)
            uploadFromFile(path, path)

        else:
            exit(2)       

if __name__ == "__main__":

    debugUpload = False #or True

    # # if not isUpload:
    if len(sys.argv) == 1 and not debugUpload: # 单参数，默认功能是下载云端剪贴板
        syncClipboard()

    elif debugUpload or len(sys.argv) == 2: # 两个参数，默认功能是上传剪贴板内容传到云端
        syncClipboard('upload')
    
    
    print("Finished.")
