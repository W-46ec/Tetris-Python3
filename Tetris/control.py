from file import File

# 控制模块
class Control():

	core = None				# 用于保存核心对象
	block = {				# 用于保存当前方块信息
		'x': None, 
		'y': None, 
		'type': None, 
		'state': None
	}
	nextBlockSeed = {		# 用于保存下一方块种子
		'type': None, 
		'state': None
	}

	stopThread = True		# 控制自动下落线程的开关
	pause = False 			# 用于判断是否为暂停状态
	start = False 			# 用于判断游戏是否已开始
	helpPage = False 		# 用于判断帮助页是否打开

	# 初始化
	def __init__(self, core):
		self.core = core 	# 复制核心对象
		self.nextBlockSeed = self.core.generateSeed()	# 生成第一个方块种子
		self.nextBlock()	# 激活第一个方块

	# 操作函数
	def operation(self, key, autoDown = False):

		# 操作反馈信息
		operationInfo = {
			'isBottom': None, 
			'Exit': False
		}

		# 游戏操作
		if self.start == True:
			# 方向操作
			if self.pause == False:
				# WASD 控制方向
				wasd = {
					'w': 'Up', 
					'a': 'Left', 
					's': 'Down', 
					'd': 'Right', 
					'W': 'Up', 
					'A': 'Left', 
					'S': 'Down', 
					'D': 'Right'
				}
				if key in wasd:
					key = wasd[key]
				# 移动操作
				if key == 'Right' or \
					key == 'Left' or \
					key == 'Down':
					operationInfo['isBottom'] = self.core.move(self.block, key, autoDown)
					if operationInfo['isBottom'] == 1:
						self.core.rmRow()
						operationInfo['isBottom'] = 1
						return operationInfo
				# 旋转操作
				elif key == 'Up':
					self.core.rotate(self.block)

			# 暂停
			if key == 'p' or key == 'P':
				if self.pause == True:
					self.stopThread = False
					self.pause = False
				else:
					self.stopThread = True
					self.pause = True

			if key == '\x13':
				self.stopThread = True
				self.pause = True
				File().save(str(self.getAllInfo()))

		# 退出
		if key == 'Escape':
			self.stopThread = True
			if self.start == True:
				self.pause = True
			operationInfo['Exit'] = True

		# 开始游戏
		if key == 'n' or key == 'N':
			if self.start == False:
				self.pause = False
				self.stopThread = False
				self.start = True

		# 加载存档
		if key == 'l' or key == 'L':
			if self.start == False:
				File().load(self.core, self)
			
		return operationInfo

	# 激活下一方块
	def nextBlock(self):
		self.block = self.generateNextBlock()
		self.nextBlockSeed = self.core.generateSeed()
		self.core.writeTetromino(self.block)

	# 生成下一方块信息
	def generateNextBlock(self):
		return self.core.generateTetromino(self.nextBlockSeed)

	# 获取 4*4 矩阵
	def getBlockMatrix(self, block):
		return self.core.generateBlockMatrix(block)

	# 获取核心参数
	def getParameter(self):
		return {
			'column': self.core.column, 
			'row': self.core.row, 
			'score': self.core.score, 
			'interval': self.core.interval, 
			'matrix': self.core.matrix
		}

	# 获取用于保存文件的所有参数
	def getAllInfo(self):
		return {
			'matrix': self.core.matrix, 
			'score': self.core.score, 
			'interval': self.core.interval, 
			'block': self.block, 
			'nextBlockSeed': self.nextBlockSeed, 
			'stopThread': self.stopThread, 
			'pause': self.pause, 
			'start': self.start, 
			'helpPage': self.helpPage
		}

	# 返回是否输信息
	def getIsLose(self):
		return self.core.isLose()