#strategy:
#currently in long term: max/min, ensure they do not leave themselves in a check (return 0 if so), 
#ensure they are not killed (return 0 if so), if last layer of tree then do not leave player in a check or kill
#currently in immediate function: checks for immediate threat of check caused by move (aka if long term are all kills then don't play an immediate kill), checks for immediate win possibility
#technically currently gives a randomly losing move if in checkmate

#WHEN HAVE TIME: if in check then check for checkmate (analyze board)

from random import randint

#PLAYER FUNCTIONS
def chessPlayerDumb(board, player):
	status = True
	candidateMoves = []
	evalTree = None
	move = []
	try:
		possibleMoves = getPossibleSafeMoves(player, board)
		move = possibleMoves[randint(0,len(possibleMoves)-1)]
	except:
		status = False
	return [status, move, candidateMoves,evalTree]

#returns list of moves with their max possible guaranteed scores [[move, score],[move, score]]
def analyzeTree(gameTree, player):
	listy = []
	for moveTree in gameTree.store[1]:
		move = moveTree.store[0][2]#the moveToNode variable in the node of the tree
		score = analyzeTreeHelper(moveTree, player)
		listy += [[move, score + 50]]#the +5 is to differentiate between long term and immediate threat of death
	return listy

#returns max possible guaranteed score of that spot
def analyzeTreeHelper(gameTree, player):
	playerToNode = gameTree.store[0][0]
	scoreAtNode = gameTree.store[0][1]
	playerToNextNode = 0
	scoreDiff = 0
	if (player == 10):
		scoreDiff = scoreAtNode[0]-scoreAtNode[2]
	else:
		scoreDiff = scoreAtNode[2]-scoreAtNode[0]
	
	if playerToNode == 10:
		playerToNextNode = 20
	else:
		playerToNextNode = 10

	#check if player would leave themselves in a check, return 0 score if so
	if (playerToNode == player):
		if (player == 10 and scoreAtNode[1] == True):
			return -40
		elif (player == 20 and scoreAtNode[3] == True):
			return -40
	
	#check if this move would kill player, return 0 if so
	if player == 10 and scoreAtNode[4] == 20:#scoreAtNode[4] is a winning player
		return -40
	elif player == 20 and scoreAtNode[4] == 10:
		return -40

	#check if the player would capture the opponent's king, return score 95 if possible
	if player == 10 and scoreAtNode[4] == 10:#scoreAtNode[4] is a winning player
		return 40
	elif player == 20 and scoreAtNode[4] == 20:
		return 40

	#check if end of tree
	if len(gameTree.store[1]) == 0:
		#if final tree in a branch
		if player == 10: #return score of player 10
			if scoreAtNode[1] == True:#just in case check for check on last branch of tree, return 0 if so
				return -40
			return scoreDiff
		else: #return score of player 20
			if scoreAtNode[3] == True:
				return -40
			return scoreDiff
	
	if playerToNextNode == player:
		#player can get the maximum score path
		maxScore = -1
		for gameNode in gameTree.store[1]:
			tempScore = analyzeTreeHelper(gameNode, player)
			if (tempScore > maxScore):#new high score
				maxScore = tempScore
		return maxScore
	else:
		#opponent tries to make minimal score path
		minScore = 1000
		for gameNode in gameTree.store[1]:
			tempScore = analyzeTreeHelper(gameNode, player)
			if (tempScore < minScore):#new high score
				minScore = tempScore
		return minScore


def chessPlayer2(board, player):
	status = True
	move = None
	candidateMoves = None
	evalTree = None
	if (player == 10):
		playerToNextNode = 20
	else:
		playerToNextNode = 10
	try:
		gameTree = genChessTree(list(board), playerToNextNode, None, None, 1)
		candidateMoves = analyzeTree(gameTree, player)
		
		maxScore = -2
		move = []
		
		for movv in candidateMoves:#check for immediate threat of check
			tempBoard = movePiece(movv[0][0], movv[0][1], list(board))
			testScore = analyzeBoard(tempBoard)
			if (player == 10 and testScore[1] ==True) or (player == 20 and testScore[3] == True):
				movv[1] = -1 #immediate threat of check is not acceptable, thus make it 0 score

		for i in candidateMoves:#convert raw score to decimal and get the best move
			if i[1] > maxScore:
				move = i[0]
				maxScore = i[1]
			i[1] = float(i[1])/100 #marking scheme out of 50
		evalTree = gameTree.Get_LevelOrder()
	except:
		status = False
	return [status, move, candidateMoves,evalTree]

