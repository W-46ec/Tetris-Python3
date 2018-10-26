import random
import setting

# 核心模块
class Core():
	matrixBuffer = setting.matrixBuffer
	row, column = setting.row, setting.column
	matrixRow, matrixColumn = setting.matrixRow, setting.matrixColumn
	score, initInterval, interval = setting.score, setting.initInterval, setting.interval

	matrix = []		# 主矩阵

	# 方块信息
	tetromino = {
		'I': (
			((1, 0), (1, 1), (1, 2), (1, 3)), 
			((0, 1), (1, 1), (2, 1), (3, 1))
		), 
		'O': (
			((0, 1), (0, 2), (1, 1), (1, 2)), 
		), 
		'T': (
			((0, 1), (1, 0), (1, 1), (1, 2)), 
			((0, 1), (1, 1), (1, 2), (2, 1)), 
			((1, 0), (1, 1), (1, 2), (2, 1)), 
			((0, 1), (1, 0), (1, 1), (2, 1))
		), 
		'L': (
			((0, 1), (1, 1), (2, 1), (2, 2)), 
			((1, 0), (1, 1), (1, 2), (2, 0)), 
			((0, 0), (0, 1), (1, 1), (2, 1)), 
			((0, 2), (1, 0), (1, 1), (1, 2))
		), 
		'J': (
			((0, 1), (1, 1), (2, 0), (2, 1)), 
			((0, 0), (1, 0), (1, 1), (1, 2)), 
			((0, 1), (0, 2), (1, 1), (2, 1)), 
			((1, 0), (1, 1), (1, 2), (2, 2))
		), 
		'S': (
			((0, 1), (1, 1), (1, 2), (2, 2)), 
			((0, 1), (0, 2), (1, 0), (1, 1))
		), 
		'Z': (
			((0, 1), (1, 1), (1, 0), (2, 0)), 
			((0, 0), (0, 1), (1, 1), (1, 2))
		)
	}

	# 初始化
	def __init__(self):
		self.initMatrix()

	# 主矩阵初始化
	def initMatrix(self):
		for i in range(self.matrixRow):	# 矩阵外围一圈为缓冲区
			self.matrix.append([0] * self.matrixColumn)

	# 生成种子
	def generateSeed(self):
		types = "IOTLJSZ"
		randNum = random.randint(0, len(types) - 1)
		seed = {
			'type': types[randNum], 
			'state': random.randint(0, len(self.tetromino[types[randNum]]) - 1)
		}
		return seed

	# 生成一个 dict 类型的方块信息
	def generateTetromino(self, seed):
		block = {
			'x': 1, 
			'y': self.column // 2, 
			'type': seed['type'],
			'state': seed['state']
		}
		return block

	# 将方块写入主矩阵
	def writeTetromino(self, block):
		matrixInfo = self.tetromino[block['type']][block['state']]
		for i in range(4):
			self.matrix[1 + matrixInfo[i][0]][self.column // 2 + matrixInfo[i][1]] = 1

	# 生成一个 4*4 的 list 类型的方块信息矩阵
	def generateBlockMatrix(self, block):
		matrixInfo = self.tetromino[block['type']][block['state']]
		x = block['x']
		y = block['y']
		BlockMatrix = []

		for i in range(4):
			BlockMatrix.append([0] * 4)

		for i in matrixInfo:
			BlockMatrix[i[0]][i[1]] = 1

		return BlockMatrix

	# 获取方块边界信息
	def getAllBorder(self, block):
		matrixInfo = self.tetromino[block['type']][block['state']]
		border_all = {
			'l_min': matrixInfo[0][1], 
			'r_max': matrixInfo[0][1], 
			'bottom_max': matrixInfo[0][0], 
			'Left': [], 
			'Right': [], 
			'bottom': []
		}

		row_i = [[], [], [], []]	# 区分每行的信息
		column_i = [[], [], [], []]	# 区分每列的信息
		for i in range(4):
			for j in range(4):
				if matrixInfo[j][0] == i:
					row_i[i].append(matrixInfo[j])
				if matrixInfo[j][1] == i:
					column_i[i].append(matrixInfo[j])

		for i in range(4):
			# 若该行不为空
			if len(row_i[i]) != 0:
				sorted_column = sorted(row_i[i], key = lambda e: e[1])	# 按 y 值排序
				border_all['Left'].append(sorted_column[0])
				border_all['Right'].append(sorted_column[len(sorted_column) - 1])
				if sorted_column[0][1] < border_all['l_min']:
					border_all['l_min'] = sorted_column[0][1]
				if sorted_column[len(sorted_column) - 1][1] > border_all['r_max']:
					border_all['r_max'] = sorted_column[len(sorted_column) - 1][1]
				if i > border_all['bottom_max']:
					border_all['bottom_max'] = i
			# 若该列不为空
			if len(column_i[i]) != 0:
				sorted_row = sorted(column_i[i], key = lambda e: e[0])	# 按 x 值排序
				border_all['bottom'].append(sorted_row[len(sorted_row) - 1])

		return border_all

	# 移动检测函数
	def moveCheck(self, block, direction):
		matrixInfo = self.tetromino[block['type']][block['state']]
		x = block['x']
		y = block['y']
		border = self.getAllBorder(block)	# 边界极值信息
		if direction == 'Right':
			if border['r_max'] + y >= self.column:
				return False
			y += 1
			for i in border['Right']:
				if self.matrix[x + i[0]][y + i[1]] == 1:
					return False
		elif direction == 'Left':
			if border['l_min'] + y <= 1:
				return False
			y -= 1
			for i in border['Left']:
				if self.matrix[x + i[0]][y + i[1]] == 1:
					return False
		elif direction == 'Down':
			if border['bottom_max'] + x >= self.row:
				return False
			x += 1
			for i in border['bottom']:
				if self.matrix[x + i[0]][y + i[1]] == 1:
					return False
		return True

	# 移动函数
	def move(self, block, direction, autoDown = False):
		matrixInfo = self.tetromino[block['type']][block['state']]
		x = block['x']
		y = block['y']

		# 右移
		if direction == 'Right':
			if self.moveCheck(block, 'Right') == True:
				for i in range(4):
					self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 0
				y += 1
				block['y'] += 1
				for i in range(4):
					self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 1

		# 左移
		elif direction == 'Left':
			if self.moveCheck(block, 'Left') == True:
				for i in range(4):
					self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 0
				y -= 1
				block['y'] -= 1
				for i in range(4):
					self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 1

		# 下移
		elif direction == 'Down':

			# 手动下移
			if autoDown == False:
				while self.moveCheck(block, 'Down') == True:
					block['x'] += 1
				for i in range(4):
					self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 0
				x = block['x']
				for i in range(4):
					self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 1
				return 1		# 方块以固定

			# 自动下移
			elif autoDown == True:
				if self.moveCheck(block, 'Down') == True:
					block['x'] += 1
				else:
					return 1		# 方块以固定
				for i in range(4):
					self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 0
				x = block['x']
				for i in range(4):
					self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 1

	# 旋转检测函数
	def rotateCheck(self, block):
		x = block['x']
		y = block['y']
		length = len(self.tetromino[block['type']])

		# 原方块参数
		prevState = block['state']
		prevMatrixInfo = self.tetromino[block['type']][prevState]

		# 新方块参数
		newState = (prevState + 1) % length
		newMatrixInfo = self.tetromino[block['type']][newState]
		newBlock = block.copy()
		newBlock['state'] = newState

		border = self.getAllBorder(newBlock)	# 新方块边界极值信息
		if border['r_max'] + y > self.column or \
			border['l_min'] + y < 1 or \
			border['bottom_max'] + x > self.row:
			return False
		for i in range(4):
			self.matrix[x + prevMatrixInfo[i][0]][y + prevMatrixInfo[i][1]] = 0
		for i in range(4):
			if self.matrix[x + newMatrixInfo[i][0]][y + newMatrixInfo[i][1]] == 1:
				for i in range(4):
					self.matrix[x + prevMatrixInfo[i][0]][y + prevMatrixInfo[i][1]] = 1
				return False
		for i in range(4):
			self.matrix[x + prevMatrixInfo[i][0]][y + prevMatrixInfo[i][1]] = 1
		return True

	# 旋转函数
	def rotate(self, block):
		matrixInfo = self.tetromino[block['type']][block['state']]
		x = block['x']
		y = block['y']
		length = len(self.tetromino[block['type']])
		if self.rotateCheck(block) == True:
			state = (block['state'] + 1) % length
			block['state'] = state
			for i in range(4):
				self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 0
			matrixInfo = self.tetromino[block['type']][state]
			for i in range(4):
				self.matrix[x + matrixInfo[i][0]][y + matrixInfo[i][1]] = 1

	# 消除检测 (返回可以被消除的行号)
	def rmRowDetect(self, startRow):
		for i in range(startRow, 0, -1):
			counter = 0
			for j in range(1, self.column + 1):
				if self.matrix[i][j] == 1:
					counter += 1
			if counter == self.column:
				return i 		# 返回行号
			if counter == 0:	# 若为空行，则可停止搜索
				return -1
		return 0

	# 递归消除满行
	def rmRow(self, startRow = 20):
		row = self.rmRowDetect(startRow)
		if row > 0:
			for i in range(row, 0, -1):
				for j in range(1, self.column + 1):
					self.matrix[i][j] = self.matrix[i - 1][j]
			self.score += 1		# 分数增加
			if self.initInterval - 0.1 * int(self.score / 10) > 0.1:
				self.interval = self.initInterval - 0.1 * int(self.score / 10)	# 自动下落时间间隔衰减
			else:
				self.interval = 0.1
			self.rmRow(startRow = row)
		elif row == 0 or row == -1:
			return

	# 失败检测
	def isLose(self):
		for i in range(4):
			for j in range(4):
				if self.matrix[1 + i][self.column // 2 + j] == 1:
					return True
		return False

	# 在控制台输出矩阵信息(测试用)
	def ConsolePrintMatrix(self):
		for i in range(self.matrixRow):
			print(self.matrix[i])