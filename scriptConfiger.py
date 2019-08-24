import configparser
import os
import sys

# 将工作目录修改为当前代码的位置
cur_dir = os.path.dirname(sys.argv[0]) # sys.argv的第一个参数是代码文件的绝对\或与工作目录的相对路径
if cur_dir != "":
	os.chdir(cur_dir)
# print(os.getcwd())

class ScriptConfiger():
    def __init__(self, section='default', fpath='config.ini'):
        self.fpath = fpath
        if not os.path.exists(fpath):
            self.buildConfigFile()
        
        # 初始化并读取ini文件
        self.conf = configparser.ConfigParser()
        self.conf.read(fpath, encoding='utf-8')
        self.section = section
        # print(os.getcwd())

    def getValue(self, option):
        return self.conf.get(self.section, option, fallback=None)

    def buildConfigFile(self):
        print('Build config file.')
        conf = configparser.ConfigParser()
        conf.add_section('default')
        conf.set('default', 'intro', 'some scripts to improve efficiency')
        conf.set('default', 'author', 'Dan')
        conf.write(open(self.fpath, 'w'))

    def isSectionExists(self):
        if self.conf.has_section(self.section):
            return True
        else:
            self.conf.add_section(self.section)
            return False

    # def addSection(self):

    def setKeyValue(self, key, value):
        self.conf.set(self.section, key, value)
        self.conf.write(open(self.fpath, 'w'))


    # def writeConfigToFile(self):

# def buildConfig():
#     sc = ScriptConfig()
#     conf = sc.getConf()
#     section_name = 'uploadpic'
#     conf.add_section(section_name)
#     conf.set(section_name, 'picBed', 'aliyun')
#     conf.set(section_name, 'log_name', 'log.txt')
#     conf.write()

def newSection(name='uploadpic'):
    sc = ScriptConfiger(section=name)
    if not sc.isSectionExists():
        sc.setKeyValue('picBed', 'aliyun')
        sc.setKeyValue('log_name', 'log.txt')

if __name__ == "__main__":
    # sc = ScriptConfiger(section='default')
    # res = sc.getValue('intro')
    # print(res)
    newSection()
    sc = ScriptConfiger(section='uploadpic')
    print(sc.getValue('picBed'))