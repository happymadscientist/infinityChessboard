#include<Arduino.h>
#include "bigVars.h"
#include <SPI.h>
#include <FastLED.h>
#include "colorutils.h"

#include "userParams.h"
class ledWriter {
  public:
      //led control
ledWriter();
          //low level LED control
    void changeBrightness(uint8_t bright);
        void LEDSetup();
    void turnOffLEDs();


    void writeStrand(uint8_t strand, CRGB color, uint8_t bright);
    void writeSquare(byte coords, CRGB color, bool showLED);
    void writeRowCol(CRGB color, uint8_t rowNum, bool rowCol);
    void writeArray(uint8_t instruction[][5]);
    void writePicture(uint8_t pictureIn[][8][3]);
    void writeSquareRGB(uint8_t x, uint8_t y, uint8_t color[],bool showLED);
    CRGB leds[NUM_STRANDS][NUM_LEDS];
    //full board writing cokmmands
    void turnOnRowCol(CRGB color, uint8_t brightness, int delayTime, bool rowCol);
    void snake(CRGB color, CRGB color2, uint8_t brightness, int delayTime);
    void fastSnake(CRGB color, CRGB color2, uint8_t brightness, int delayTime);
    void turnOnBySquare(CRGB color1,CRGB color2 ,uint8_t bright, uint8_t delayTime);
    void loadingTurnOn(CRGB color1,CRGB color2, uint8_t brightness, int delayTime);
    void fadeIn(CRGB color, CRGB color2,int fadeDelay, uint8_t brightness);
    void fadeOut(int fadeDelay, uint8_t brightness);
    void randomizeSquares();
    uint8_t squares[8][8][4];
};