def genChessTree(boardAtNode, playerToNode, moveToNode, scoreAtNode, layerAtNode):
	treey = tree([playerToNode, scoreAtNode, moveToNode])
	nextPlayerToNode = 0
	if (playerToNode == 10):
		nextPlayerToNode = 20
	else:
		nextPlayerToNode = 10
	movesListy = getPossibleMoves(nextPlayerToNode, boardAtNode)
	layerAtNextNode = layerAtNode +1
	if (layerAtNode > 2 or len(movesListy) == 0 or (layerAtNode != 1 and scoreAtNode[4] != 0)):
		return treey
	for i in movesListy:
		nextBoard = movePiece(i[0], i[1], list(boardAtNode))
		scoreAtNextNode = analyzeBoard(nextBoard)
		tempTree = genChessTree(nextBoard, nextPlayerToNode, i, scoreAtNextNode, layerAtNextNode)
		treey.AddSuccessor(tempTree)
	return treey

#########################################################################
###PLAYER 2 TEST FUNCTIONS
def analyzeBoard2(board):
	#returned variables:
	scoreWhite = 0
	scoreBlack = 0
	playerInWin = 0
	playerInCheck = 0

	#temp only in function variables:
	blackInCheck = True
	whiteInCheck = True
	whiteWin = True
	blackWin = True

	KnightTable = [-50,-40,-30,-30,-30,-30,-40,-50,
		-40,-20,  0,  0,  0,  0,-20,-40,
		-30,  0, 10, 15, 15, 10,  0,-30,
		-30,  5, 15, 20, 20, 15,  5,-30,
		-30,  0, 15, 20, 20, 15,  0,-30,
		-30,  5, 10, 15, 15, 10,  5,-30,
		-40,-20,  0,  5,  5,  0,-20,-40,
		-50,-40,-20,-30,-30,-20,-40,-50]

	BishopTable = [
		-20,-10,-10,-10,-10,-10,-10,-20,
		-10,  0,  0,  0,  0,  0,  0,-10,
		-10,  0,  5, 10, 10,  5,  0,-10,
		-10,  5,  5, 10, 10,  5,  5,-10,
		-10,  0, 10, 10, 10, 10,  0,-10,
		-10, 10, 10, 10, 10, 10, 10,-10,
		-10,  5,  0,  0,  0,  0,  5,-10,
		-20,-10,-40,-10,-10,-40,-10,-20]

	PawnTable = [
		 0,  0,  0,  0,  0,  0,  0,  0,
		50, 50, 50, 50, 50, 50, 50, 50,
		10, 10, 20, 30, 30, 20, 10, 10,
		 5,  5, 10, 27, 27, 10,  5,  5,
		 0,  0,  0, 25, 25,  0,  0,  0,
		 5, -5,-10,  0,  0,-10, -5,  5,
		 5, 10, 10,-25,-25, 10, 10,  5,
		 0,  0,  0,  0,  0,  0,  0,  0
	]
	for pos in range(64):
		posPlay = posPlayer(pos, board)
		if posPlay == 10:
			pieceType = board[pos]-10
			if pieceType == 0: #pawn
				scoreWhite += 100
				scoreWhite += PawnTable[convertPos(posPlay, pos)]
			elif pieceType == 1: #knight
				scoreWhite += 320
				scoreWhite += KnightTable[convertPos(posPlay, pos)]
			elif pieceType == 2: #bishop
				scoreWhite +=325
				scoreWhite += BishopTable[convertPos(posPlay, pos)]
			elif pieceType == 3: #rook
				scoreWhite += 500
			elif pieceType == 4: #queen
				scoreWhite += 975
			elif pieceType == 5: #king
				blackWin = False
				whiteInCheck = IsPositionUnderThreat(board,pos,posPlay)
		elif posPlay == 20:
			pieceType = board[pos]-20
			if pieceType == 0: #pawn
				scoreBlack += 100
				scoreBlack += PawnTable[convertPos(posPlay, pos)]
			elif pieceType == 1: #knight
				scoreBlack += 320
				scoreBlack += KnightTable[convertPos(posPlay, pos)]
			elif pieceType == 2: #bishop
				scoreBlack += 325
				scoreBlack += BishopTable[convertPos(posPlay, pos)]
			elif pieceType == 3: #rook
				scoreBlack += 500
			elif pieceType == 4: #queen
				scoreBlack += 975
			elif pieceType == 5: #king
				whiteWin = False
				blackInCheck = IsPositionUnderThreat(board,pos,posPlay)
	
	#WHEN HAVE TIME: if incheck then check for checkmate

	if blackWin == True:
		playerInWin = 20
		scoreWhite = 0
	elif whiteWin == True:
		playerInWin = 10
		scoreBlack = 0
	return [scoreWhite, whiteInCheck, scoreBlack, blackInCheck, playerInWin]

