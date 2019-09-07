import sys
from syncClipboard import syncClipboard
from notifier import notifier
from picbed import picbed

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("The number of parameters is invalid.")
		exit()

	if sys.argv[1] == '1':
		syncClipboard('upload')
		notifier('云剪贴板', '上传完成。')
	elif sys.argv[1] == '2':
		syncClipboard()
		notifier('云剪贴板', '下载完成。')
	elif sys.argv[1] == '3':
		picbed()
		syncClipboard('upload')
		notifier('图床', '上传完成。')
		