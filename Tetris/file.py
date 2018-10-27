import json
import tkinter.messagebox as messagebox
from tkinter.filedialog import askdirectory
from tkinter import filedialog

# 文件模块
class File():

	# 数据过滤
	def loadDataFilter(self, core, content):
		for i in range(core.matrixRow):
			for j in range(core.matrixColumn):
				if i == 0 or i == core.matrixRow - 1 or \
					j == 0 or j == core.matrixColumn - 1:
					if content['matrix'][i][j] == 1:
						return False
				else:
					if content['matrix'][i][j] != 1 and \
						content['matrix'][i][j] != 0:
						return False
				core.matrix[i][j] = content['matrix'][i][j]
		if content['interval'] < 0:
			return False
		if content['block']['x'] < 0 or content['block']['x'] > core.row:
			return False
		if content['block']['y'] < 0 or content['block']['y'] > core.column:
			return False
		if content['block']['type'] not in 'IOTLJSZ':
			return False
		if content['block']['state'] < 0 or \
			content['block']['state'] > len(core.tetromino[content['block']['type']]):
			return False
		if content['nextBlockSeed']['type'] not in 'IOTLJSZ':
			return False
		if content['nextBlockSeed']['state'] < 0 or \
			content['nextBlockSeed']['state'] > len(core.tetromino[content['block']['type']]):
			return False
		return True

	# 读档
	def load(self, core, control):
		try:
			path = filedialog.askopenfilename(	# 获取存档路径
				filetypes = (
					("JSON", "*.json*"), 
					("All files", "*.*")
				)
			)
			if path:
				with open(path, 'r') as f:
					content = json.loads(f.read())

					# 写入数据
					try:
						if self.loadDataFilter(core, content) == True:
							for i in range(1, core.row + 1):
								for j in range(1, core.column + 1):
									core.matrix[i][j] = content['matrix'][i][j]
							core.score = content['score']
							core.interval = content['interval']
							control.block['x'] = content['block']['x']
							control.block['y'] = content['block']['y']
							control.block['type'] = content['block']['type']
							control.block['state'] = content['block']['state']
							control.nextBlockSeed['type'] = content['nextBlockSeed']['type']
							control.nextBlockSeed['state'] = content['nextBlockSeed']['state']
							control.stopThread = True
							control.pause = True
							control.start = True
						else:
							messagebox.showerror('Error', '参数错误')	# 游戏参数错误
					except BaseException as err:
						messagebox.showerror('Error', 'Unknown error')	# 游戏参数错误
		except BaseException as e:
			messagebox.showerror('Error', e)	# 文件读写错误

	# 存档
	def save(self, content):
		string = json.dumps(content, indent = 4)
		saveAs = filedialog.asksaveasfilename(
			defaultextension = ".json", 
			filetypes = (
				("JSON", "*.json"), 
			)
		)
		if saveAs:
			try:
				with open(saveAs, 'w') as f:
					f.write(string)
			except BaseException as e:
				messagebox.showerror('Error', e)