def makeNebuScore(scores, playerToNode, player):
	###OUT OF 5000
	scoreDiff = 0
	if (player == 10):
		scoreDiff = scores[0]- scores[2]
	else:
		scoreDiff = scores[2]-scores[0]
	
	if playerToNode == 10:
		playerToNextNode = 20
	else:
		playerToNextNode = 10

	#check if player would leave themselves in a check, return 0 score if so
	if (playerToNode == player):
		if (player == 10 and scores[1] == True):
			return -float(4000)/5000
		elif (player == 20 and scores[3] == True):
			return -float(4000)/5000
	
	#check if this move would kill player, return 0 if so
	if player == 10 and scores[4] == 20:#scores[4] is a winning player
		return -float(4000)/5000
	elif player == 20 and scores[4] == 10:
		return -float(4000)/5000

	#check if the player would capture the opponent's king, return score 95 if possible
	if player == 10 and scores[4] == 10:#scores[4] is a winning player
		return float(4900)/5000
	elif player == 20 and scores[4] == 20:
		return float(4900)/5000

	return float(scoreDiff)/5000

def convertPos(player, pos):
	if player == 10:
		return 63-pos
	else:
		coors = genCoor(pos)
		coors[1] = 7-coors[1]
		pos = genPos(coors[0], coors[1])
		return 63-pos

def chessPlayer(board, player):
	status = True
	move = None
	candidateMoves = None
	evalTree = None
	if (player == 10):
		playerToNextNode = 20
	else:
		playerToNextNode = 10
	try:
		gameTree = genChessTree2(list(board), playerToNextNode, None, None, 1)
		candidateMoves = analyzeTree2(gameTree, player)
		
		maxScore = -1
		move = []
		
		for movv in candidateMoves:#check for immediate threat of check
			tempBoard = movePiece(movv[0][0], movv[0][1], list(board))
			testScore = analyzeBoard2(tempBoard)
			if (player == 10 and testScore[1] ==True) or (player == 20 and testScore[3] == True):
				movv[1] = 0 #immediate threat of check is not acceptable, thus make it 0 score

		for i in candidateMoves:#convert raw score to decimal and get the best move
			if i[1] > maxScore:
				move = i[0]
				maxScore = i[1]
		evalTree = gameTree.Get_LevelOrder()
	except:
		status = False
	return [status, move, candidateMoves,evalTree]

def genChessTree2(boardAtNode, playerToNode, moveToNode, scoreAtNode, layerAtNode):
	treey = tree([playerToNode, scoreAtNode, moveToNode])
	nextPlayerToNode = 0
	if (playerToNode  == 10):
		nextPlayerToNode = 20
	else:
		nextPlayerToNode = 10
	movesListy = getPossibleMoves(nextPlayerToNode, boardAtNode)
	layerAtNextNode = layerAtNode +1
	if (layerAtNode > 2 or len(movesListy) == 0 or (layerAtNode != 1 and scoreAtNode[4] != 0)):#the main levels
		return treey
	for i in movesListy:
		nextBoard = movePiece(i[0], i[1], list(boardAtNode))
		scoreAtNextNode = analyzeBoard2(nextBoard)
		tempTree = genChessTree2(nextBoard, nextPlayerToNode, i, scoreAtNextNode, layerAtNextNode)
		treey.AddSuccessor(tempTree)
	return treey


#returns list of moves with their max possible guaranteed scores [[move, score],[move, score]]
def analyzeTree2(gameTree, player):
	listy = []
	for moveTree in gameTree.store[1]:
		move = moveTree.store[0][2]#the moveToNode variable in the node of the tree
		score = analyzeTreeHelper2(moveTree, player, -1, 1000000)
		listy += [[move, score]]#the +5 is to differentiate between long term and immediate threat of death
	return listy

