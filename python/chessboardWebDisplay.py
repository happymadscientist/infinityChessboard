from bokeh.plotting import figure, show, curdoc
from bokeh.models import TapTool

from string import ascii_uppercase, ascii_lowercase
import numpy as np

from textHandler import textHandler
texter = textHandler()

class chessboardWebDisplay:

	def __init__(self):
		self.verbose = 0
		self.setupBoardVariables()
		self.setupMasterBoardWindow()

	def log(self,messageType,messageData,priority = "INFO"):
		if self.verbose:
			print (priority,"-",messageType,"-",messageData)

	#####SETUP FUNCTIONS###############
	def setupBoardVariables(self):
		self.figureSize = 880

		self.numRows = 8
		self.numCols = 8
		self.ledSize = 1
		self.ledSpacing = 1.15
		self.squareSize = self.ledSpacing*6
		self.ledColors = ["green"] * 16 * self.numRows * self.numCols
		self.squareColors = ["green"] * self.numRows * self.numCols

	def setupMasterBoardWindow(self):
		#creates the main display window which shows squares and leds
		xRange = (-self.ledSize/2,6*self.ledSpacing*self.numCols - self.ledSize/2)
		yRange = (-self.ledSize/2,6*self.ledSpacing*self.numRows - self.ledSize/2)

		boardWindow = figure(plot_width=self.figureSize, plot_height=self.figureSize,
			x_range = xRange,y_range = yRange,toolbar_location=None,
			name = "board window",tools="",output_backend="webgl")

		boardWindow.grid.visible = False
		boardWindow.axis.visible = False

		ledXs = np.array([])
		ledYs = np.array([])

		for xInd in range(self.numCols):
			for yInd in range(self.numRows):
				x,y = self.generateLedCoords(self.ledSpacing,xInd,yInd)
				ledXs = np.append(ledXs,x)
				ledYs = np.append(ledYs,y)

		#draw the gridlines
		xTicks = np.linspace(xRange[0],xRange[1],self.numCols+1)
		yTicks = np.linspace(yRange[0],yRange[1],self.numRows+1)

		lineXs,lineYs = self.generateGridLineCoords(xTicks,yTicks)

		boardWindow.multi_line(xs=lineXs, ys=lineYs, line_color="#8073ac", line_width=2)

		squareSizeMod = .9
		offset = 1 - squareSizeMod

		squareCoords = self.generateSquareCoords(self.numRows)
		squareXs = (squareCoords[:,0])
		squareYs = (squareCoords[:,1])

		# xRange = (offset,(self.squareSize * self.numRows) - offset)
		# yRange = (offset,(self.squareSize * self.numCols) - offset)

		self.leds = boardWindow.rect(x=ledXs, y=ledYs, 
			width=self.ledSize, height=self.ledSize,
			color=self.ledColors,angle=0, height_units="data",
			fill_alpha=.5)

		self.squares = boardWindow.rect(x=squareXs, y=squareYs, 
			width=self.squareSize*squareSizeMod, height=self.squareSize*squareSizeMod, 
			color=self.squareColors, angle=0, height_units="data",
			fill_alpha=.5)

		#set these equal so the board doesn't go dark when a single led/square is clicked
		self.squares.nonselection_glyph = self.squares.selection_glyph
		self.leds.nonselection_glyph = self.leds.selection_glyph

		self.boardSelectTool= TapTool(renderers = [self.squares,self.leds])

		#set squares visible at start
		# self.squares.visible = False
		self.leds.visible = False

		boardWindow.add_tools(self.boardSelectTool)
		boardWindow.toolbar.active_tap = self.boardSelectTool

		self.boardWindow = boardWindow

	def generateGridLineCoords(self,xTicks,yTicks):
		#generates coordinates for a grid
		boardWidth, boardHeight = xTicks[-1], yTicks[-1]

		lineXs = []
		lineYs = []

		for xTick in xTicks:
			xCoords = [xTick,xTick]
			yCoords = [0,boardHeight]

			lineXs.append(xCoords)
			lineYs.append(yCoords)

		for yTick in yTicks:
			xCoords = [0,boardWidth]
			yCoords = [yTick,yTick]

			lineXs.append(xCoords)
			lineYs.append(yCoords)

		return lineXs,lineYs

	def generateSquareCoords(self,numSquares):
		squareCenter = np.array((self.squareSize,self.squareSize))/2
		squareCoords = []
		for x in range(numSquares):
			for y in range(numSquares):
				squareCoord = squareCenter + (x*self.squareSize,0) + (0,y*self.squareSize)
				squareCoords.append(squareCoord)

		return (np.array((squareCoords)))

	def generateLedCoords(self,squareSpacing,rowNum,colNum):
		masterSquareSpace = 6*squareSpacing
		squareMatrix = np.array([
			[0,1,1,1,1,0],
			[1,0,0,0,0,1],
			[1,0,0,0,0,1],
			[1,0,0,0,0,1],
			[1,0,0,0,0,1],
			[0,1,1,1,1,0]
			])

		xs,ys = np.where(squareMatrix)
		ys = (ys * squareSpacing) + (masterSquareSpace * colNum)
		xs = (xs * squareSpacing) + (masterSquareSpace * rowNum)
		return (xs,ys)


	#####CONTROL FUNCTIONS###########
	def assignSquareClickToFunction(self,functionIn):
		self.squares.data_source.selected.on_change("indices",functionIn)

	def assignLedClickToFunction(self,functionIn):
		self.leds.data_source.selected.on_change("indices",functionIn)

	def writeBackground(self,color,squares):
		#if squares, writes all sqaures to the color, else writes all leds as color
		if squares:	self.bulkSquareColorWrite( [color] * 64 )
		else: self.bulkLedColorWrite( [color] * 1024 )

	def toggleVisibility(self,squaresVisible):
		#changes whether the square or the leds are visible
		self.log("Toggle visibility",squaresVisible)
		self.leds.visible = not squaresVisible
		self.squares.visible = bool(squaresVisible)

	def changeBrightness(self,newBrightness):
		self.log("Change brightness", newBrightness)
		self.squares.glyph.fill_alpha = newBrightness
		self.leds.glyph.fill_alpha = newBrightness

		# self.squares.selection_glyph.fill_alpha = newBrightness
		# self.leds.nonselection_glyph.fill_alpha = newBrightness

	## Square mode functions
	def writeSquareToColor(self,squareIndex,color):
		#changes the square at squareIndex to color (and bulk updates the values to trigger a graphics change)
		self.log("Single Square",(squareIndex,color))
		existingColors = self.squares.data_source.data["fill_color"]
		existingColors[squareIndex] = color

		self.squares.data_source.data["fill_color"] = existingColors

	def bulkSquareColorWrite(self,newColors):
		#updates every square on the board
		self.log("Bulk Square",newColors)
		self.squares.data_source.data["fill_color"] = newColors

	### LED Mode functions
	def bulkLedColorWrite(self,newColors):
		self.log("Bulk LED",newColors)
		self.leds.data_source.data["fill_color"] = newColors

	def writeLedToColor(self,ledIndex,color):
		#changes the color of the led at ledIndex to color (and bulk updates the color array to trigger the graphics change)
		self.log("Single LED",(ledIndex,color))

		existingColors = self.leds.data_source.data["fill_color"]
		existingColors[ledIndex] = color
		self.leds.data_source.data["fill_color"] = existingColors

	#####TEXT FUNCTIONS
	def displayChar(self,charIn,color):
		self.log("Character",(charIn,color))

		indices = texter.charToBokehIndices(charIn)
		self.bulkSquareColorWrite(["green"]*64)
		for index in indices:
			self.writeSquareToColor(index,color)

def testChessboardWebDisplay():
	cWB = chessboardWebDisplay()

	# cWB.displayChar("R","#0000FF")
	# cWB.writeSquareToColor(0,"#0000FF")
	# cWB.toggleVisibility(0)
	# cWB.writeLedToColor(0,"#0000FF")

	# show (cWB.boardWindow)
	# curdoc().add_root(cWB.boardWindow)

# testChessboardWebDisplay()