from bokeh.plotting import figure, show, output_file, curdoc
import numpy as np
from bokeh.models import TapTool, ColumnDataSource
import bokeh.events as events
from bokeh.layouts import row, column
from bokeh.models.widgets import RadioButtonGroup, Button, Slider, TextInput
from bokeh.models.glyphs import Rect

from textHandler import textHandler
texter = textHandler()

from string import ascii_uppercase, ascii_lowercase

class chessboardSquarePicker:

	def __init__(self):

		self.setupBoardVariables()
		self.setupMasterBoardWindow()
		self.setupPalleteWindow()
		self.setupControls()
		self.setupGui()

	def setupControls(self):
		textInput = TextInput(value="",title = "Text to display")
		textInput.on_change("value",self.textCallback)

		brightnessSlider = Slider(start=0, end=1, value=.5, step=.05, title="Brightness")
		brightnessSlider.on_change("value",self.brightnessCallback)

		iconFileSource = ColumnDataSource({'file_contents':[], 'file_name':[]})
		# iconFileSource.on_change('data', self.iconFileCallback)
		importFileButton = Button(label="Import file", button_type="success")
		# importFileButton.callback = self.fileButtonCallback(iconFileSource)

		boardModeButtons = RadioButtonGroup(labels=self.boardModes, active=0,width=400,button_type="warning")
		boardModeButtons.on_change("active",self.boardModeCallback)
		self.controls = row(brightnessSlider,boardModeButtons,textInput)

	def setupGui(self):
		self.gui = column(
			row(self.boardWindow,self.colorPicker),
			self.controls
			)
	def textCallback(self,attr,old,new):
		newChar = new[0]
		indices = texter.charToBokehIndices(newChar)
		cSP.bulkSquareColorWrite(["green"]*64)
		# color = "blue"
		for index in indices:
			cSP.writeSquareToColor(index,self.activeColor)


	def brightnessCallback(self,attr,old,new):
		newBrightness = new
		# print (dir(self.squares))
		self.squares.glyph.fill_alpha = new
		self.leds.glyph.fill_alpha = new

		# self.leds.nonselection_glyph.fill_alpha = new
		# self.squares.fill_alpha = new


	def boardModeCallback(self,attr,old,new):
		self.boardMode = self.boardModes[new]
		self.changeBoardMode(self.boardMode)

	def changeBoardMode(self,boardMode):
		if boardMode == "Square":
			self.leds.visible = False
			self.squares.visible = True

		elif boardMode == "LED":
			self.leds.visible = True
			self.squares.visible = False

	def setupBoardVariables(self):
		self.boardModes = ["Square","LED","Picture","Text"]
		self.boardMode = self.boardModes[0]

		self.figureSize = 880

		self.numRows = 8
		self.numCols = 8
		self.ledSize = 1
		self.ledSpacing = 1.15
		self.squareSize = self.ledSpacing*6
		self.ledColors = ["green"] * 16 * self.numRows * self.numCols
		self.squareColors = ["green"] * self.numRows * self.numCols

	def setupMasterBoardWindow(self):
		xRange = (-self.ledSize/2,6*self.ledSpacing*self.numCols - self.ledSize/2)
		yRange = (-self.ledSize/2,6*self.ledSpacing*self.numRows - self.ledSize/2)

		p = figure(plot_width=self.figureSize, plot_height=self.figureSize,
			x_range = xRange,y_range = yRange,toolbar_location=None,
			name = "board window",tools="")

		p.grid.visible = False
		p.axis.visible = False

		ledXs = np.array([])
		ledYs = np.array([])

		for xInd in range(self.numCols):
			for yInd in range(self.numRows):
				x,y = self.generateLedCoords(self.ledSpacing,xInd,yInd)
				ledXs = np.append(ledXs,x)
				ledYs = np.append(ledYs,y)

		xTicks = np.linspace(xRange[0],xRange[1],self.numCols+1)
		yTicks = np.linspace(yRange[0],yRange[1],self.numRows+1)

		lineXs,lineYs = self.generateGridLineCoords(xTicks,yTicks)

		p.multi_line(xs=lineXs, ys=lineYs, line_color="#8073ac", line_width=2)

		squareSizeMod = .9
		offset = 1 - squareSizeMod

		squareCoords = self.generateSquareCoords(self.numRows)
		squareXs = (squareCoords[:,0])
		squareYs = (squareCoords[:,1])

		# xRange = (offset,(self.squareSize * self.numRows) - offset)
		# yRange = (offset,(self.squareSize * self.numCols) - offset)

		self.leds = p.rect(x=ledXs, y=ledYs, 
			width=self.ledSize, height=self.ledSize,
			color=self.ledColors,angle=0, height_units="data",
			fill_alpha=.5)

		self.squares = p.rect(x=squareXs, y=squareYs, 
			width=self.squareSize*squareSizeMod, height=self.squareSize*squareSizeMod, 
			color=self.squareColors, angle=0, height_units="data",
			fill_alpha=.5)

		self.squares.nonselection_glyph = self.squares.selection_glyph
		self.leds.nonselection_glyph = self.leds.selection_glyph

		self.boardSelectTool= TapTool(renderers = [self.squares,self.leds])

		# self.squares.visible = False
		self.leds.visible = False

		p.add_tools(self.boardSelectTool)
		p.toolbar.active_tap = self.boardSelectTool

		self.boardWindow = p

		self.squares.data_source.on_change("selected",self.squareSelectCallback)
		self.leds.data_source.on_change("selected",self.ledSelectCallback)


	def fileButtonCallback(self,fileInfoSource):
		return CustomJS(args=dict(file_source=fileInfoSource), code = """
			function read_file(filename) {
			    var reader = new FileReader();
			    reader.onload = load_handler;
			    reader.onerror = error_handler;
			    // readAsDataURL represents the file's data as a base64 encoded string
			    reader.readAsDataURL(filename);
			}

			function load_handler(event) {
			    var b64string = event.target.result;
			    file_source.data = {'file_contents' : [b64string], 'file_name':[input.files[0].name]};
			    file_source.trigger("change");
			}

			function error_handler(evt) {
			    if(evt.target.error.name == "NotReadableError") {
			        alert("Can't read file!");
			    }
			}

			var input = document.createElement('input');
			input.setAttribute('type', 'file');
			input.onchange = function(){
			    if (window.FileReader) {
			        read_file(input.files[0]);
			    } else {
			        alert('FileReader is not supported in this browser');
			    }
			}
			input.click();
			""")

	def generateGridLineCoords(self,xTicks,yTicks):
		
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

	def bulkLedColorWrite(self,newColors):
		self.leds.data_source.data["fill_color"] = newColors

	def ledSelectCallback(self,attr,old,new):
		selectedIndices = self.leds.data_source.selected.indices
		if selectedIndices:
			self.writeLedToColor(selectedIndices[-1],self.activeColor)

	def writeLedToColor(self,ledIndex,color):
		existingColors = self.leds.data_source.data["fill_color"]
		existingColors[ledIndex] = color
		self.leds.data_source.data["fill_color"] = existingColors

	## Square mode functions
	def generateSquareCoords(self,numSquares):
		squareCenter = np.array((self.squareSize,self.squareSize))/2
		squareCoords = []
		for x in range(numSquares):
			for y in range(numSquares):
				squareCoord = squareCenter + (x*self.squareSize,0) + (0,y*self.squareSize)
				squareCoords.append(squareCoord)

		return (np.array((squareCoords)))

	def squareSelectCallback(self,attr,old,new):
		selectedIndex = self.squares.data_source.selected.indices[-1]
		self.writeSquareToColor(selectedIndex,self.activeColor)

	def writeSquareToColor(self,squareIndex,color):
		existingColors = self.squares.data_source.data["fill_color"]
		existingColors[squareIndex] = color

		self.squares.data_source.data["fill_color"] = existingColors

	def bulkSquareColorWrite(self,newColors):
		self.squares.data_source.data["fill_color"] = newColors

	def colorUpdate(self,r,g):
		color = "#%02x%02x%02x" % (int(255*r), int(255*g), 150)
		self.activeColor = color
		self.outputColorSource.data["color"] =[color]

	def mouseCallback(self,event):	
		if self.colorChangeMode:
			self.colorUpdate(event.x,event.y)

	def mouseClickCallback(self,event):
		self.colorChangeMode = 1 -  self.colorChangeMode

	def setupPalleteWindow(self):
		self.colorChangeMode = 0
		self.colorPickerSquareSize = .1
		self.activeColor = "red"
		x = np.linspace(0,1,11)
		y = np.linspace(0,1,11)

		mesh = np.meshgrid(x,y)

		xx = mesh[0].flatten()
		yy = mesh[1].flatten()

		colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(255*xx, 256*yy)]

		p = figure(x_range=(0,1),y_range=(0,1),width=200,height=self.figureSize-200,toolbar_location=None,tools="")
		p.axis.visible = False
		p.grid.visible = False

		colorMap = p.rect(x=xx,y=yy,width=self.colorPickerSquareSize,height=self.colorPickerSquareSize, fill_color=colors,line_color=colors)#line_width=0,line_alpha=0.0)

		outputColorWindow = figure(x_range=(0,1),y_range=(0,1),width=200,height=200,toolbar_location=None,tools="")
		outputColorWindow.axis.visible = False
		outputColorWindow.grid.visible = False
		self.outputColorSource = ColumnDataSource(data=dict(x=[.5],y=[.5],w=[1],h=[1],color=[self.activeColor]))

		outputColorRect = outputColorWindow.rect(x="x",y="y",width = "w",height="h", fill_color="color",source=self.outputColorSource,name="output rect")#line_width=0,line_alpha=0.0)

		p.on_event(events.MouseMove,self.mouseCallback)
		p.on_event(events.Tap,self.mouseClickCallback)
		self.colorPicker = column(outputColorWindow,p)

	def showGui(self):
		show(self.gui)
		curdoc().add_root(self.gui)
		self.letterIndex = 0
		self.upperLowerMode = 0
		curdoc().add_periodic_callback(self.alphabetize,500)

	def alphabetize(self):
		if self.letterIndex > 25:
			self.letterIndex = 0
			self.upperLowerMode = 1 - self.upperLowerMode

		if self.upperLowerMode:
			activeLetter = ascii_lowercase[self.letterIndex]
		else:
			activeLetter = ascii_uppercase[self.letterIndex]

		self.textCallback(0,0,activeLetter)
		self.letterIndex += 1
		
# from imageHandler import chessboardImageHandler
# cI = chessboardImageHandler()

# cI.iconFileCallback(1,1,{"file_name":["heart.png"]})
# newColors = (cI.updateResizedImage())

cSP = chessboardSquarePicker()
# cSP.changeBoardMode("LED")
# cSP.bulkLedColorWrite(newColors)
# cSP.brightnessCallback(0,0,0)
# cSP.textCallback(0,0,"R")
cSP.showGui()
