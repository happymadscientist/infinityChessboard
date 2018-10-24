from textBoardMapping import numbersDict, upperLettersDict,lowerLettersDict

class textHandler:
     def charToCoords(self,charIn):
          if charIn == charIn.upper():
               charIndices = upperLettersDict[charIn][:-1]
          else:
               charIndices = lowerLettersDict[charIn][:-1]
          charCoords = [self.boardIndexToPosCoord(charIndex) for charIndex in charIndices]
          return charCoords

     def charToBokehIndices(self,charIn):
          charCoords = self.charToCoords(charIn)
          charBokehIndices = [self.coordToBokehIndex(charCoord) for charCoord in charCoords]
          return (charBokehIndices)

     def boardIndexToPosCoord(self,index):
          x = 7 - index%16
          y = 7 - int(index/16)
          return (x,y)

     def coordToBokehIndex(self,coordIn):
          index = coordIn[0]*8 + coordIn[1]
          return index