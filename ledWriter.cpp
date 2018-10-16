#include "ledWriter.h"

ledWriter::ledWriter(){}



//writes a single strand a solid color
void ledWriter::writeStrand(uint8_t strand, CRGB color, uint8_t bright){
  fill_solid(leds[strand],NUM_LEDS,color);
  FastLED.show();
}

//turns both strands off
void ledWriter::turnOffLEDs(){
  writeStrand(1,CRGB::Black,maxBrightness);
  writeStrand(0,CRGB::Black,maxBrightness);
}

//enable the LEDs and turn them off
void ledWriter::LEDSetup(){
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds[0], NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.addLeds<LED_TYPE, LED_PIN2, COLOR_ORDER>(leds[1], NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(maxBrightness);
  turnOffLEDs();
}

//change the brightness of both strips
void ledWriter::changeBrightness(uint8_t newBrightness){
  FastLED.setBrightness(newBrightness);
  FastLED.show();
}

/* END LED FUNCTIONS */

/* CHESSBOPARD FUNCTIONS */

//given coords in form decimal xy (eg 34 or 02) and color, write that square that color.  Update the board if showLED==true
void ledWriter::writeSquare(byte coords, CRGB color, bool showLED){
 uint8_t x = coords>>4;
 uint8_t y = coords%8;
 bool strand = (x+y)%2;
  for (int side=0;side<4;side++){    
    int ledNum = ((squares[x][y][side]-1)*4);
    leds[strand][ledNum] = color;
    leds[strand][ledNum+1] = color;
    leds[strand][ledNum+2] = color;
    leds[strand][ledNum+3] = color;
  }
  if (showLED) FastLED.show();
}

//writes a single square indexed 0-7,0-7 the colors set by r,g,b
void ledWriter::writeSquareRGB(uint8_t x, uint8_t y, uint8_t color[],bool showLED){
  CRGB colorRGB = CRGB(color[0],color[1],color[2]);
  uint8_t coord = x*16+y;
  writeSquare(coord,colorRGB,showLED);
}


//writes an entire row/col a solid color and updates once all 8 are set. Boolean rowCol determines row/col
void ledWriter::writeRowCol(CRGB color, uint8_t rowNum, bool rowCol){
  for (int i=0;i<8;i++){
    if (rowCol) writeSquare(rowNum*16+i,color,0);
    else writeSquare(i*16+rowNum,color,0);
    }
    FastLED.show();
}


//fades out from any configuration
void ledWriter::fadeOut(int fadeDelay, uint8_t brightness){
  for (int bright=brightness;bright>=0;bright--){
    changeBrightness(bright);
    delay(fadeDelay);
  }
  turnOffLEDs();
}

//given an 8x8 grid with rgv vals in each, write the board that picture.
void ledWriter::writePicture(uint8_t pictureIn[][8][3]){
  for (int x=0;x<7;x++){
    for (int y=0;y<7;y++){
      //writeSquareRGB(x,y,pictureIn[x][y],1);
    }
  }
}

//entire board a solid color by rows or columns
void ledWriter::turnOnRowCol(CRGB color, uint8_t brightness, int delayTime, bool rowCol){
  //changeBrightness(brightness);
  for (int x=0;x<8;x++){
    //writeRowCol(color,x,rowCol);
    delay(delayTime);
  }
}

//activates the leds in both strands, independent colors, one at a time
void ledWriter::snake(CRGB color, CRGB color2, uint8_t brightness, int delayTime){
   //changeBrightness(maxBrightness);
    for (int i=0;i<NUM_LEDS;i++){
      leds[0][i]= color;
      leds[1][i] = color2;
      FastLED.show();
      delayMicroseconds(delayTime);
    }
}

//activates the leds in both strands, independent colors, one at a time
void ledWriter::fastSnake(CRGB color, CRGB color2, uint8_t brightness, int multiplier){
   changeBrightness(maxBrightness);
    for (int i=0;i<(NUM_LEDS/multiplier)-multiplier;i++){
      for (int j=0;j<multiplier;j++){
          leds[0][multiplier*i+j]= color;
          leds[1][multiplier*i+j] = color2;
      }
      FastLED.show();
      //delayMicroseconds(delayTime);
    }
}

//turnas alternating squares their specific color.
void ledWriter::turnOnBySquare(CRGB color1,CRGB color2 ,uint8_t bright, uint8_t delayTime){
  changeBrightness(bright);
  for (int x=0;x<8;x++){
    for (int y=0;y<8;y++){
      uint8_t coord = x*16+y;
      //if ((x+y)%2) writeSquare(coord,color1,1);
      //else writeSquare(coord,color2,1);
      delay(delayTime);
    }
  }
}

//starting from the top left led, this goes through the led in each square and trurns it a color, kind of like a loading bar
void ledWriter::loadingTurnOn(CRGB color1,CRGB color2, uint8_t brightness, int delayTime){
  changeBrightness(brightness);
  for (int led=0;led<16;led++){
    int side = floor(led/4);
    for (int x=0;x<8;x++){
      for (int y=0;y<8;y++){
          int ledNum = (squares[x][y][side]-1)*4 + (led%4);
          bool strand = (x+y)%2;
          if (strand) leds[strand][ledNum] = color1;
          else leds[strand][ledNum] = color2;
       }
    } 
    FastLED.show();
    delay(delayTime);
  }
}

//fades in the chessboard with two colors
void ledWriter::fadeIn(CRGB color, CRGB color2,int fadeDelay, uint8_t brightness){
  fill_solid(leds[0],NUM_LEDS,color);
  fill_solid(leds[1],NUM_LEDS,color2);
  for (int bright=0;bright<brightness;bright++){
    changeBrightness(bright);
    delay(fadeDelay);
  }
}

//randomizes all the squares
void ledWriter::randomizeSquares(){
  for (int x=0;x<8;x++){
    for (int y=0;y<8;y++){
      uint8_t coord = x*16+y;
      writeSquare(coord,CRGB(random(255),random(255),random(255)),0);
    }
  }
  delay(10);
  FastLED.show();
}