#returns max possible guaranteed score of that spot
def analyzeTreeHelper2(gameTree, player, alpha, beta):
	playerToNode = gameTree.store[0][0]
	scoreAtNode = gameTree.store[0][1]
	playerToNextNode = 0
	scory = makeNebuScore(scoreAtNode, playerToNode, player)
	if (playerToNode  == 10):
		nextPlayerToNode = 20
	else:
		nextPlayerToNode = 10
	#check if end of tree
	if len(gameTree.store[1]) == 0:
		#if final tree in a branch
		if player == 10: #return score of player 10
			if scoreAtNode[1] == True:#just in case check for check on last branch of tree, return 0 if so
				return -float(4000)/5000
			return scory
		else: #return score of player 20
			if scoreAtNode[3] == True:
				return -float(4000)/5000
			return scory
	
	if playerToNextNode == player:
		#player can get the maximum score path
		maxScore = -1
		for gameNode in gameTree.store[1]:
			tempScore = analyzeTreeHelper2(gameNode, player, alpha, beta)
			maxScore = max(tempScore, maxScore)
			beta = max(beta, maxScore)
			if (beta>=alpha):
				break
		return maxScore
	else:
		#opponent tries to make minimal score path
		minScore = 1000000
		for gameNode in gameTree.store[1]:
			tempScore = analyzeTreeHelper2(gameNode, player, alpha, beta)
			minScore = min(tempScore, minScore)
			beta = min(beta, minScore)
			if (beta>=alpha):
				break
		return minScore
###END OF TEST PLAYER 2
################################

###GAMEPLAY FUNCTIONS
def playPVP(board):
	player = 10
	while (True):
		
		if player == 10:
			printy = "WHITE"
		else:
			printy = "BLACK"
		
		print "Player " + printy + ", please enter the position of the next piece you want to move. The board is shown below."
		startPos = -1
		endPos = -1
		while (True):
			print printBoardPersonal(board)
			inputted = raw_input()
			if (isValidPiece(inputted, player, board) == False):
				print "Player, "+printy+", please enter a valid board spot of a piece that can move. The board is shown below."
			else:
				startPos = int(inputted)
				break
		print "Player " + printy + ", please enter the position of where you want to move to. The possible move locations are:"
		print GetPieceLegalMoves(board, startPos)
		
		print "The board is shown below."
		while (True):
			print printBoardPersonal(board)
			inputted = raw_input()
			if (isValidMove(startPos, inputted, player, board) == False):
				print "Player, "+printy+", please enter a valid board spot. The board is shown below."
			else:
				endPos = int(inputted)
				#move piece from startPos to endPos
				board = movePiece(startPos, endPos, board)
				break
		
		#returns [int whitescore, bool whiteincheck, int blackscore, bool blackincheck, int playerinwin]	
		scores = analyzeBoard(board)
		print "\nBOARD AFTER MOVE:"
		print printBoardPersonal(board)
		print "Current score of player WHITE: "+ str(scores[0]) + " and BLACK: " + str(scores[2])
		print "WHITE in check: "+ str(scores[1]) + " and BLACK in check: " + str(scores[3])
		
		if (scores[4] == 10 ):
			print "!!!Player WHITE Won!!!"
			printBoardPersonal(board)
			break
		elif (scores[4] == 20):
			print "!!!Player BLACK Won!!!"
			printBoardPersonal(board)
			break
		
		print "NEXT TURN---------------------------------------------------"

		if (player == 10):
			player = 20
		else:
			player = 10

