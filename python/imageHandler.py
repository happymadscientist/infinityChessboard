import os
from PIL import Image
import numpy as np

class chessboardImageHandler:
	"""Tool to resize and mask an image to be displayed on infinity chessboard.
	Output modes:
	8x8 (square = 1 pixel)
	32x32 (square = 16 pixels)
	48x48 (square = 36 pixels)
	"""

	def __init__(self):
		self.maskModes = {(8,8):0,(32,32):4,(48,48):6}
		self.activeUrl = ""
		self.resizeSize = (48,48)
		self.maskMode = self.maskModes[self.resizeSize]
	
	def getMaskCoords(self,resizeSize):
		if resizeSize == (48,48):
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

		for y in range(8):
			for x in range(8):
				maskYs = np.append(maskYs,ys + (masterSquareSpace * y))
				maskXs = np.append(maskXs,xs + (masterSquareSpace * x))

		return(maskXs.astype(int),maskYs.astype(int))

	def maskResizedImage(self,imArray,resizeSize):
		maskXs,maskYs = self.getMaskCoords(resizeSize)
		blankImage = np.zeros([resizeSize[0],resizeSize[1],4],dtype=np.uint8)

		vectorizedCoords = []
		for xCoord,yCoord in zip(maskXs,maskYs):
			imVal = imArray[xCoord,yCoord]
			blankImage[xCoord,yCoord] = imVal

			colorCode = self.pixelValueToColorCode(imVal[:3])
			vectorizedCoords.append(colorCode)

		return blankImage,vectorizedCoords

	def getBoardImage(self,url,resizeSize = (8,8)):
		print (url)
		print (1)
		img = Image.open(url).convert("RGBA")
		
		resizedImg = img.resize(resizeSize)
		imArray = np.flipud(np.array(resizedImg))

		if resizeSize != (8,8):
			imArray,coords = self.maskResizedImage(imArray,resizeSize)
		else:
			coords = self.vectorizePixelValues(imArray)

		return imArray,coords

	#methods for converting masked images to board colors
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

def testImageHandler():
	# cI = chessboardImageHandler()
	url = os.path.join("static","heart.png")
	# print (cI.getBoardImage(url))
	# self.pictureSizes = list(self.maskModes.keys())


from bokeh.io import show, curdoc
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import CheckboxButtonGroup, TextInput, DateSlider, Div, RadioButtonGroup, Button, HTMLTemplateFormatter
from bokeh.models.glyphs import ImageURL
from bokeh.models import CustomJS
from bokeh.plotting import ColumnDataSource, figure

class chessboardImageShower:

	def __init__(self):
		self.imageHandler = chessboardImageHandler()
		self.setupVariables()
		self.setupPictureWindows()
		self.setupControls()
		self.setupGui()

	def setupVariables(self):
		self.pictureModes = ["8x8","32x32","48x48"]
		self.resizeSizes = {"8x8":(8,8),"32x32":(32,32),"48x48":(48,48)}
		self.resizeSize = (48,48)

	def setupPictureWindows(self):
		#Unmodified image window setup
		ogWindow = self.getPictureWindow()

		image = ImageURL(url="url", x="x1", y="y1", w="w1", h="h1", anchor="bottom_left",name = "IconSource")

		self.picSource = ColumnDataSource(dict(
		    url = [""],
		    x1 = [0], y1 = [0],w1 = [1], h1 = [1]
		))

		ogWindow.add_glyph(self.picSource,image)

		#masked image window setup
		resizedWindow = self.getPictureWindow()
		resizedWindow.image_rgba(image=[], x=0, y=0, dw=1, dh=1,name = "masked")

		self.pictureWindows = column(ogWindow,resizedWindow)

	def getPictureWindow(self):
		#returns bokeh figure window
		p = figure(x_range=(0,1), y_range=(0,1), plot_width=300, plot_height=300,
		       tools="", toolbar_location=None)

		p.axis.visible = False
		p.grid.visible = False
		p.outline_line_color = None
		return p

	def setupIconFileButton(self):
		#creates button and registers its callback to load a user chosen image
		self.iconFileSource = ColumnDataSource({'file_contents':[], 'file_name':[]})

		#this will be set by an external class
		# iconFileSource.on_change('data', self.iconFileCallback)

		iconFileButton = Button(label="Import image", button_type="success")
		iconFileButton.callback = self.fileButtonCallback(self.iconFileSource)
		return iconFileButton

	# def iconFileCallback(self,attr,old,new):
	# 	#called when 'file_name' is changed, loads the new image in and updates the board views
	# 	iconFilename =  new['file_name'][0]
	# 	self.activeUrl = os.path.join("static",iconFilename)

	# 	self.updateOriginalImage()
	# 	imArray,coords = cI.getBoardImage(self.activeUrl,self.resizeSize)
	# 	self.updateResizedImage(imArray)
 

	def fileButtonCallback(self,fileInfoSource):
		#loads in a user selected image
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

	def pictureModeCallback(self,attr,old,new):
		#called on change of picture mode (8x8,32x32...)
		newMode = self.pictureModes[new]

		self.resizeSize = self.resizeSizes[newMode]

		imArray,coords = self.imageHandler.getBoardImage(self.activeUrl,self.resizeSize)
		self.updateResizedImage(imArray)

	def updateOriginalImage(self):
		self.picSource.data["url"] = [self.activeUrl]

	def getBoardImage(self):
		print (self.activeUrl)
		imArray,coords = self.imageHandler.getBoardImage(self.activeUrl,self.resizeSize)

		return imArray,coords

	def updateResizedImage(self,imArray):
		self.gui.select_one({"name":"masked"}).data_source.data["image"] = [imArray]

	def setupControls(self):
		pictureModeButtons = RadioButtonGroup(labels=self.pictureModes, active=0,width=400)
		pictureModeButtons.on_change("active",self.pictureModeCallback)

		fileButton = self.setupIconFileButton()
		self.controls = column(fileButton,pictureModeButtons)

	def setupGui(self):
		self.gui = column(
			self.controls,
			self.pictureWindows,
		)

	def showGui(self):
		show(self.gui)
		try:
			curdoc().add_root(self.gui)
		except:
			pass

def testImageHandler():
	cIS = chessboardImageShower()

	filepath = "heart.png"
	cIS.iconFileCallback(1,1,{"file_name":[filepath]})
	# cIS.showGui()

# testImageHandler()