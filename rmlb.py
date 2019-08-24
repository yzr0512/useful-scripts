# -*- coding: UTF-8 -*-
# remove the line break when copy from pdf

import os
import sys

import win32clipboard as wcb


def check_contain_chinese(check_str):
    for ch in check_str:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def remove_cb_line_break():
    wcb.OpenClipboard()
    if wcb.IsClipboardFormatAvailable(wcb.CF_TEXT):
        text = wcb.GetClipboardData()
        if check_contain_chinese(text):
			# text = text.replace(' ', '')
            text = text.replace('\r', '')
            text = text.replace('\n', '')
        else:
            text = text.replace('\r', '')
            text = text.replace('\n', ' ')
        wcb.EmptyClipboard()
        wcb.SetClipboardData(wcb.CF_UNICODETEXT, text)
        # wcb.SetClipboardText(text)
    wcb.CloseClipboard()

if __name__ == "__main__":

    # 将工作目录修改为当前代码的位置
    cur_dir = os.path.dirname(sys.argv[0]) # sys.argv的第一个参数是代码文件的绝对\或与工作目录的相对路径
    if cur_dir != "":
        os.chdir(cur_dir)
       
    remove_cb_line_break()
    os.system('C_v.ahk')
    # print(wcb.IsClipboardFormatAvailable(wcb.CF_TEXT))
    