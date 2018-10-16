#include "tester.h"

tester::tester(){}

//turns on alternating squares with various loading settings
void tester::loadingTest(){
 loadingTurnOn(CRGB::Purple,CRGB::Black,10,10);
 loadingTurnOn(CRGB::Black,CRGB::Yellow,10,10);
 loadingTurnOn(CRGB::Purple,CRGB::Black,10,10);
 loadingTurnOn(CRGB::Black,CRGB::Black,10,10);
}

//turns on and off the leds with various fade settings
void tester::fadeTest(){
   fadeIn(CRGB::Red,CRGB::Yellow,10,10);
   fadeOut(10,10);
}

//turns on and off the leds with various row and column settings
void tester::rowTest(){
  turnOnRowCol(CRGB::Green,maxBrightness,testDelayTime,0);
  turnOnRowCol(CRGB::Yellow,maxBrightness,testDelayTime,1);  
  turnOnRowCol(CRGB::Black,maxBrightness,testDelayTime,0);  
}

//turns on and off the leds with various square settings
void tester::squareTest(){
   turnOnBySquare(CRGB::Yellow,CRGB::Red,maxBrightness,5);
   turnOnBySquare(CRGB::Black,CRGB::Red,maxBrightness,5);
   turnOnBySquare(CRGB::Black,CRGB::Black,maxBrightness,5);
}

//turns on and off the leds with various snake settings
void tester::snakeTest(){
   fastSnake(CRGB::Red,CRGB::Blue,maxBrightness,2);
   fastSnake(CRGB::Black,CRGB::Black,maxBrightness,3);

   fastSnake(CRGB::Red,CRGB::Blue,maxBrightness,4);
   fastSnake(CRGB::Black,CRGB::Black,maxBrightness,5);
}

//several tests comiled into a function to tesst mass functionality
void tester::startupTest(){
   //writePicture(picture);
   //delay(1000);
   //writePicture(picture2);
   //delay(3000);
   //turnOffLEDs();
   loadingTest();
   //fadeTest();
   squareTest();
   //snakeTest();
}