def playPVC(board, dumbness):
	player = 10
	print "Please enter \"W\" if you want to be WHITE and go first, and \"B\" if you want to be BLACK and go second."
	human = 0
	computer = 0
	while (True):
		inputted = raw_input()
		if (inputted == "W"):
			human = 10
			computer = 20
			break
		elif (inputted == "B"):
			human = 20
			computer = 10
			break
		else:
			print "Please enter valid entry (\"W\" or \"B\")!"
	
	while (True):
		if player == 10:
			printy = "WHITE"
		else:
			printy = "BLACK"
		if (player == human):
			print "Player " + printy + ", please enter the position of the next piece you want to move. The board is shown below."
			startPos = -1
			endPos = -1
			while (True):
				print printBoardPersonal(board)
				inputted = raw_input()
				if (isValidPiece(inputted, player, board) == False):
					print "Player, "+printy+", please enter a valid board spot of a piece that can move. The board is shown below."
				else:
					startPos = int(inputted)
					break
			print "Player " + printy + ", please enter the position of where you want to move to. The possible move locations are:"
			print GetPieceLegalMoves(board, startPos)
		
			print "The board is shown below."
			while (True):
				print printBoardPersonal(board)
				inputted = raw_input()
				if (isValidMove(startPos, inputted, player, board) == False):
					print "Player, "+printy+", please enter a valid board spot. The board is shown below."
				else:
					endPos = int(inputted)
					#move piece from startPos to endPos
					board = movePiece(startPos, endPos, board)
					break
		elif(player == computer):
			print "Computer plays as follows"
			computerMoveList = []
			if (dumbness == 1):
				computerMoveList = chessPlayerDumb(board,player)
			elif (dumbness == 0):
				computerMoveList = chessPlayer2(board, player)
			print "Computer's move:" + str(computerMoveList[1])
			board = movePiece(computerMoveList[1][0], computerMoveList[1][1], board)
			
		scores = analyzeBoard(board)
		print "\nBOARD AFTER MOVE:"
		print printBoardPersonal(board)
		print "Current score of player WHITE: "+ str(scores[0]) + " and BLACK: " + str(scores[2])
		print "WHITE in check: "+ str(scores[1]) + " and BLACK in check: " + str(scores[3])
		
		if (scores[4] == 10 ):
			print "!!!Player WHITE Won!!!"
			printBoardPersonal(board)
			break
		elif (scores[4] == 20):
			print "!!!Player BLACK Won!!!"
			printBoardPersonal(board)
			break
		
		print "NEXT TURN---------------------------------------------------"
		
		if (player == 10):
			player = 20
		else:
			player = 10

def playCVC(board):
	player = 10
	
	while (True):
		if player == 10:
			printy = "WHITE"
		else:
			printy = "BLACK"
		if (player == 10):
			print "Computer WHITE plays as follows"
			computerMoveList = []
			computerMoveList = chessPlayer(board,player)
			print "Computer's move:" + str(computerMoveList[1])
			board = movePiece(computerMoveList[1][0], computerMoveList[1][1], board)

		elif(player == 20):
			print "Computer BLACK plays as follows"
			computerMoveList = []
			computerMoveList = chessPlayer2(board, player)
			print "Computer's move:" + str(computerMoveList[1])
			board = movePiece(computerMoveList[1][0], computerMoveList[1][1], board)
			
		scores = analyzeBoard(board)
		print "\nBOARD AFTER MOVE:"
		print printBoardPersonal(board)
		print "Current score of player WHITE: "+ str(scores[0]) + " and BLACK: " + str(scores[2])
		print "WHITE in check: "+ str(scores[1]) + " and BLACK in check: " + str(scores[3])
		
		if (scores[4] == 10 ):
			print "!!!Player WHITE Won!!!"
			printBoardPersonal(board)
			break
		elif (scores[4] == 20):
			print "!!!Player BLACK Won!!!"
			printBoardPersonal(board)
			break
		
		print "NEXT TURN---------------------------------------------------"
		
		if (player == 10):
			player = 20
		else:
			player = 10

#assumes error checking completed.
def movePiece(startPos, endPos, board):
	board[endPos] = board[startPos]
	board[startPos] = 0
	return board

##########################

####IMPORTANT BOARD FUNCTIONS
def genBoard():
	r=[0 for i in range(64)]
	White=10
	Black=20
	for i in [ White, Black ]:
		if i==White:
			factor=+1
			shift=0
		else:
			factor=-1
			shift=63

		r[shift+factor*7] = r[shift+factor*0] = i+getPiece("rook")
		r[shift+factor*6] = r[shift+factor*1] = i+getPiece("knight")
		r[shift+factor*5] = r[shift+factor*2] = i+getPiece("bishop")
		if i==White:
			r[shift+factor*4] = i+getPiece("queen") # queen is on its own color square
			r[shift+factor*3] = i+getPiece("king")
		else:
			r[shift+factor*3] = i+getPiece("queen") # queen is on its own color square
			r[shift+factor*4] = i+getPiece("king")

		for j in range(0,8):
			r[shift+factor*(j+8)] = i+getPiece("pawn")

	return r

