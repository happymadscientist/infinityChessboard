#include "chessboard.h"

chessboard::chessboard(){

}

void chessboard::startup(){
  //serialPacketSetup();
//  LEDSetup();
  //startBLE("∞ Chessboard");
}

void chessboard::turnOn(ledWriter* ledControl){
  ledControl->loadingTurnOn(CRGB::Green,CRGB::Red, 10, 50);
}

