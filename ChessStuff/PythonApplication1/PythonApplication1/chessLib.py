from chessTest import *
'''
board=genBoard()
print printBoardPersonal(board)
print "----------"
print GetPlayerPositions(board, 20)


print ""
print " Note 1: lower right hand square is WHITE"
print " Note 2: two upper rows are for BLACK PIECES"
print " Note 3: two lower rows are for WHITE PIECES"
'''

doneGame = False
while(True):
	if doneGame == True:
		break
	boardy = genBoard()
	print "Welcome to Chess. Please enter \"1\" for 2 human players, \"2\" for player vs dumb computer, \"3\" for player vs smart computer, or \"4\" to exit game."
	while (True):
		inputted = raw_input()
		if inputted == "1":
			playPVP(boardy)
			break
		elif inputted == "2":
			playPVC(boardy, 1)
			break
		elif inputted == "3":
			playPVC(boardy, 0)
			break
		elif inputted == "4":
			playCVC(boardy)
			break
		else:
			print "Please enter a valid input. Please enter \"1\" for 2 human players, \"2\" for player vs dumb computer, or \"3\" for player vs smart computer."