def printBoard(board):
	accum="---- BLACK SIDE ----\n"
	max=63
	for j in range(0,8,1):
		for i in range(max-j*8,max-j*8-8,-1):
			accum=accum+'{0: <5}'.format(board[i])
		accum=accum+"\n"
	accum=accum+"---- WHITE SIDE ----"
	return accum

def printBoardPersonal(board):
	accum="---- BLACK SIDE ----\n"
	max=63
	for j in range(0,8,1):
		for i in range(max-j*8,max-j*8-8,-1):
			piece = board[i]
			if piece == 10 or piece == 11 or piece == 12 or piece == 13 or piece == 14 or piece == 15 or piece == 20 or piece == 21 or piece == 22 or piece == 23 or piece == 24 or piece == 25:
				accum=accum+'{0: <5}'.format(getSpotName(board[i]))
			else:
				accum=accum+'{0: <5}'.format(i)
		accum=accum+"\n"
	accum=accum+"---- WHITE SIDE ----"
	return accum

###RECOMMENDED ASSIGNED FUNCTIONS

def GetPieceLegalMoves(board,position):
	listy = []
	if position < 0 or position > 63:
		return []
	if board[position] == 0:
		return []
	
	#get info about the position and player
	player = posPlayer(position, board)
	coords = genCoor(position)
	xOriginal = coords[0]
	yOriginal = coords[1]

	if board[position]%10 == getPiece("bishop"):
		listy = checkBishopMoves(xOriginal, yOriginal, player, board)
	elif board[position]%10 == getPiece("rook"):
		listy = checkRookMoves(xOriginal, yOriginal, player, board)
	elif board[position]%10 == getPiece("queen"):
		listy = checkQueenMoves(xOriginal, yOriginal, player, board)
	elif board[position]%10 == getPiece("king"):
		listy = checkKingMoves(xOriginal, yOriginal, player, board)
	elif board[position]%10 == getPiece("knight"):
		listy = checkKnightMoves(xOriginal, yOriginal, player, board)
	elif board[position]%10 == getPiece("pawn"):
		listy = checkPawnMoves(xOriginal, yOriginal, player, board)
	return listy

#player is the threatENED
def IsPositionUnderThreat(board,position,player):
	for pos in range(64):
		posPlay = posPlayer(pos, board)
		if (posPlay != 0 and posPlay != player):
			positions = GetPieceLegalMoves(board, pos)
			for i in positions:
				if position == i:
					return True
	return False

#returns [int whitescore, bool whiteincheck, int blackscore, bool blackincheck, int playerinwin]
def analyzeBoard(board):
	#returned variables:
	scoreWhite = 0
	scoreBlack = 0
	playerInWin = 0
	playerInCheck = 0

	#temp only in function variables:
	blackInCheck = True
	whiteInCheck = True
	whiteWin = True
	blackWin = True

	for pos in range(64):
		posPlay = posPlayer(pos, board)
		if posPlay == 10:
			pieceType = board[pos]-10
			if pieceType == 0: #pawn
				scoreWhite += 1
			elif pieceType == 1: #knight
				scoreWhite += 3
			elif pieceType == 2: #bishop
				scoreWhite += 3
			elif pieceType == 3: #rook
				scoreWhite += 5
			elif pieceType == 4: #queen
				scoreWhite += 9
			elif pieceType == 5: #king
				blackWin = False
				whiteInCheck = IsPositionUnderThreat(board,pos,posPlay)
		elif posPlay == 20:
			pieceType = board[pos]-20
			if pieceType == 0: #pawn
				scoreBlack += 1
			elif pieceType == 1: #knight
				scoreBlack += 3
			elif pieceType == 2: #bishop
				scoreBlack += 3
			elif pieceType == 3: #rook
				scoreBlack += 5
			elif pieceType == 4: #queen
				scoreBlack += 9
			elif pieceType == 5: #king
				whiteWin = False
				blackInCheck = IsPositionUnderThreat(board,pos,posPlay)
	
	#WHEN HAVE TIME: if incheck then check for checkmate
	
	if blackWin == True:
		playerInWin = 20
		scoreWhite = 0
	elif whiteWin == True:
		playerInWin = 10
		scoreBlack = 0
	return [scoreWhite, whiteInCheck, scoreBlack, blackInCheck, playerInWin]

