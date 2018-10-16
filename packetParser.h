#include <Arduino.h>
//this class takes in packets in the form of byte arrays (from ble or serial) and calls chessboard/led functions according to what the packet says
#include <FastLED.h>
#include "colorutils.h"
#include "userParams.h"
class packetParser {
 public:
   packetParser();
   
   void parseDaPacket(byte packet[]);  //where the parsing happens
   
   //packet manipulation functions
   uint8_t mpr(uint8_t input);  //a function that maps ascii numbers to decimal values
   void wipeArray(byte arrayIn[]);
   bool calculateChecksum(byte packet[],uint8_t numBytes);
   void error(const __FlashStringHelper*err);
   void assign(char* arr,char* newArray);
   void writeArray(uint8_t instructions[][5]);
   //different packet types
   void strandPacket(uint8_t packet[]);
   void loadingPacket(uint8_t packet[]);
   void colorPacket(byte packet[]);
   void fadePacket(byte packet[]);
   void snakePacket(byte packet[]);
   void picturePacket(byte packet[]);
   void resetPacket(byte packet[]);  //wipe a packet

   void packetParserTest();
   uint8_t packet[PACKET_SIZE+1];  //buffer to hold incoming characters plus one for the checksum
};
