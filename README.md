# 介绍

Version: 0.2

这个仓库中存放的是一些基于python的脚本，配合上uTools(Win)、Alfred(macOS)等软件，可大大提高学习工作的效率。

目前有如下脚本：
- 将剪贴板的图片上传到smms/阿里云图床 v0.1
  - `uploadpic.py` : Win端
  - `uploadpic_mac.py` : Mac端
- 云剪贴板 v0.1
  - `syncClipboard.py` : Win端
  - `syncClipboard_mac.py` : Mac端
- 去除字符串中的换行，在复制pdf文本时会多出很多换行符 v0.1
  - `rmlb.py` : Win端

其余文件的用途：
- `scriptConfiger.py` : 各脚本用于读取一些必要的配置，比如云剪贴板中用户的身份信息，存放在 `config.ini` 文件中
- `tone_beep.wav` : 脚本完成时播放的声音

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

[uploadpic]
pic_bed = aliyun
; pic_bed 可选 「smms」或「aliyun」
log_name = saved_pic/log.txt
pic_save_dir = saved_pic
key_id = xxx
key_secret = xxx
endpoint = xxx
bucket_name = xxx

[uploadpic_mac]
pic_bed = aliyun
; pic_bed 可选 「smms」或「aliyun」
pic_save_dir = saved_pic
log_name = saved_pic/log.txt
sb_editor = vscode
; sb_editor 可选 「vscode」或「evernote」
sb_style = form
; sb_style 可选 「form」或「blod」
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

[syncClipboard_mac]
key_id = xxx
key_secret = xxx
endpoint = xxx
bucket_name = xxx
project_dir = syncClipboard
```

## 将剪贴板的图片上传到smms/阿里云图床

## 云剪贴板