#returns list of moves
def getPossibleMoves(player, board):
	moves = []
	L = GetPlayerPositions(board, player)
	for position in L:
		posMoves = GetPieceLegalMoves(board, position)
		for i in posMoves:
			moves += [[position,i]]
	return moves

def getPossibleSafeMoves(player, board):
	moves = []
	L = GetPlayerPositions(board, player)
	for position in L:
		posMoves = GetPieceLegalMoves(board, position)
		for i in posMoves:
			if not IsPositionUnderThreat(board, i, player):
				moves += [[position,i]]
	return moves

def GetPlayerPositions(board,player):
	returner = []
	counter = 0
	for i in range(64):
		if posPlayer(i, board) == player:
			returner +=[i]
	return returner

################
######Small helpful functions
#gen position on board given x and y
#where x is 0 to 7 and y is 0 to 7 
def genPos(x,y):
	return x+y*8
def min(x,y):
	if x<=y:
		return x
	else:
		return y
def max(x,y):
	if x >= y:
		return x
	else:
		return y
#opposite of genPos	
def genCoor(pos):
	return [pos%8, pos/8]

#the player on the board
def posPlayer(position, board):
	return (board[position]/10)*10

#checks whether position is on board
def onBoard2(x,y):
	if x>-1 and x<8 and y < 8 and y > -1:
		return True
	else:
		return False

#gives the number of the piece name
def getPiece(name):
	if name=="pawn":
		return 0
	elif name=="knight":
		return 1
	elif name=="bishop":
		return 2
	elif name=="rook":
		return 3
	elif name=="queen":
		return 4
	elif name=="king":
		return 5
	else:
		return -1

def getSpotName(number):
	if number == 10:
		return "wP"
	elif number == 11:
		return "wN"
	elif number == 12:
		return "wB"
	elif number == 13:
		return "wR"
	elif number == 14:
		return "wQ"
	elif number == 15:
		return "wK"
	elif number == 20:
		return "bP"
	elif number == 21:
		return "bN"
	elif number == 22:
		return "bB"
	elif number == 23:
		return "bR"
	elif number == 24:
		return "bQ"
	elif number == 25:
		return "bK"
	else:
		return ""

#says whether player's piece is valid
def isValidPiece(inputted, player, board):
	try:
		if (int(inputted)>-1 and int(inputted)<64 and posPlayer(int(inputted), board) == player):
			#check if piece can move
			if len(GetPieceLegalMoves(board, int(inputted)))>0:
				return True
	except:
		return False
	return False

#says whether player's move on a piece at piecePosition is valid
def isValidMove(piecePosition, move, player, board):
	try:
		if (int(move)>-1 and int(move)<64):
			moves = GetPieceLegalMoves(board, piecePosition)
			for i in moves:
				if int(move) == i:
					return True
			return False
		else:
			return False
	except:
		return False
#################

#####Board checking helpers
#bishop
def checkBishopMoves(xOriginal, yOriginal, player, board):
	listy = []
	for i in range(4):
		x = xOriginal
		y = yOriginal
		while True:
			if i == 0:
				x+=1
				y+=1
			elif i == 1:
				x+=1
				y-=1
			elif i == 2:
				x-=1
				y+=1
			elif i == 3:
				x-=1
				y-=1
			pos = genPos(x,y)
			if onBoard2(x,y) == False:
				break
			posPlay = posPlayer(pos, board)
			if posPlay == player:
				break
			if posPlay != 0 and posPlay != player:
				listy += [pos]
				break
			listy += [pos]
	return listy

def checkRookMoves(xOriginal, yOriginal, player, board):
	listy = []
	for i in range(4):
		x = xOriginal
		y = yOriginal
		while True:
			if i == 0:
				x+=1
			elif i == 1:
				x-=1
			elif i == 2:
				y+=1
			elif i == 3:
				y-=1
			pos = genPos(x,y)
			if onBoard2(x,y) == False:
				break
			posPlay = posPlayer(pos, board)
			if posPlay == player:
				break
			if posPlay != 0 and posPlay != player:
				listy += [pos]
				break
			listy += [pos]
	return listy

