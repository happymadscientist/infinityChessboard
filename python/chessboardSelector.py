from bokeh.plotting import figure, show, output_file, curdoc
import numpy as np
from bokeh.models import TapTool
import bokeh.events as events
from bokeh.layouts import row

class chessboardSquarePicker:

	def __init__(self):
		self.setupBoardVariables()

		self.setupSquareWindow()
		self.setupLedWindow()
		self.setupPalleteWindow()
		self.setupGui()

	def setupGui(self):
		self.gui = row(self.squareWindow)#,self.colorPicker)

	def setupBoardVariables(self):
		self.boardMode = "square"

		self.figureSize = 1200

		self.numRows = 8
		self.numCols = 8
		self.ledSize = 1
		self.ledSpacing = 1.15
		self.squareSize = 1
		self.ledColors = ["green"] * 1024
		self.squareColors = ["green"] * self.numRows * self.numCols
	### LED Mode functions
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

	def setupLedWindow(self):

		ledXs = np.array([])
		ledYs = np.array([])

		for xInd in range(self.numCols):
			for yInd in range(self.numRows):
				x,y = self.generateLedCoords(self.ledSpacing,xInd,yInd)
				ledXs = np.append(ledXs,x)
				ledYs = np.append(ledYs,y)

		xRange = (-self.ledSize/2,6*self.ledSpacing*self.numCols - self.ledSize/2)
		yRange = (-self.ledSize/2,6*self.ledSpacing*self.numRows - self.ledSize/2)

		xTicks = np.linspace(xRange[0],xRange[1],self.numCols+1)
		yTicks = np.linspace(yRange[0],yRange[1],self.numRows+1)

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

		p = figure(plot_width=self.figureSize, plot_height=self.figureSize,
			x_range = xRange,y_range = yRange)

		p.grid.visible = False
		p.axis.visible = False

		self.leds = p.rect(x=ledXs, y=ledYs, 
			width=self.ledSize, height=self.ledSize,
			color=self.ledColors,angle=0, height_units="data")

		# self.ldes.data_source.on_change("selected",self.callback)

		p.multi_line(xs=lineXs, ys=lineYs, line_color="#8073ac", line_width=2)

		p.add_tools(TapTool(renderers = [self.squares]))

		self.ledWindow = p


	def bulkLedColorWrite(self,newColors):
		self.leds.data_source.data["fill_color"] = newColors

	## Square mode functions
	def generateSquareCoords(self,numSquares):
		squareCenter = np.array((self.squareSize,self.squareSize))/2
		squareCoords = []
		for x in range(numSquares):
			for y in range(numSquares):
				squareCoord = squareCenter + (x*self.squareSize,0) + (0,y*self.squareSize)
				squareCoords.append(squareCoord)

		return (np.array((squareCoords)))

	def setupSquareWindow(self):
		squareSizeMod = .9
		offset = 1-squareSizeMod

		squareCoords = self.generateSquareCoords(self.numRows)
		xs = (squareCoords[:,0])
		ys = (squareCoords[:,1])

		xRange = (offset,(self.squareSize * self.numRows) - offset)
		yRange = (offset,(self.squareSize * self.numCols) - offset)
		p = figure(plot_width=self.figureSize, plot_height=self.figureSize,
			x_range=xRange,y_range = yRange)

		p.axis.visible = False
		p.grid.visible = False

		self.squares = p.rect(x=xs, y=ys, 
			width=self.squareSize*squareSizeMod, height=self.squareSize*squareSizeMod, 
			color=self.squareColors,
		       angle=0, height_units="data")

		self.squares.data_source.on_change("selected",self.squareSelectCallback)

		p.add_tools(TapTool())

		self.squareWindow = p

	def squareSelectCallback(self,attr,old,new):
		selectedIndex = self.squares.data_source.selected.indices[-1]
		self.writeSquareToColor(selectedIndex,"red")

	def writeSquareToColor(self,squareIndex,color):
		existingColors = self.squares.data_source.data["fill_color"]
		existingColors[squareIndex] = color

		self.squares.data_source.data["fill_color"] = existingColors

	def bulkSquareColorWrite(self,newColors):
		self.squares.data_source.data["fill_color"] = newColors

	def colorUpdate(self,r,g):
		color = "#%02x%02x%02x" % (int(255*r), int(255*g), 150)
		
		outputRect = self.colorFig.select_one({'name': 'colorRect'})
		outputRect.data_source.data = {"x":[.5],"y":[.5],"width":[1],"height":[1],"fill_color":[color]}

	def mouseCallback(self,event):	
		colorUpdate(event.x,event.y)

	def setupPalleteWindow(self):

		x = np.linspace(0,1,4)
		y = np.linspace(0,1,4)

		mesh = np.meshgrid(x,y)

		xx = mesh[0].flatten()
		yy = mesh[1].flatten()

		colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(255*xx, 256*yy)]

		p = figure(x_range=(0,1),y_range=(0,1),width=200,height=self.figureSize,toolbar_location=None)
		p.axis.visible = False
		p.grid.visible = False

		self.colorPickerSquareSize = .1
		colorMap = p.rect(x=xx,y=yy,width=self.colorPickerSquareSize,height=self.colorPickerSquareSize, fill_color=colors,line_color=colors)#line_width=0,line_alpha=0.0)

		# p.on_event(events.MouseMove,self.mouseCallback)
		self.colorPicker = p

	def showGui(self):
		show(self.gui)
		curdoc().add_root(self.gui)


from imageHandler import chessboardImageHandler
cI = chessboardImageHandler()

cI.iconFileCallback(1,1,{"file_name":["josh.png"]})
newColors = (cI.updateResizedImage())

cSP = chessboardSquarePicker()
cSP.bulkLedColorWrite(newColors)

cSP.showGui()