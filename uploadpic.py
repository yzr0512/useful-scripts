import os
import sys
import requests
import json
import time

# win平台特有库
import winsound
from PIL import ImageGrab
import win32clipboard as wcb
import win32con

from scriptConfiger import ScriptConfiger
def getConfig(name='uploadpic'):
    sc = ScriptConfiger(section=name)
    if not sc.isSectionExists():
        sc.setKeyValue('pic_bed', 'aliyun') # smms, aliyun
        sc.setKeyValue('pic_save_dir', 'saved_pic')
        sc.setKeyValue('log_name', 'saved_pic/log.txt')
        
        sc.setKeyValue('key_id', 'xxx')
        sc.setKeyValue('key_secret', 'xxx')
        sc.setKeyValue('endpoint', 'xxx') # ['evernote', 'vscode']
        sc.setKeyValue('bucket_name', 'xxx') # ['blod', 'form']

        exit()
    return sc
conf = getConfig()

# 配置项
pic_bed = conf.getValue('pic_bed')
log_name = conf.getValue('log_name')

# 将工作目录修改为当前代码的位置
cur_dir = os.path.dirname(sys.argv[0]) # sys.argv的第一个参数是代码文件的绝对\或与工作目录的相对路径
if cur_dir != "":
	os.chdir(cur_dir)
# print(os.getcwd())

# 保存图片的文件夹名称（可修改）及路径，默认与代码所在的路径相同
pic_save_dir = conf.getValue('pic_save_dir')
if not os.path.exists(pic_save_dir):
    os.mkdir(pic_save_dir)

def get_time_str(format="%Y-%m-%d-%H%M%S"):
    """这个函数用于获取指定格式的时间字符串。This function is used to get the time string of the specified format.
    
    Keyword Arguments:
        format {str} -- the format of time string (default: {"%Y%m%d%H%M%S"})
    
    Returns:
        [str] -- time string of the specified format
    """

    time_str = time.strftime(format, time.localtime())
    return time_str


def setClipboardText(text):
    wcb.OpenClipboard()
    wcb.EmptyClipboard()
    wcb.SetClipboardText(text)
    wcb.CloseClipboard()

if __name__ == "__main__":

    # 检查剪贴板中是否图片，防止误调用
    if not wcb.IsClipboardFormatAvailable(wcb.CF_BITMAP): # 非图片就执行默认的粘贴命令
        if wcb.IsClipboardFormatAvailable(wcb.CF_TEXT):
            import rmlb
            rmlb.remove_cb_line_break()
        
        winsound.PlaySound('tone_beep.wav', winsound.SND_FILENAME) # 自定义铃声在电脑未播放音频的时候会出现听不见的现象
        # os.system('C_v.ahk')
        exit()

    # 用当前时间给图片命名
    tm = time.localtime()
    pic_name = time.strftime("%Y-%m-%d-%H%M%S", tm)+'.png'
    pic_path = os.path.join(pic_save_dir, pic_name)
    im = ImageGrab.grabclipboard()
    im.save(pic_path, 'png')

    if pic_bed == 'smms':
        # v1
        f_img = open(os.path.join(pic_save_dir, pic_name),'rb')
        r = requests.post('https://sm.ms/api/upload', files={'smfile':f_img, 'format':'json'})
        f_img.close()
        ret = json.loads(r.text)
        # debug_log(ret)

        # 日志文件
        f_log = open(log_name, 'a')
        f_log.write('Picture name: %s\n' % pic_name)
        f_log.write('url: %s\n' % ret['data']['url'])
        f_log.write('delete: %s\n' % ret['data']['delete'])
        f_log.write('----------------------------------\n')
        f_log.close()
        markdown_url = '![smms](%s)' % ret['data']['url']

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
            #         % (bucket_name, endpoint.replace('https://', ''), objectName)
            f_log = open(log_name, 'a')
            f_log.write('%s: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S ', tm), pic_name))
            f_log.write('markdown url: %s\n' % markdown_url)
            f_log.write('----------------------------------\n')
            f_log.close()
        else:
            markdown_url = 'Upload failed! Status: ' + r.status
        print(r.status)

    # 剪贴板赋值，将url转换成markdown格式
    setClipboardText(markdown_url)

    # 通知用户上传完毕
    # winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)
    winsound.PlaySound('tone_beep.wav', winsound.SND_FILENAME) # 自定义铃声在电脑未播放音频的时候会出现听不见的现象

    # 调用AutoHotkey来将剪贴板内容粘贴出来
    # os.system('C_v.ahk')
