import sys
import testsyncClipboard
import notifier

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("The number of parameters is invalid.")
		exit()
	if sys.argv[1] == '1':
		testsyncClipboard.syncClipboard('upload')
		notifier.notifier('云剪贴板', '上传完成。')
	elif sys.argv[1] == '2':
		testsyncClipboard.syncClipboard()
		notifier.notifier('云剪贴板', '下载完成。')
