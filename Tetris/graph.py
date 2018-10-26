import time
import threading
import os
from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.font as tkFont

# 图像模块
class Graph():

	# 窗体对象
	mainPanel = Tk()
	mainPanel.title("Tetris")		# 标题
	mainPanel.geometry("640x480")	# 窗口大小
	mainPanel.resizable(width = False, height = False)	# 窗体大小不可变

	control = None			# 用于保存控制对象

	startRun = False 		# 用于判断启动动画是否播放过

	autoFallThread = None	# 用于保存自动下落线程

	graphMatrix = []		# 图像面板矩阵
	nextBlockMatrix = []	# 下一方块图像面板矩阵

	# 主画布
	cv = Canvas(
		mainPanel, 
		bg = 'black', 
		width = 640, 
		height = 480
	)

	gameWindow = None		# 用于存放游戏界面
	gameCv = None			# 用于存放游戏界面画布
	pauseBox = None			# 用于存放暂停提示框
	startWindow = None		# 用于存放启动页面
	startCv = None			# 用于存放启动画布
	menuWindow = None		# 用于存放菜单页面
	helpWindow = None		# 用于存放帮助页面
	scoreText = None		# 记分板面板

	titleFont = tkFont.Font(size = 25)	# Title 字号
	itemFont = tkFont.Font(size = 15)	# Item 字号

	def __init__(self, control):

		# 初始化
		self.control = control
		self.initGraph()
		self.initGraphMatrix()

		# 显示方块
		self.draw()
		self.drawNext(self.control.generateNextBlock())

		# 监听键盘事件
		self.mainPanel.bind('<KeyPress>', self.onKeyboardEvent)

		# 建立方块下落线程
		self.autoFallThread = threading.Thread(target = self.autoRun, args = ())
		self.autoFallThread.setDaemon(True)
		self.autoFallThread.start()

		# 进入消息循环
		self.mainPanel.mainloop()
		
	# 界面初始化
	def initGraph(self):
		self.createStartWindow()	# 创建启动页面
		self.createMenuWindow()		# 创建菜单页面
		self.createGameWindow()		# 创建游戏界面
		self.createHelpPage()		# 创建帮助页面
		self.createPauseBox()		# 创建暂停提示框
		self.cv.pack()

	# 创建启动页面
	def createStartWindow(self):
		self.startCv = Canvas(
			self.mainPanel, 
			bg = 'black', 
			width = 640, 
			height = 480
		)
		self.startCv.create_rectangle(
			80, 100, 560, 200,  
			outline = 'white', 
			fill = 'black'
		)
		self.startCv.create_rectangle(
			83, 103, 557, 197,   
			outline = 'white', 
			fill = 'black'
		)
		self.startCv.create_rectangle(
			40, 400, 600, 420, 
			outline = 'white', 
			fill = 'black'
		)
		self.startCv.create_text(
			310, 130, 
			text = 'Tetris', 
			font = self.titleFont, 
			fill = 'white'
		)
		self.startCv.create_text(
			310, 180, 
			text = 'Loading...', 
			font = self.itemFont, 
			fill = 'white'
		)
		self.startWindow = self.cv.create_window(
			320, 240, 
			window = self.startCv, 
			state = HIDDEN
		)

	# 播放启动动画
	def runStartWindow(self):
		temp = []
		self.cv.itemconfig(
			self.startWindow, 
			state = NORMAL
		)
		for i in range(41, 600):
			temp.append(self.startCv.create_line(
				i, 401, i, 420,  
				fill = 'yellow'
			))
			time.sleep(0.001)
		time.sleep(1)
		self.cv.itemconfig(
			self.startWindow, 
			state = HIDDEN
		)
		self.cv.itemconfig(
			self.menuWindow, 
			state = NORMAL
		)
		for i in temp:
			self.startCv.delete(i)

	# 创建菜单页面
	def createMenuWindow(self):
		menuCv = Canvas(
			self.mainPanel, 
			bg = 'black', 
			width = 640, 
			height = 480
		)
		menuCv.create_rectangle(
			80, 100, 560, 200,  
			outline = 'white', 
			fill = 'black'
		)
		menuCv.create_rectangle(
			83, 103, 557, 197,   
			outline = 'white', 
			fill = 'black'
		)
		menuCv.create_text(
			310, 130, 
			text = 'Tetris', 
			font = self.titleFont, 
			fill = 'white'
		)
		menuCv.create_text(
			310, 180, 
			text = 'Menu', 
			font = self.itemFont, 
			fill = 'white'
		)
		menuCv.create_text(
			310, 250, 
			text = """\n\n(N)New game\n\n(H)Help\n\n(L)Load""", 
			font = self.itemFont, 
			fill = 'yellow'
		)
		self.menuWindow = self.cv.create_window(
			320, 240, 
			window = menuCv, 
			state = HIDDEN
		)

	# 创建帮助页面
	def createHelpPage(self):
		helpCv = Canvas(
			self.mainPanel, 
			bg = 'black', 
			width = 640, 
			height = 480
		)
		helpCv.create_text(
			310, 50, 
			text = "帮助", 
			font = self.titleFont, 
			fill = 'yellow'
		)
		helpCv.create_text(
			300, 200, 
			text = """
			\n ↑ ← ↓ → : .......用于控制方块移动方向
			\n N : ...........................开始新游戏
			\n H : .................................帮助
			\n P : .............................暂停游戏
			\n Esc : ...........................退出游戏
			\n L : .............................加载存档
			\n Ctrl + S : ......................保存游戏
			""", 
			font = self.itemFont, 
			fill = 'yellow'
		)
		helpCv.create_text(
			300, 400, 
			text = "Press any key to return...", 
			font = self.itemFont, 
			fill = 'yellow'
		)
		self.helpWindow = self.cv.create_window(
			320, 240, 
			window = helpCv, 
			state = HIDDEN
		)

	# 创建游戏界面
	def createGameWindow(self):
		self.gameCv = Canvas(
			self.mainPanel, 
			bg = 'black', 
			width = 640, 
			height = 480
		)
		# 双线主方框
		self.gameCv.create_rectangle(
			36, 36, 44 + 15 * 20, 44 + 20 * 20, 
			outline = 'lightgray', 
			fill = 'black'
		)
		self.gameCv.create_rectangle(
			39, 39, 41 + 15 * 20, 41 + 20 * 20,
			outline = 'lightgray', 
			fill = 'black'
		)

		# 下一方块提示框
		self.gameCv.create_rectangle(
			400, 40, 580, 140, 
			outline = 'white', 
			fill = 'black'
		)
		self.gameCv.create_text(
			425, 50, 
			text = 'Next:', 
			fill = 'white'
		)

		# 记分板
		self.gameCv.create_rectangle(
			400, 200, 580, 250, 
			outline = 'white', 
			fill = 'black'
		)
		self.gameCv.create_text(
			425, 210, 
			text = 'Score:', 
			fill = 'white'
		)
		self.scoreText = self.gameCv.create_text(
			475, 210, 
			text = str(self.control.getParameter()['score']), 
			fill = 'white'
		)
		self.gameWindow = self.cv.create_window(
			320, 240, 
			window = self.gameCv, 
			state = HIDDEN
		)

	# 创建暂停提示框
	def createPauseBox(self):
		pauseBoxCv = Canvas(
			self.mainPanel, 
			bg = 'black', 
			width = 220, 
			height = 50
		)
		pauseBoxCv.create_rectangle(
			4, 4, 219, 49, 
			outline = 'lightgreen', 
			fill = 'black'
		)
		pauseBoxCv.create_text(
			0, 25, 
			text = """
				         Pause
				Press P to continue
			""", 
			fill = 'lightgreen'
		)
		self.pauseBox = self.gameCv.create_window(
			490, 405, 
			window = pauseBoxCv, 
			state = HIDDEN
		)

	# 图像面板矩阵初始化
	def initGraphMatrix(self):
		parameter = self.control.getParameter()
		# 图像面板矩阵初始化
		for i in range(parameter['row']):	# 矩阵外围一圈为缓冲区
			self.graphMatrix.append([])
			for j in range(parameter['column']):
				rectangle = self.gameCv.create_rectangle(
					40 + j * 20, 40 + i * 20, 60 + j * 20, 60 + i * 20, 
					outline = 'black', 
					fill = 'cyan', 
					state = HIDDEN
				)
				self.graphMatrix[i].append(rectangle)

		# 下一方块面板矩阵初始化
		x, y = 470, 50		# 参考坐标
		for i in range(4):
			self.nextBlockMatrix.append([])
			for j in range(4):
				rectangle = self.gameCv.create_rectangle(
					x + j * 20, y + i * 20, x + 20 + j * 20, y + 20 + i * 20, 
					outline = 'black', 
					fill = 'cyan', 
					state = HIDDEN
				)
				self.nextBlockMatrix[i].append(rectangle)

	# 将主矩阵信息映射到图像面板矩阵
	def draw(self):
		parameter = self.control.getParameter()
		for i in range(parameter['row']):
			for j in range(parameter['column']):
				if parameter['matrix'][i + 1][j + 1] == 1:
					self.gameCv.itemconfig(
						self.graphMatrix[i][j], 
						state = NORMAL
					)
				elif parameter['matrix'][i + 1][j + 1] == 0:
					self.gameCv.itemconfig(
						self.graphMatrix[i][j], 
						state = HIDDEN
					)

	# 下一方块提示显示
	def drawNext(self, block):
		BlockMatrix = self.control.getBlockMatrix(block)
		for i in range(4):
			for j in range(4):
				if BlockMatrix[i][j] == 1:
					self.gameCv.itemconfig(
						self.nextBlockMatrix[i][j], 
						state = NORMAL
					)
				else:
					self.gameCv.itemconfig(
						self.nextBlockMatrix[i][j], 
						state = HIDDEN
					)

	# 暂停提示
	def showPauseBox(self, swich):
		if swich == 'On':
			self.gameCv.itemconfig(
				self.pauseBox, 
				state = NORMAL
			)
		else:
			self.gameCv.itemconfig(
				self.pauseBox, 
				state = HIDDEN
			)

	# 显示分数
	def showScore(self):
		self.gameCv.itemconfig(
			self.scoreText,  
			text = str(self.control.getParameter()['score']), 
			fill = 'white'
		)

	# 重启
	def restart(self):
		self.control.reset()
		self.cv.itemconfig(
			self.gameWindow, 
			state = HIDDEN
		)
		self.cv.itemconfig(
			self.menuWindow, 
			state = NORMAL
		)

	# 键盘事件处理函数
	def onKeyboardEvent(self, event):
		# 预先捕捉的事件处理
		if self.control.start == False:		# 进入帮助页
			if self.control.helpPage == False:
				if event.keysym == 'h' or event.keysym == 'H':
					self.control.helpPage = True
					self.cv.itemconfig(
						self.helpWindow, 
						state = NORMAL
					)
					return
			if self.control.helpPage == True:	# 退出帮助页
				self.control.helpPage = False
				self.cv.itemconfig(
					self.menuWindow, 
					state = NORMAL
				)
				self.cv.itemconfig(
					self.helpWindow, 
					state = HIDDEN
				)
				return
		if self.control.start == True:	# 捕获 Ctrl 状态

			if event.char == '\x13':
				operationInfo = self.control.operation(event.char)
			if self.control.pause == True:	# 暂停提示框
				self.showPauseBox('On')
			else:
				self.showPauseBox('Off')

		# 交给控制模块处理
		operationInfo = self.control.operation(event.keysym)
		self.draw()

		# 开始
		if self.control.start == True:

			self.drawNext(self.control.generateNextBlock())
			self.showScore()

			self.cv.itemconfig(
				self.menuWindow, 
				state = HIDDEN
			)
			self.cv.itemconfig(
				self.gameWindow, 
				state = NORMAL
			)

			# 方块已下降至最底
			if operationInfo['isBottom'] == 1:
				self.draw()
				self.showScore()

			# 暂停提示框
			if self.control.pause == True:
				self.showPauseBox('On')
			else:
				self.showPauseBox('Off')

		# 询问是否退出
		if operationInfo['Exit'] == True:
			if messagebox.askokcancel("Verify",'Do you really want to quit?'):
				os._exit(0)
			else:
				if self.control.start == True:
					self.control.pause = False
					self.control.stopThread = False
					self.showPauseBox('Off')

	# 自动下落函数
	def autoRun(self):
		while True:
			if self.startRun == False:
				self.runStartWindow()
				self.startRun = True
			while self.control.stopThread == True:
				time.sleep(0.001)
			while self.control.pause == False and self.control.start == True:
				self.draw()
				operationInfo = self.control.operation('Down', autoDown = True)
				if operationInfo['isBottom'] == 1:		# 方块已下降至最底
					self.draw()
					self.showScore()
					if self.control.getIsLose() != True:		# 未输
						self.control.nextBlock()
						self.drawNext(self.control.generateNextBlock())
						self.draw()
					else:		# 输
						messagebox.showinfo('Message', 'Game over!')
						self.restart()
				time.sleep(self.control.getParameter()['interval'])