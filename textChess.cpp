#include "textChess.h"

textChess::textChess(){ 
}

void textChess::scrollText(uint8_t l1, uint8_t l2,CRGB color1, CRGB color2,int delayTime){
 
 uint8_t size1 = sizeof(lettersU[l1]);
 uint8_t size2 = sizeof(lettersU[l2]);

 uint8_t* packet1 = &lettersU[l1][0];
 uint8_t* packet2=  &lettersU[l2][0];

 for (int shift=0;shift<9;shift++){
   for (int dot1=0;dot1<size1;dot1++){
     uint8_t newDot = packet1[dot1] - (shift*16);
     if (newDot<128){
       //writeSquare(newDot,color1,0);
     }
   }

   for (int dot2=0;dot2<size2;dot2++){
     uint8_t newDot = packet2[dot2] - (shift*16) +128;
     if (newDot<128){
       //writeSquare(newDot,color2,0);
     }
   }
   FastLED.show();
   delay(delayTime);
   //turnOffLEDs();
 }
}

//writes a word via scrolling to the board.
void textChess::writeWord(String stringIn){
 uint8_t wordLength = sizeof(stringIn);
 byte wordIn[wordLength];
 stringIn.toCharArray(wordIn,wordLength);

 int delayTime = 100;
 CRGB color1 = CRGB::Yellow;
 CRGB color2 = CRGB::Red;
 for (int i=0;i<wordLength-2;i++){
   uint8_t l1 = wordIn[i] - 0x41;  //first letter
   uint8_t l2 = wordIn[(i+1)%wordLength] - 0x41; //second letter
   scrollText(l1,l2,color1,color2, delayTime);  //scroll through thosae two letters
 }  //loop and advance by 1 letter
 
}
void textChess::wordTest(){
 writeWord("CHOKU");
}

//counts up from 0-9
void textChess::countup(){
 for (int i=0;i<10;i++){
   //colorPacket(numbers[i]);
   FastLED.show();
   delay(250);
//    turnOffLEDs();
 }
}

//does the whole alphabet
void textChess::alphabet(){
 for (int i=0;i<26;i++){
   //colorPacket(lettersL[i]);
   //FastLED.show();
   //delay(250);
   //turnOffLEDs();
   //colorPacket(lettersU[i]);
   FastLED.show();
   delay(250);
//    turnOffLEDs();
 }
}

void textChess::scrollTextTest(){
 CRGB color1 = CRGB::Blue;
 CRGB color2 = CRGB::Green;
 CRGB color3 = CRGB::Red;
 int delayTime = 100;
 scrollText(0,1,color1,color2,delayTime);
 scrollText(1,2,color2,color3,delayTime/2);
 scrollText(2,3,color1,color2,delayTime);
 scrollText(4,5,color3,color2,delayTime/2);
 scrollText(5,6,color1,color2,delayTime);
}