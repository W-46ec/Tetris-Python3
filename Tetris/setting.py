matrixBuffer = 2						# 缓冲大小
row = 20								# 面板格子行数
column = 15								# 面板格子列数
matrixRow = row + matrixBuffer			# 矩阵行数
matrixColumn = column + matrixBuffer	# 矩阵列数

score = 0					# 分数
initInterval = 0.5			# 方块下落初始速度
interval = initInterval 	# 方块下落当前速度