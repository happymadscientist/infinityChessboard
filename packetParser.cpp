#include "packetParser.h"

packetParser::packetParser(){
}

void packetParser::assign(char* arr,char* newArray){
 strcpy(arr, newArray);
}  

void packetParser::wipeArray(byte arrayIn[]){
 for (int i=0;i<PACKET_SIZE;i++){
   arrayIn[i] = 0;
 }
}

uint8_t packetParser::mpr(uint8_t input){
 return (uint8_t)map(input-0x30,0,9,0,255);
}

bool packetParser::calculateChecksum(byte packet[],uint8_t numBytes){// check checksum of a packet!
 uint8_t runningSum = 0;  
 uint8_t checksum = packet[numBytes];  //last position
 for (uint8_t i=0; i<numBytes-1; i++) {
   runningSum += packet[i];  //add up the values and don't care if it overflows
 }
 runningSum = ~runningSum;  //bitwise not for checksum
 return (runningSum == checksum); // Return true if checksums match
}


void packetParser::parseDaPacket(byte packet[]){
 char first = packet[0];  //get the first charcter of the packet to discern its meaning

 switch (first){ //first check if packet is a reset or a picture packet
   case 'R': {strandPacket(packet); break; } //Reset the board packet
   case 'P': {break;} //picture packet
 }

 
 switch (first){
  /* case 'Q': {colorPacket(packet);break;} //means square // form QRGBdnSS...SS 
   case 'S': {strandPacket(packet);break;} //means strand  //form SRGBn
   case 'L': {loadingPacket(packet);break;} //means loading //form L
   case 'F': {fadePacket(packet);break;}  //means fade  
   //case 'N': {snakePacket(packet); break;} // means snake

   //case 'P': {picturePacket(packet);break;}  //means print picture
 } */
 }
 wipeArray(packet);
}


void packetParser::error(const __FlashStringHelper*err) {
 Serial.println(err);
 while (1);
}


void packetParser::resetPacket(byte packet[]){
 //turnOffLEDs();
 delay(1000);
//  startupTest();
}


//void packetParser::writeArray(byte arrayIn[][5]){
//  for (int i=0;i<sizeof(arrayIn)/5;i++){
//    byte newArray[4];
//    for (int j=0;j<5;j++){
//      newArray[j] = arrayIn[i][j];
//    }
//    parseDaPacket(newArray);
//    }
//}

//form SRGBn
void packetParser::strandPacket(uint8_t packet[]){
 int strandBright = 10;
 CRGB color =  CRGB(mpr(packet[1]),mpr(packet[2]),mpr(packet[3]));//RGB color vals
 uint8_t strand = packet[4]-0x30; //strand number
 //writeStrand(strand,color,strandBright);
}

//form LRGBrgbdb
void packetParser::loadingPacket(uint8_t packet[]){
 CRGB color1 =  CRGB(mpr(packet[1]),mpr(packet[2]),mpr(packet[3]));//RGB color vals - 1st color
 CRGB color2 =  CRGB(mpr(packet[4]),mpr(packet[5]),mpr(packet[6]));//RGB color vals

 uint8_t delayTime = mpr(packet[7]);
 uint8_t brightness = mpr(packet[8]);  //brightness
 //changeBrightness(brightness);
 //loadingTurnOn(color1,color2,brightness,delayTime);
}


void packetParser::colorPacket(byte packet[]){
 CRGB color = CRGB(mpr(packet[1]),mpr(packet[2]),mpr(packet[3]));//RGB color vals
 uint8_t delayTime = 0;//mpr(packet[4]);
 uint8_t numSq = packet[5];  //num of squares
 for (int square=0; square<numSq; square++){
   uint8_t index = square+6;  //offset
   byte coord = packet[index];
   //writeSquare(coord,color,0);
   delay(delayTime);
 }
}
//{'C','9','9','0','1'};
//{0x43,0x39,0x39,0x30,0x31};
void packetParser::fadePacket(byte packet[]){
 CRGB color = CRGB(mpr(packet[1]),mpr(packet[2]),mpr(packet[3]));//RGB color vals
}


void packetParser::packetParserTest(){
 //Color test
 byte packetIn[11] = {0x43,0x39,0x30,0x30,0x31,0x35,0x00,0x01,0x02,0x04,0x05};
 parseDaPacket(packetIn);
 parseDaPacket("C90013012");
 parseDaPacket("C90013012");
 delay(1000);
 //turnOffLEDs();
 delay(1000);

 parseDaPacket("!L09999072");
 delay(1000);
 parseDaPacket("L00000022");


 //strandTest
 //turnOffLEDs();
 parseDaPacket("S0091");  //turn strand #1 full blue
 parseDaPacket("S9900"); //turn strand #0 yellow
 delay(1000);
 parseDaPacket("S0001");  //turn strand #1 full blue
 parseDaPacket("S0000"); //turn strand #0 yellow
 delay(1000);
// colorPacket(commands[2]);
// picturePacket(picPacket);
// colorPacket(packetNew);

// packetParserNew("C0099501234");
// packetParserNew("C09005abcde");
}


/* message parsing commands */
//uint8_t instructions[8][5] = {{1,6,255,34,56},{6,6,255,34,56},{6,1,255,34,56},{1,1,255,34,56},{4,3,255,34,56},{4,4,255,34,56},{3,4,255,34,56},{3,3,255,34,56}};
//given a list of coordinates in form {x,y,R,G,B}, write those squares accordingly
void packetParser::writeArray(uint8_t instructions[][5]){
 for (int i=0;i<sizeof(instructions)/5;i++){
     int x = instructions[i][0];
     int y = instructions[i][1];
//      writeSquareRGB(x,y,instructions[i],1);
 }
}
