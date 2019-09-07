# 介绍

Version: 0.3

这个仓库中存放的是一些基于python的脚本，配合上uTools(Win)、Alfred(macOS)等软件，可大大提高学习工作的效率。

目前有如下脚本：
- 将剪贴板的图片上传到smms/阿里云图床 v0.2
  - `uploadpic.py` : Win/Mac端
- 云剪贴板 v0.2
  - `syncClipboard.py` : Win/Mac端
- 去除字符串中的换行，在复制pdf文本时会多出很多换行符 v0.1
  - `rmlb.py` : Win端

其余文件的用途：
- `scriptConfiger.py` : 各脚本用于读取一些必要的配置，比如云剪贴板中用户的身份信息，存放在 `config.ini` 文件中
- `mainController.py` : 脚本的总控制器，可以组合一些脚本来实现更复杂的功能。
- `notifier.py` : 弹窗通知，用于告知用户脚本运行完成。

## 依赖库

各脚本用到的库不尽相同，这里将用到的所有库都列举出来。

**Windows**
```
oss2==2.8.0
```

**macOS**
```
oss2==2.6.1
pasteboard==0.2.0
```

## 使用说明

每个脚本需要先运行一遍，然后脚本就会在 `config.ini` 文件（文件不存在时会自动创建）中生成需要的参数项，补充完整后即可使用。

也可以自行按下面格式手动创建 `config.ini` 文件。

```ini
[default]
intro = some scripts to improve efficiency
author = Dan

[picbed]
pic_bed = aliyun
; pic_bed 可选 「smms」或「aliyun」
log_path = picbed/log.txt
pic_save_dir = picbed
key_id = xxx
key_secret = xxx
endpoint = xxx
bucket_name = xxx

[syncClipboard]
key_id = xxx
key_secret = xxx
endpoint = xxx
bucket_name = xxx
project_dir = syncClipboard

```

## 将剪贴板的图片上传到smms/阿里云图床

```
python uploadpic.py
```

## 云剪贴板

- 单参数调用时，功能是将云端内容下载到剪贴板。
```
python syncClipboard.py
```

- 双参数调用时，功能是将剪贴板内容上传到云端。第二参数的值无限制，随意填即可。
```
python syncClipboard.py upload
```