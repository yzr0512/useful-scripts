import os
import sys
import time

import util

from scriptConfiger import ScriptConfiger
def getConfig(name='picbed'):
    sc = ScriptConfiger(section=name)
    if not sc.isSectionExists():
        sc.setKeyValue('pic_bed', 'aliyun') # smms, aliyun
        sc.setKeyValue('pic_save_dir', 'picbed')
        sc.setKeyValue('log_path', 'picbed/log.txt')
        
        sc.setKeyValue('key_id', 'xxx')
        sc.setKeyValue('key_secret', 'xxx')
        sc.setKeyValue('endpoint', 'xxx') # ['evernote', 'vscode']
        sc.setKeyValue('bucket_name', 'xxx') # ['blod', 'form']

        exit()
    return sc
conf = getConfig()

# 配置项
pic_bed = conf.getValue('pic_bed')
log_path = conf.getValue('log_path')

# 将工作目录修改为当前代码的位置
cur_dir = os.path.dirname(sys.argv[0]) # sys.argv的第一个参数是代码文件的绝对\或与工作目录的相对路径
if cur_dir != "":
	os.chdir(cur_dir)
# print(os.getcwd())

# 保存图片的文件夹名称（可修改）及路径，默认与代码所在的路径相同
pic_save_dir = conf.getValue('pic_save_dir')
if not os.path.exists(pic_save_dir):
    os.mkdir(pic_save_dir)


def upload_smms(pic_name, proj_dir='picbed', log_path='picbed/log.txt'):
    """上传到sm.ms图床。
    
    Arguments:
        pic_name {str} -- 图片文件名称，不包括路径。
    
    Keyword Arguments:
        proj_dir {str} -- 图片文件夹 (default: {'picbed'})
        log_path {str} -- 日志文件的路径，包括文件名 (default: {'picbed/log.txt'})
    
    Returns:
        [str] -- markdown形式的图片链接
    """
    import requests
    import json
    # v1
    f_img = open(os.path.join(proj_dir, pic_name),'rb')
    r = requests.post('https://sm.ms/api/upload', files={'smfile':f_img, 'format':'json'})
    f_img.close()
    ret = json.loads(r.text)
    # debug_log(ret)

    # 日志文件
    f_log = open(log_path, 'a')
    f_log.write('Picture name: %s\n' % pic_name)
    f_log.write('url: %s\n' % ret['data']['url'])
    f_log.write('delete: %s\n' % ret['data']['delete'])
    f_log.write('----------------------------------\n')
    f_log.close()
    markdown_url = '![smms](%s)' % ret['data']['url']
    return markdown_url


def upload_aliyun(pic_name, proj_dir='picbed', log_path='picbed/log.txt'):
    """上传到阿里云图床。
    
    Arguments:
        pic_name {str} -- 图片文件名称，不包括路径。
    
    Keyword Arguments:
        proj_dir {str} -- 图片文件夹 (default: {'picbed'})
        log_path {str} -- 日志文件的路径，包括文件名 (default: {'picbed/log.txt'})
    
    Returns:
        [str] -- markdown形式的图片链接
    """
    import oss2
    endpoint = conf.getValue('endpoint')
    bucket_name = conf.getValue('bucket_name')

    auth = oss2.Auth(conf.getValue('key_id'), conf.getValue('key_secret'))
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    tm = time.localtime()
    objectName = time.strftime("%Y/%m/", tm) + pic_name
    r = bucket.put_object_from_file(objectName, os.path.join(proj_dir, pic_name))
    if r.status == 200:
        markdown_url = '![ali](https://%s.%s/%s)'\
                % (bucket_name, endpoint.replace('https://', ''), objectName)
        # markdown_url = '<img alt="ali" width=80%% src="https://%s.%s/%s" style="display:block; margin:0 auto;">'\
        #         % (bucket_name, endpoint.replace('https://', ''), objectName)
        f_log = open(log_path, 'a')
        f_log.write('%s: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S ', tm), pic_name))
        f_log.write('markdown url: %s\n' % markdown_url)
        f_log.write('----------------------------------\n')
        f_log.close()
    else:
        markdown_url = 'Upload failed! Status: ' + r.status    

    return markdown_url


def picbed():
    if util.getClipboardDataType() != util.TYPE_PNG:
        print('The data in the clipboard is not an image.')
        exit()
    
    # 用当前时间给图片命名
    tm = time.localtime()
    pic_name = time.strftime("%Y-%m-%d-%H%M%S", tm)+'.png'
    pic_path = os.path.join(pic_save_dir, pic_name)

    _, path = util.getClipboardData(projDir=pic_save_dir)
    if not os.path.exists(path):
        print('Error: Image is not existed.')
        exit(2)
    os.rename(path, pic_path)

    if pic_bed == 'smms':
        s = upload_smms(pic_name, pic_save_dir, log_path)
    elif pic_bed == 'aliyun':
        s = upload_aliyun(pic_name, pic_save_dir, log_path)
    else:
        s = 'Error: the picture bed which you choosed is not supported.'
    util.setClipboardData(util.TYPE_STRING, s)
    print('Picbed: Finish!')


if __name__ == "__main__":

    picbed()
