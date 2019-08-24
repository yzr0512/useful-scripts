import os
import sys
import requests
import json
import time


# https://blog.csdn.net/weixin_33910434/article/details/87474604
# 从PyObjC库的AppKit模块引用NSPasteboard主类，和PNG、TIFF的格式类
from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPasteboardTypeString
import pasteboard

from scriptConfiger import ScriptConfiger
def getConfig(name='uploadpic_mac'):
    sc = ScriptConfiger(section=name)
    if not sc.isSectionExists():
        sc.setKeyValue('pic_bed', 'aliyun') # smms, aliyun
        sc.setKeyValue('pic_save_dir', 'saved_pic')
        sc.setKeyValue('log_name', 'saved_pic/log.txt')
        sc.setKeyValue('sb_editor', 'vscode') # ['evernote', 'vscode']
        sc.setKeyValue('sb_style', 'form') # ['blod', 'form']

        sc.setKeyValue('key_id', 'xxx')
        sc.setKeyValue('key_secret', 'xxx')
        sc.setKeyValue('endpoint', 'xxx') # ['evernote', 'vscode']
        sc.setKeyValue('bucket_name', 'xxx') # ['blod', 'form']

        exit()
    return sc
conf = getConfig()

# 配置项
# -图床
pic_bed = conf.getValue('pic_bed')
# -扇贝
sb_editor = conf.getValue('sb_editor')
sb_style = conf.getValue('sb_style')

# 将工作目录修改为当前代码的位置
cur_dir = os.path.dirname(sys.argv[0]) # sys.argv的第一个参数是代码文件的绝对\或与工作目录的相对路径
if cur_dir != "":
	os.chdir(cur_dir)
# print(os.getcwd())

# 保存图片的文件夹名称（可修改）及路径，默认与代码所在的路径相同
pic_save_dir = conf.getValue('pic_save_dir')
if not os.path.exists(pic_save_dir):
    os.mkdir(pic_save_dir)

# 日志，名称可自己修改
log_name = conf.getValue('log_name')

def get_time_str(format="%Y-%m-%d-%H%M%S"):
    """这个函数用于获取指定格式的时间字符串。This function is used to get the time string of the specified format.
    
    Keyword Arguments:
        format {str} -- the format of time string (default: {"%Y%m%d%H%M%S"})
    
    Returns:
        [str] -- time string of the specified format
    """
    import time
    time_str = time.strftime(format, time.localtime())
    return time_str

if __name__ == "__main__":
       
    pb = NSPasteboard.generalPasteboard()  # 获取当前系统剪切板数据
    data_type = pb.types()  # 获取剪切板数据的格式类型
    # print(data_type)

    # 根据剪切板数据类型进行处理
    if NSPasteboardTypePNG in data_type:
        # PNG

        # 用当前时间给图片命名
        tm = time.localtime()
        pic_name = time.strftime("%Y-%m-%d-%H%M%S", tm)+'.png'
        # print(pic_name)
        pic_path = os.path.join(pic_save_dir, pic_name)
       
        data = pb.dataForType_(NSPasteboardTypePNG)        
        ret = data.writeToFile_atomically_(pic_path, False)    # 将剪切板数据保存为文件

        if pic_bed == 'smms':
            # v1
            f_img = open(os.path.join(pic_save_dir, pic_name),'rb')
            r = requests.post('https://sm.ms/api/upload', files={'smfile':f_img, 'format':'json'})
            f_img.close()
            ret = json.loads(r.text)
    
            # 日志文件
            f_log = open(log_name, 'a')
            f_log.write('Picture name: %s\n' % pic_name)
            f_log.write('url: %s\n' % ret['data']['url'])
            f_log.write('delete: %s\n' % ret['data']['delete'])
            f_log.write('----------------------------------\n')
            f_log.close()
            markdown_url = '![](%s)' % ret['data']['url']

        elif pic_bed == 'aliyun':
            import oss2
            endpoint = conf.getValue('endpoint')
            bucket_name = conf.getValue('bucket_name')

            auth = oss2.Auth(conf.getValue('key_id'), conf.getValue('key_secret'))
            bucket = oss2.Bucket(auth, endpoint, bucket_name)

            objectName = time.strftime("%Y/%m/", tm) + pic_name
            r = bucket.put_object_from_file(objectName, pic_path)
            if r.status == 200:
                markdown_url = '![ali](https://%s.%s/%s)'\
                     % (bucket_name, endpoint.replace('https://', ''), objectName)
                # markdown_url = '<img alt="ali" width=80%% src="https://%s.%s/%s" style="display:block; margin:0 auto;">'\
                #      % (bucket_name, endpoint.replace('https://', ''), objectName)
                f_log = open(log_name, 'a')
                f_log.write('%s: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S ', tm), pic_name))
                f_log.write('markdown url: %s\n' % markdown_url)
                f_log.write('----------------------------------\n')
                f_log.close()
            else:
                markdown_url = 'Upload failed! Status: ' + r.status

        pb = pasteboard.Pasteboard()
        print(pb.set_contents(markdown_url))

    elif NSPasteboardTypeString in data_type:
        # string
        data = pb.dataForType_(NSPasteboardTypeString) # bytes类型
        data = str(data, 'utf-8')

        import re
        if not re.search('扇贝单词', data):
            # 非扇贝
            exit()
        if re.search('例句', data):
        # if re.search(b'例句', data):
            # 有例句
            pattern = re.compile('([a-z]+)\n(.+)trumpet\n(.+)trumpet\n\n.+典\n(.+)例句\n\n(.*)', re.I | re.S)
        else:
            # 无例句
            pattern = re.compile('([a-z]+)\n(.*)trumpet\n(.*)trumpet\n\n.+典\n(.+)(.*)', re.I | re.S)

        res = re.split(pattern=pattern, string=data)
        # print(res)

        # 1-单词 2-US音标 3-UK音标 4-释义 5-例句（可无）
        if sb_editor == 'evernote':
            if sb_style == 'blod':
                md = '**' + res[1] + '** '\
                + res[2] + ' '\
                + res[3] + '\n'\
                + re.sub('\n\n', '\n', res[4]) + ''\
                + re.sub('\n\n', '\n', res[5]) + '\n\n'
            elif sb_style == 'form':
                md = 'Evernote editor doesn\'t support \'<br>\'. Please use vscode.'
        elif sb_editor == 'vscode':
            if sb_style == 'blod':
                md = '**' + res[1] + '**\n'\
                + res[2] + '\n'\
                + res[3] + '\n\n'\
                + res[4] + ''\
                + res[5] + '\n\n'
            elif sb_style == 'form':
                md = '|' + res[1] + '|'\
                + res[2] + '<br>'\
                + res[3] + '|'\
                + re.sub('\n\n', '<br>', res[4]) + '|'\
                + re.sub('\n\n', '<br>', res[5]) + '|\n'
                
        # print(md)
        pb = pasteboard.Pasteboard()
        print(pb.set_contents(md))
    else:
        print('未知格式')
