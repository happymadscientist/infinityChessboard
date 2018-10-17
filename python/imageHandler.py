from bokeh.io import show, curdoc
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import CheckboxButtonGroup, TextInput, DateSlider, Div, RadioButtonGroup, Button, HTMLTemplateFormatter
from bokeh.models.glyphs import ImageURL
from bokeh.models import CustomJS
from bokeh.plotting import ColumnDataSource, figure

import os
from PIL import Image
import numpy as np

class chessboardImageHandler:
	"""Tool to resize and mask an image to be displayed on infinity chessboard.
	Display modes:
	8x8 (square = 1 pixel)
	32x32 (square = 16 pixels)
	48x48 (square = 36 pixels)
	"""

	def __init__(self):
		self.maskModes = {(8,8):0,(32,32):4,(48,48):6}

		self.pictureModes = ["8x8","32x32","48x48"]
		self.pictureSizes = self.maskModes.keys()
		
		self.activeUrl = ""
		self.resizeSize = (8,8)
		self.maskMode = self.maskModes[self.resizeSize]
		self.setupPictureWindows()
		self.setupControls()
		self.setupGui()

	def showGui(self):
		show(self.gui)
		curdoc().add_root(self.gui)

	def setupControls(self):

		self.pictureModeTitle = Div(text="Picture mode:",width=80,height=1)
		pictureModeButtons = RadioButtonGroup(
		        labels=self.pictureModes, active=0,width=400,button_type="warning")

		pictureModeButtons.on_change("active",self.pictureModeCallback)

		writeToBoardButton = Button(label="Write  to board", button_type="success")

		fileButton = self.setupIconFileButton()

		self.controls = row(fileButton,pictureModeButtons)

	def setupGui(self):
		self.gui = column(
			self.pictureWindows,
			self.controls)

	def pictureModeCallback(self,attr,old,new):
		newMode = new
		self.resizeSize = self.pictureSizes[newMode]
		self.maskMode =self.maskModes[self.resizeSize]
		self.updateResizedImage()

	def setupIconFileButton(self):
		iconFileSource = ColumnDataSource({'file_contents':[], 'file_name':[]})
		iconFileSource.on_change('data', self.iconFileCallback)
		iconFileButton = Button(label="Import image", button_type="success")
		iconFileButton.callback = self.fileButtonCallback(iconFileSource)
		return iconFileButton

	def iconFileCallback(self,attr,old,new):
		iconFilename =  new['file_name'][0]
		self.activeUrl = os.path.join("static",iconFilename)

		self.updateOriginalImage()
		self.updateResizedImage()

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

	def setupPictureWindows(self):
		ogWindow = self.getPictureWindow()
		image = ImageURL(url="url", x="x1", y="y1", anchor="bottom_left", w="w1", h="h1",name = "IconSource")#, anchor="bottom_left")
		self.picSource = ColumnDataSource(dict(
		    url = [""],
		    x1 = [0], y1 = [0],w1 = [1], h1 = [1]
		))
		ogWindow.add_glyph(self.picSource,image)

		resizedWindow = self.getPictureWindow()
		resizedWindow.image_rgba(image=[], x=0, y=0, dw=1, dh=1,name = "resized")

		self.pictureWindows = row(ogWindow,resizedWindow)

	def getPictureWindow(self):
		p = figure(x_range=(0,1), y_range=(0,1), plot_width=300, plot_height=300,
		       tools="", toolbar_location=None)

		p.axis.visible = False
		p.grid.visible = False
		p.outline_line_color = None
		return p

	def getMaskCoords(self,maskMode):
		if maskMode == 6:
			masterSquareSpace = 6
			squareMatrix = np.array([
				[0,1,1,1,1,0],
				[1,0,0,0,0,1],
				[1,0,0,0,0,1],
				[1,0,0,0,0,1],
				[1,0,0,0,0,1],
				[0,1,1,1,1,0]
				])
		else:
			masterSquareSpace = 4
			squareMatrix = np.array([
				[1,1,1,1],
				[1,0,0,1],
				[1,0,0,1],
				[1,1,1,1]
				])

		xs,ys = np.where(squareMatrix)

		maskXs = []
		maskYs = []

		for x in range(8):
			for y in range(8):
				maskYs = np.append(maskYs,ys + (masterSquareSpace * y))
				maskXs = np.append(maskXs,xs + (masterSquareSpace * x))

		return(maskXs.astype(int),maskYs.astype(int))

	def maskResizedImage(self,imArray):
		maskXs,maskYs = self.getMaskCoords(self.maskMode)
		blankImage = np.zeros([self.resizeSize[0],self.resizeSize[1],4],dtype=np.uint8)

		vectorizedCoords = []
		for xCoord,yCoord in zip(maskXs,maskYs):
			imVal = imArray[xCoord,yCoord]
			blankImage[xCoord,yCoord] = imVal

			colorCode = self.pixelValueToColorCode(imVal[:2])
			vectorizedCoords.append(colorCode)

		return blankImage,vectorizedCoords


	def updateResizedImage(self):
		newImg = Image.open(self.activeUrl).convert("RGBA")
		resizedImg = newImg.resize(self.resizeSize)
		imArray = np.flipud(np.array(resizedImg))

		if self.maskMode:
			imArray,coords = self.maskResizedImage(imArray)
		else:
			coords = self.vectorizePixelValues(imArray)

		self.gui.select_one({"name":"resized"}).data_source.data["image"] = [imArray]
		return coords

	def pixelValueToColorCode(self,pixelValue):
		hexVals = [format(rgbVal, '02x') for rgbVal in pixelValue]

		if not pixelValue.any(): colorCode = "#FFFFFF"
		else: colorCode = "#" + "".join(hexVals)

		return colorCode

	def vectorizePixelValues(self,imArray):
		pixelValues = []
		rows,cols,rgba = imArray.shape
		for y in range(0, cols):
			for x in range(0, rows):
				rgbVals = imArray[x,y][:3]
				colorCode = self.pixelValueToColorCode(rgbVals)
				pixelValues.append(colorCode)
		return pixelValues

	def updateOriginalImage(self):
		self.picSource.data["url"] = [self.activeUrl]

def testImageHandler():
	cI = chessboardImageHandler()
	cI.iconFileCallback(1,1,{"file_name":["heart.png"]})
	cI.showGui()

# testImageHandler()