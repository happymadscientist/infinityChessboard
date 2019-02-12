from bokeh.models.widgets import RadioButtonGroup, Button, Slider, TextInput
from bokeh.models.glyphs import Rect
from bokeh.events import MouseMove, Tap
from bokeh.models import ColumnDataSource, TapTool
from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import row, column

import numpy as np
import os

from imageHandler import chessboardImageShower
cIS = chessboardImageShower()

from chessboardWebDisplay import chessboardWebDisplay as chessboardDisplay

# from chessboardCommunicator import chessboardClient
# cc = chessboardClient()

class chessboardWebController:

	def __init__(self):

		self.colors = ["#FF00FF","#00FFFF","#FFFF00","#00FF00"]
		self.colorIndex = 0
		self.numColors = 1

		self.setupControllerVariables()
		self.setupControls()
		self.setupColorPalleteWindow()

		self.setupChessboardDisplay()
		self.setupGui()

		self.createColorOutputWindow(self.numColors)

	def setupChessboardDisplay(self):
		self.chessboardDisplay = chessboardDisplay()
		self.chessboardDisplay.assignSquareClickToFunction(self.handleSquareSelect)
		self.chessboardDisplay.assignLedClickToFunction(self.handleLedSelect)

	def setupControllerVariables(self):
		self.boardModes = ["Line","Snake","Fade Out","Square","LED","Image","Text"]
		self.activeMode = self.boardModes[0]

		self.figureSize = 800

	def setupControls(self):
		boardModeButtons = RadioButtonGroup(labels=self.boardModes, active=0,width=400,button_type="primary")
		boardModeButtons.on_change("active",self.boardModeCallback)

		self.brightnessSlider = Slider(title="Brightness", show_value=False, height=self.figureSize, value=.5, start=0, end=1, step=.1, orientation="vertical")
		self.brightnessSlider.on_change("value",self.brightnessCallback)

		#create an empty row to store the active controls in
		activeControlsBox = column(name="activeControls")

		#setup the image handler controls to control the board
		cIS.iconFileSource.on_change('data', self.iconFileCallback)

		self.controls = column(boardModeButtons,activeControlsBox)

	# def setupIconFileCallback(self):
	
	def iconFileCallback(self,attr,old,new):
		#called when 'file_name' is changed, loads the new image in and updates the board views
		iconFilename =  new['file_name'][0]
		cIS.activeUrl = os.path.join("static",iconFilename)
		cIS.updateOriginalImage()
		imArray,coords = cIS.getBoardImage()

		cIS.updateResizedImage(imArray)
		self.chessboardDisplay.bulkLedColorWrite(coords)
		# print (coords[0])



	def createSquareControls(self):
		squareColorWindow = self.createColorOutputWindow(1)
		return [squareColorWindow]

	def createLedControls(self):
		ledColorWindow = self.createColorOutputWindow(1)
		return [ledColorWindow]

	def createLineControls(self):
		self.startingSquare = None
		self.endingSquare = None

		lineColorWindow = self.createColorOutputWindow(1)
		sendLineButton = Button(label = "Send")
		sendLineButton.on_click(self.postLine)
		return [lineColorWindow,sendLineButton]

	def createFadeOutControls(self):
		self.fadeSpeed = 500
		fadeSpeedSlider = Slider(title="Speed", show_value=False, value=self.fadeSpeed, start=30, end=1000, step=5)
		fadeSpeedSlider.on_change("value",self.fadeSpeedCallback)

		self.fadeStride = .1
		fadeStrideSlider = Slider(title="Stride", show_value=False, value=self.fadeStride, start=.01, end=.2, step=.01)
		fadeStrideSlider.on_change("value",self.fadeStrideCallback)

		return [fadeSpeedSlider,fadeStrideSlider]

	def fadeStrideCallback(self,attr,old,new):
		self.fadeStride = new

	def fadeSpeedCallback(self,attr,old,new):
		#called when the fade speed slider is changed, updates the callback frequency of the fade update function
		self.fadeSpeed = new

		try:
			curdoc().remove_periodic_callback(self.fadeCallback)
			self.fadeCallback = curdoc().add_periodic_callback(self.updateFade,self.fadeSpeed)
		except:
			print ("Snake speed - Couldn't remove callback")

	def createSnakeControls(self):
		#snake mode controls
		snakeModeControls = RadioButtonGroup(labels=["Square","LED"], active=0,width=400,button_type="primary")
		# snakeModeControls.on_change("active",self.visibilityCallback)

		self.snakeSpeed = 500
		snakeSpeedSlider = Slider(title="Speed", show_value=False, value=self.snakeSpeed, start=30, end=1000, step=5)
		snakeSpeedSlider.on_change("value",self.snakeSpeedCallback)
		snakeNumberControls = RadioButtonGroup(labels=["1","2"], active=0,width=400,button_type="primary", name = "Num Snakes")
		snakeColorWindow = self.createColorOutputWindow(2)

		sendSnakeButton = Button(label = "Send")
		sendSnakeButton.on_click(self.postSnake)

		return [snakeModeControls,snakeNumberControls,snakeSpeedSlider,snakeColorWindow,sendSnakeButton]

	def snakeSpeedCallback(self,attr,old,new):
		#called when the snake speed slider is changed, updates the callback frequency of the snake update function
		self.snakeSpeed = new

		try:
			curdoc().remove_periodic_callback(self.snakeCallback)
			self.snakeCallback = curdoc().add_periodic_callback(self.updateSnake,self.snakeSpeed)
		except:
			print ("Snake speed - Couldn't remove callback")

	def createTextControls(self):
		#text mode controls
		textInput = TextInput(value="",title = "Text to display",name = "Text")
		textInput.on_change("value", self.textBoxCallback)
		textColorWindow = self.createColorOutputWindow(1)
		sendTextButton = Button(label = "Send")
		sendTextButton.on_click(self.postText)
		return [textInput,textColorWindow,sendTextButton]

	def textBoxCallback(self,attr,old,new):
		#a boolean used to set if the first letter of the string should be drawn immediately when "drawText" is called or if it should wait to be updated by the periodic callback
		#if this is the first time the string has been diusplayed, immediately display string[0] for responsiveness.
		#otherwise, if you've reached the end of the string and are repeating it from the beginning, don't immediately draw the first character, hold the last one until the periodic callback updates it
		self.firstTextDisplay = 1

		if new:
			self.activeString = new
			self.drawText()

	def drawText(self):
		self.charColor = self.activeColor
		self.activeCharIndex = 0
		self.textCallback = curdoc().add_periodic_callback(self.updateText,1000)
		if self.firstTextDisplay:
			self.updateText()
			self.firstTextDisplay = 0

	def updateText(self):
		activeChar = self.activeString[self.activeCharIndex]
		self.chessboardDisplay.displayChar(activeChar,self.charColor)

		self.activeCharIndex += 1
		if self.activeCharIndex >= len(self.activeString):
			curdoc().remove_periodic_callback(self.textCallback)
			self.drawText()

	def alphabetize(self,color = "#00FFF0"):
		alphabetString = ascii_lowercase + ascii_uppercase
		self.displayString(alphabetString,color)

	def createImageControls(self):
		return [cIS.gui]

	def setupGui(self):
		self.gui = column(
			row(self.controls,self.colorPicker,self.chessboardDisplay.boardWindow,self.brightnessSlider),
			# row(self.controls,self.colorPicker,self.boardWindow,self.brightnessSlider),
			)

	def brightnessCallback(self,attr,old,new):
		newBrightness = new
		self.chessboardDisplay.changeBrightness(newBrightness)

	def boardModeCallback(self,attr,old,new):
		self.activeMode = self.boardModes[new]
		self.changeBoardMode(self.activeMode)

	def removePeriodicCallbacks(self):
		try: curdoc().remove_periodic_callback(self.snakeCallback)
		except:	pass
		try: curdoc().remove_periodic_callback(self.fadeCallback)
		except: pass
		try: curdoc().remove_periodic_callback(self.textCallback)
		except: pass

	def changeBoardMode(self,boardMode):
		self.removePeriodicCallbacks()

		if boardMode == "Square":
			self.chessboardDisplay.toggleVisibility(squaresVisible = True)
			newControls = self.createSquareControls()

		elif boardMode == "LED":
			self.chessboardDisplay.toggleVisibility(squaresVisible = False)
			newControls = self.createLedControls()

		elif boardMode == "Fade Out":
			newControls = self.createFadeOutControls()
			self.drawFade()

		elif boardMode == "Image":	
			self.chessboardDisplay.toggleVisibility(squaresVisible = False)
			newControls = self.createImageControls()

		elif boardMode == "Text":	
			self.chessboardDisplay.toggleVisibility(squaresVisible = True)
			newControls = self.createTextControls()

		elif boardMode == "Snake":	
			newControls = self.createSnakeControls()
			self.drawSnake()

		elif boardMode == "Line":	newControls = self.createLineControls()

		self.updateActiveControls(newControls)

	def updateActiveControls(self,newActiveControls):
		self.gui.select_one({"name":"activeControls"}).children = newActiveControls

	def colorUpdate(self,r,g):
		if r>1: r=1
		if g>1: g =1
		color = "#%02x%02x%02x" % (int(254*r), int(254*g), 150)

		self.activeColor = color
		self.outputColorSource.data["color"] = [color]*(self.numColors)
		self.brightnessSlider.bar_color = color

	def mouseCallback(self,event):
	#called on movement of the mouse through the color pallete window.
	#if color change is active, will update the output color window with the color the mouse is at
		if self.colorChangeMode:
			self.colorUpdate(event.x,event.y)

	def colorPalleteClickCallback(self,event):
		#called on click of an output color square, toggles whether or not its color is to be changed
		self.colorChangeMode = 1 -  self.colorChangeMode

	def setupColorPalleteWindow(self):
		self.colorChangeMode = 0
		self.colorPickerSquareSize = .1
		self.activeColor = "#FFFFFF"
	
		x = np.linspace(0,1,11)
		y = np.linspace(0,1,11)
		mesh = np.meshgrid(x,y)
		xx = mesh[0].flatten()
		yy = mesh[1].flatten()

		colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(255*xx, 256*yy)]

		colorPallete = figure(x_range=(0,1),y_range=(0,1),width=300,height=self.figureSize,toolbar_location=None,tools="")
		colorPallete.axis.visible = False
		colorPallete.grid.visible = False

		colorPallete.rect(x=xx,y=yy,width=self.colorPickerSquareSize,height=self.colorPickerSquareSize, fill_color=colors,line_color=colors)#line_width=0,line_alpha=0.0)
		colorPallete.on_event(MouseMove,self.mouseCallback)
		colorPallete.on_event(Tap,self.colorPalleteClickCallback)

		self.colorPicker = colorPallete

	def createColorOutputWindow(self,numColors):
		self.numColors = numColors
		# create the output color window
		outputColorWindow = figure(x_range=(0,numColors),y_range=(0,1),width=300,height=100,toolbar_location=None,tools="")
		outputColorWindow.axis.visible = False
		outputColorWindow.grid.visible = False

		self.outputColorSource = ColumnDataSource(data=dict(x=range(numColors),y=[.5]*numColors,w=[1]*numColors,h=[1]*numColors,color=[self.activeColor]*numColors))
		outputColorRect = outputColorWindow.rect(x="x",y="y",width = "w",height="h", fill_color="color",source=self.outputColorSource,name="output rect")#line_width=0,line_alpha=0.0)

		activeColorSelectTool= TapTool(renderers = [outputColorRect])

		outputColorRect.data_source.selected.on_change("indices",self.activeColorChange)
		return outputColorWindow

	def postLine(self):
		print (1)
		#line mode controls

	def postSnake(self):
		numSnakes = (self.gui.select_one({"name":"Num Snakes"})).active
		print (numSnakes)

	def postText(self):
		text = (self.gui.select_one({"name":"Text"})).value

	def postImage(self):
		print (1)

	def handleSquareSelect(self,attr,old,new):
		#get the most recently selected value
		if not new: return
		selectedIndex = new[-1]
		self.handleEvent("Square",selectedIndex)
		new = []

		# self.chessboardDisplay.writeSquareToColor(selectedIndex,self.activeColor)
		# cc.sendSquarePacket(selectedIndex,self.activeColor)

	def handleLedSelect(self,attr,old,new):
		if not new: return
		selectedIndex = new[-1]
		self.handleEvent("LED",selectedIndex)

	def handleEvent(self,eventType,eventData):
		#called on click of a square/led on the board

		#SQUARE LINE
		if eventType == "Square":
			clickedIndex = eventData
			if self.activeMode == "Line":
				#check if the starting square has been set
				if self.startingSquare == None:
					self.startingSquare = (clickedIndex//8, 7 - (clickedIndex%8))
					self.chessboardDisplay.writeSquareToColor(clickedIndex,self.activeColor)
					return

				endingX,endingY =  clickedIndex//8,7 - (clickedIndex%8)

				commonX = (endingX == self.startingSquare[0]) 
				commonY = (endingY == self.startingSquare[1])

				#check that the selected choice is colinear with the starting choice
				if not (commonX or commonY):
					return

				if commonY:
					#draw a horizontal line between the two squares
					xs = (self.startingSquare[0],endingX)
					xCoords = range(min(xs),max(xs))
					yCoords = [self.startingSquare[1]]*len(xCoords)

				else:
					#draw a vertical line between the choices
					ys = (self.startingSquare[1],endingY)
					yCoords = range(min(ys),max(ys))
					xCoords = [self.startingSquare[0]] * len(yCoords)

				indices = []
				for x,y in zip(xCoords,yCoords):
					index = (x*8) + (7-y)
					indices.append(index)
					self.chessboardDisplay.writeSquareToColor(index,self.activeColor)

				self.chessboardDisplay.writeSquareToColor(clickedIndex,self.activeColor)

		# 		cc.sendMultiSquarePacket(squareIndexes = indices,squareColors = [self.activeColor]*len(indices))

		# 		#reset the starting square for next time
				self.startingSquare = None
				return

			elif self.activeMode == "Square":
				self.chessboardDisplay.writeSquareToColor(clickedIndex,self.activeColor)

		elif eventType == "LED":
			clickedIndex = eventData
			if self.activeMode == "LED":
				self.chessboardDisplay.writeLedToColor(clickedIndex,self.activeColor)


		print (eventType,eventData)
		print (self.activeMode)

	def createSnakeCoords(self):
		self.numSnakes = 2
		baseOffset = (1,0)
		multiplier = 0

		#four snakes
		# theta = np.radians(90)
		# c, s = np.cos(theta), np.sin(theta)
		# R = np.array(((c,-s), (s, c)))

		# firstSnakeStartingCoord = (0,0)
		# secondSnakeStartingCoord = (7,0)
		# thirdSnakeStartingCoord = (7,7)
		# fourthSnakeStartingCoord = (0,7)

		# firstSnakeCoords = self.getCoordsOffsetDir(firstSnakeStartingCoord,(7,0))
		# secondSnakeCoords = self.getCoordsOffsetDir(secondSnakeStartingCoord,(0,7))
		# thirdSnakeCoords = self.getCoordsOffsetDir(thirdSnakeStartingCoord,(-7,0))
		# fourthSnakeCoords = self.getCoordsOffsetDir(fourthSnakeStartingCoord,(0,-7))
		# snakeCoords = [firstSnakeCoords,secondSnakeCoords,thirdSnakeCoords,fourthSnakeCoords]

		# offsetAmounts = [6,3,2]
		# offsetAmounts = range(6,-1,-3)

		# two snakes
		firstSnakeStartingCoord = (0,0)
		secondSnakeStartingCoord = (7,7)

		firstSnakeCoords = self.getCoordsOffsetDir(firstSnakeStartingCoord,(8,0))
		secondSnakeCoords = self.getCoordsOffsetDir(secondSnakeStartingCoord,(-8,0))
		snakeCoords = [firstSnakeCoords,secondSnakeCoords]
		offsetAmounts = range(7,-1,-2)

		#one snake
		# startingCoord = (0,0)
		# snakeCoords = [self.getCoordsOffsetDir(startingCoord,(8,0))]
		# offsetAmounts = range(8,-1,-1)

		for offsetAmount in offsetAmounts:
			#do a positive and a negative offset
			# if self.numSnakes = 4:

			for i in range(2):
				if i == 1 and self.numSnakes == 4:
					break
				baseOffset = baseOffset[::-1]
				multiplier += 1
				multiplier = multiplier % 4
				scaler = 1
				if (multiplier > 1):
					scaler = - 1

				offset = np.multiply(baseOffset,scaler * offsetAmount)

				#go through the last coord for each snake 
				# startingCoords = snakeCoords[-1]
				for snakeIndex,singleSnakeCoords in enumerate(snakeCoords):
					startingCoord = singleSnakeCoords[-1]
					newCoords = self.getCoordsOffsetDir(startingCoord,offset)
					snakeCoords[snakeIndex] += newCoords[1:]

					#to reverse direction for two snakes
					offset = -offset

					#to reverse direction for 4 snakes
					# offset = R.dot(offset).astype(int)

		return snakeCoords

	# def getSquareInCoords(self):
		
	def getCoordsOffsetDir(self,startingCoord,offset):
		#check if the offset is in the x dir
		dx = offset[0]
		if dx:
			direction = (dx>0)
			if direction: direction = 1
			else: direction = -1

			newXs = range(startingCoord[0],startingCoord[0]+dx,direction)
			newYs = [startingCoord[1]]*abs(dx)
		else:
			dy = offset[1]
			direction = dy>0
			if direction: direction = 1
			else: direction = -1
			
			newYs = range(startingCoord[1],startingCoord[1]+dy,direction)
			newXs = [startingCoord[0]]*abs(dy)
		
		coordsOut = [(x,y) for x,y in zip(newXs,newYs)]
		return coordsOut

	def drawFade(self):
		self.originalBrightness = self.chessboardDisplay.squares.glyph.fill_alpha

		self.newBrightness = self.originalBrightness

		self.fadeCallback = curdoc().add_periodic_callback(self.updateFade,self.fadeSpeed)

	def updateFade(self):
		self.chessboardDisplay.changeBrightness(self.newBrightness)

		self.newBrightness -= self.fadeStride
		if self.newBrightness<0:
			curdoc().remove_periodic_callback(self.fadeCallback)
			self.chessboardDisplay.changeBrightness(self.originalBrightness)
			self.drawFade()

	def drawSnake(self):
		# self.activeColor = self.colors[self.colorIndex]
		# self.colorIndex = (self.colorIndex + 1) % 3
		self.snakeCoords = self.createSnakeCoords()

		self.maxSnakeIndex = len(self.snakeCoords[0]) 

		self.activeSnakeIndex = 0
		self.snakeCallback = curdoc().add_periodic_callback(self.updateSnake,self.snakeSpeed)

	def updateSnake(self):
		#go through for each snake
		for snakeIndex in range(self.numSnakes):

			snakeCoords = self.snakeCoords[snakeIndex][self.activeSnakeIndex]
			snakeSquareIndex = (snakeCoords[0]*8) + (7-snakeCoords[1])
			snakeColor = self.colors[snakeIndex]

			self.chessboardDisplay.writeSquareToColor(snakeSquareIndex,snakeColor)

		self.activeSnakeIndex +=1
		if self.activeSnakeIndex > (self.maxSnakeIndex - 1):
			backgroundColors = [self.activeColor]*64
			self.chessboardDisplay.bulkSquareColorWrite(backgroundColors)

			curdoc().remove_periodic_callback(self.snakeCallback)
			self.drawSnake()


	def activeColorChange(self,attr,old,new):
		print (new)

	def showGui(self):
		show(self.gui)
		try:
			curdoc().add_root(self.gui)
		except:
			pass

def testWebController():
	cWB = chessboardWebController()
	cWB.showGui()

testWebController()