def checkQueenMoves(xOriginal, yOriginal, player, board):
	listy = []
	for i in range(8):
		x = xOriginal
		y = yOriginal
		while True:
			if i == 0:
				x+=1
				y+=1
			elif i == 1:
				x+=1
				y-=1
			elif i == 2:
				x-=1
				y+=1
			elif i == 3:
				x-=1
				y-=1
			elif i == 4:
				x+=1
			elif i == 5:
				y+=1
			elif i == 6:
				x-=1
			elif i == 7:
				y-=1
			pos = genPos(x,y)
			if onBoard2(x,y) == False:
				break
			posPlay = posPlayer(pos, board)
			if posPlay == player:
				break
			if posPlay != 0 and posPlay != player:
				listy += [pos]
				break
			listy += [pos]
	return listy

def checkKingMoves(xOriginal, yOriginal, player, board):
	listy = []
	for i in range(8):
		x = xOriginal
		y = yOriginal
		if i == 0:
			x+=1
			y+=1
		elif i == 1:
			x+=1
			y-=1
		elif i == 2:
			x-=1
			y+=1
		elif i == 3:
			x-=1
			y-=1
		elif i == 4:
			x+=1
		elif i == 5:
			y+=1
		elif i == 6:
			x-=1
		elif i == 7:
			y-=1
		pos = genPos(x,y)
		if onBoard2(x,y)==True:
			posPlay = posPlayer(pos, board)
			if posPlay != player:
				listy += [pos]
	return listy

def checkKnightMoves(xOriginal, yOriginal, player, board):
	listy = []
	for i in range(8):
		x = xOriginal
		y = yOriginal
		if i == 0:
			x+=1
			y+=2
		elif i == 1:
			x+=2
			y+=1
		elif i == 2:
			x+=1
			y-=2
		elif i == 3:
			x+=2
			y-=1
		elif i == 4:
			x-=1
			y+=2			
		elif i == 5:
			x-=2
			y+=1
		elif i == 6:
			x-=1
			y-=2
		elif i == 7:
			x-=2
			y-=1
		pos = genPos(x,y)
		if onBoard2(x,y)==True:
			posPlay = posPlayer(pos, board)
			if posPlay != player:
				listy += [pos]
	return listy

#Check if can actually go off board!!!!!
def checkPawnMoves(xOriginal, yOriginal, player, board):
	listy = []
	direction = 0
	if player == 10:
		direction = 1
	else:
		direction = -1

	pos = genPos(xOriginal,yOriginal+direction)
	if onBoard2(xOriginal,yOriginal+direction) == False:
		return []#check if can actually go off board
	elif posPlayer(pos, board) == 0:
		listy += [pos]
	
	pos = genPos(xOriginal+1,yOriginal+direction)
	if onBoard2(xOriginal,yOriginal+direction) == True:
		pieceOnDiag = posPlayer(pos, board)
		if pieceOnDiag != 0 and pieceOnDiag != player:
			listy += [pos]

	pos = genPos(xOriginal-1,yOriginal+direction)
	if onBoard2(xOriginal-1,yOriginal+direction) == True:
		pieceOnDiag = posPlayer(pos, board)
		if pieceOnDiag != 0 and pieceOnDiag != player:
			listy += [pos]
	return listy

class tree:
	def __init__(self,x):
		self.store = [x,[]]

	def AddSuccessor(self,x):
		self.store[1] = self.store[1] + [x]
		return True

	def Print_DepthFirst(self):
		self.Print_DepthFirstInner(0)

	def Print_DepthFirstInner(self, indent):
		stringy = ""
		for i in range(indent):
			stringy += "    "
		print self.store[0][1].printBoard()
		for i in self.store[1]:
			i.Print_DepthFirstInner(indent+1)

	def Get_LevelOrder(self):
		queuey = queue()
		queuey.enqueue(self)
		listy = []
		while(queuey.peek()!= False):
			dequeued = queuey.dequeue()
			listy += [dequeued.store[0]]
			if (len(dequeued.store[1])!= 0):
				for i in dequeued.store[1]:
					queuey.enqueue(i)
		return listy

class queue:
	def __init__(self):
		self.listy = []

	def enqueue(self, num):
		self.listy += [num]

	def dequeue(self):
		if (len(self.listy))>0:
			temp = self.listy[0]
			del self.listy[0]
			return temp
		else:
			return False

	def peek(self):
		if (len(self.listy))>0:
			return self.listy[0]
		else:
			return False